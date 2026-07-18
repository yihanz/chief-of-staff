#!/usr/bin/env python3
"""
Comprehensive, dependency-free test suite for the imessage-fixed reader
(server/main.py). Standard-library `unittest` only.

WHAT THIS DOES
--------------
Every test builds a synthetic macOS Messages `chat.db` SQLite fixture that
mirrors the real schema (grounded on a 207k-message DB), points the reader at
it via $IMSG_DB, and asserts the reader's behaviour. The reader is treated as a
black box and is never edited; failures here are bugs for someone else to fix.

Run:   python3 test_reader.py
       python3 test_reader.py -v

Schema facts modelled (from the real DB):
  * Sent message: is_from_me=1, handle_id=0 (no sender handle row).
  * date is nanoseconds since 2001-01-01 (APPLE_EPOCH = 978307200).
  * Apple Cash: balloon_bundle_id ~ PeerPayment/PassbookUIService, text empty,
    amount inside payload_data (a binary bplist).
  * Tapbacks: associated_message_type != 0. Group events: item_type != 0.
    Both must be excluded from reads.
"""

import os
import sys
import json
import time
import sqlite3
import tempfile
import shutil
import subprocess
import importlib.util
import unittest

# --------------------------------------------------------------------------
# Load the reader under test as a module (never edited).
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_PATH = os.path.join(HERE, "server", "main.py")

_spec = importlib.util.spec_from_file_location("imsg_main", MAIN_PATH)
main = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(main)

APPLE_EPOCH = 978307200


# --------------------------------------------------------------------------
# Fixture helpers
# --------------------------------------------------------------------------
def apple_ns(seconds_ago):
    """Return an Apple-epoch nanosecond timestamp for `seconds_ago` seconds in the past."""
    unix = time.time() - seconds_ago
    return int((unix - APPLE_EPOCH) * 1e9)


MESSAGE_COLS_FULL = (
    "ROWID INTEGER PRIMARY KEY, text, attributedBody, is_from_me, date, "
    "handle_id, cache_has_attachments, item_type, associated_message_type, "
    "balloon_bundle_id, payload_data"
)
MESSAGE_COLS_MIN = (
    "ROWID INTEGER PRIMARY KEY, text, attributedBody, is_from_me, date, "
    "handle_id, cache_has_attachments"
)


def new_db(path, schema="full"):
    """
    Create a fresh chat.db fixture.
      schema="full"           full modern schema
      schema="no_chat_tables" no chat/chat_message_join/chat_handle_join
      schema="min_cols"       message table missing item_type,
                              associated_message_type, balloon_bundle_id,
                              payload_data
    Returns an open connection; caller inserts rows, commits, and closes.
    """
    con = sqlite3.connect(path)
    mcols = MESSAGE_COLS_MIN if schema == "min_cols" else MESSAGE_COLS_FULL
    con.execute("CREATE TABLE message(%s)" % mcols)
    con.execute("CREATE TABLE handle(ROWID INTEGER PRIMARY KEY, id)")
    con.execute("CREATE TABLE attachment(ROWID INTEGER PRIMARY KEY, filename)")
    con.execute("CREATE TABLE message_attachment_join(message_id, attachment_id)")
    if schema != "no_chat_tables":
        con.execute("CREATE TABLE chat(ROWID INTEGER PRIMARY KEY, display_name, chat_identifier)")
        con.execute("CREATE TABLE chat_message_join(chat_id, message_id)")
        con.execute("CREATE TABLE chat_handle_join(chat_id, handle_id)")
    return con


def make_typedstream(text):
    """
    Build a minimal but structurally-real NSArchiver typedstream blob whose
    embedded NSString the reader's _decode_typed() should parse: locate
    'NSString', find the 0x2b ('+') marker within 16 bytes, then a single
    length byte followed by exactly that many UTF-8 bytes.
    """
    body = text.encode("utf-8")
    assert len(body) < 128, "helper only builds single-byte-length strings"
    return (
        b"\x04\x0bstreamtyped\x81\xe8\x03\x84\x01@\x84\x84"
        b"NSString\x01\x95\x84\x01"        # class marker then a short run
        b"+" + bytes([len(body)]) + body   # 0x2b, length, text
    )


class ReaderTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="imsgtest_")
        self.db = os.path.join(self.tmp, "chat.db")
        self._old_env = os.environ.get("IMSG_DB")
        os.environ["IMSG_DB"] = self.db

    def tearDown(self):
        if self._old_env is None:
            os.environ.pop("IMSG_DB", None)
        else:
            os.environ["IMSG_DB"] = self._old_env
        shutil.rmtree(self.tmp, ignore_errors=True)


# ==========================================================================
# 1. THE CORE FIX — sent (handle_id=0) + received both returned, order, from_me
# ==========================================================================
class TestCoreFix(ReaderTestBase):
    def test_read_thread_includes_sent_and_received_newest_first(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        # received (older), handle_id=7
        con.execute(
            "INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'hi from them',0,?,7)",
            (apple_ns(600),),
        )
        # sent (newer), is_from_me=1 handle_id=0  <-- the row an INNER JOIN drops
        con.execute(
            "INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (11,'reply from me',1,?,0)",
            (apple_ns(60),),
        )
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10),(1,11)")
        con.commit(); con.close()

        out = main.read_thread("+15551234567")
        texts = [m["text"] for m in out]
        self.assertEqual(
            len(out), 2,
            "read_thread must return BOTH sent and received; got %r" % (out,),
        )
        # newest-first: sent reply is newer -> first
        self.assertEqual(texts[0], "reply from me", "order must be newest-first")
        self.assertEqual(texts[1], "hi from them")
        self.assertTrue(out[0]["from_me"], "sent row must be from_me=True")
        self.assertFalse(out[1]["from_me"], "received row must be from_me=False")
        self.assertEqual(out[0]["handle"], "me")


# ==========================================================================
# 2. Handle matching: short code / de-prefixed / +1-prefixed all resolve
# ==========================================================================
class TestHandleMatching(ReaderTestBase):
    def _build_e164(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'ping',0,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()

    def test_e164_query(self):
        self._build_e164()
        self.assertEqual(len(main.read_thread("+15551234567")), 1)

    def test_deprefixed_query(self):
        self._build_e164()
        self.assertEqual(
            len(main.read_thread("5551234567")), 1,
            "bare 10-digit query must resolve a +1E164 handle",
        )

    def test_plus_prefixed_query(self):
        self._build_e164()
        self.assertEqual(
            len(main.read_thread("15551234567")), 1,
            "'1NNNNNNNNNN' query must resolve a +1E164 handle",
        )

    def test_short_code(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (9,'262966')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'262966')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,9)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'AMZN code',0,?,9)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        self.assertEqual(len(main.read_thread("262966")), 1, "short code must resolve exactly")


# ==========================================================================
# 3. attributedBody decoding (text NULL, typedstream blob)
# ==========================================================================
class TestAttributedBody(ReaderTestBase):
    def test_typedstream_decoded(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        blob = make_typedstream("Decoded body text")
        con.execute(
            "INSERT INTO message(ROWID,text,attributedBody,is_from_me,date,handle_id) VALUES (10,NULL,?,1,?,0)",
            (blob, apple_ns(60)),
        )
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(len(out), 1)
        self.assertEqual(
            out[0]["text"], "Decoded body text",
            "sent message with text=NULL must decode its attributedBody",
        )

    def test_decode_helper_typed(self):
        self.assertEqual(main._decode(make_typedstream("Hello")), "Hello")

    def test_decode_helper_fallback(self):
        # No NSString marker -> fallback keeps printable runs.
        blob = b"\x00\x00Hello World\x07more text\x00"
        self.assertIn("Hello World", main._decode(blob))


# ==========================================================================
# 4. Apple Cash payments (amount present / unparseable)
# ==========================================================================
class TestAppleCash(ReaderTestBase):
    def test_amount_present(self):
        payload = b"bplist00\x01\x02amount$25.00USD junk"
        self.assertEqual(main._balloon_label("com.apple.messages.MSMessageExtensionBalloonPlugin:PeerPayment", payload),
                         "[Apple Cash: $25.00]")

    def test_amount_unparseable(self):
        payload = b"bplist00 no currency here just words"
        self.assertEqual(
            main._balloon_label("PeerPaymentMessagesExtension", payload),
            "[Apple Cash payment]",
            "unparseable payment must fall back to a plain label, never blank",
        )

    def test_read_thread_surfaces_payment(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        payload = b"\x00\x00USD 40.00 sent\x00"
        con.execute(
            "INSERT INTO message(ROWID,text,is_from_me,date,handle_id,balloon_bundle_id,payload_data) "
            "VALUES (10,'',1,?,0,'PeerPaymentMessagesExtension',?)",
            (apple_ns(60), payload),
        )
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["text"], "[Apple Cash: $40.00]")


# ==========================================================================
# 5. Tapbacks (assoc_type!=0) and group events (item_type!=0) EXCLUDED
# ==========================================================================
class TestExclusions(ReaderTestBase):
    def _build(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        rows = [
            # a normal keeper
            (10, "real message", 0, 0, 0, apple_ns(300), 7),
            # tapback (associated_message_type != 0) -> excluded
            (11, "Liked “real message”", 0, 0, 2000, apple_ns(200), 7),
            # group event (item_type != 0) -> excluded
            (12, None, 0, 1, 0, apple_ns(100), 7),
        ]
        for rid, txt, fm, it, at, dt, hid in rows:
            con.execute(
                "INSERT INTO message(ROWID,text,is_from_me,item_type,associated_message_type,date,handle_id) "
                "VALUES (?,?,?,?,?,?,?)",
                (rid, txt, fm, it, at, dt, hid),
            )
            con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,?)", (rid,))
        con.commit(); con.close()

    def test_read_thread_excludes(self):
        self._build()
        out = main.read_thread("+15551234567")
        self.assertEqual([m["text"] for m in out], ["real message"],
                         "tapbacks and group events must be excluded from read_thread")

    def test_recent_excludes(self):
        self._build()
        out = main.recent(hours=1, limit=50)
        texts = [m["text"] for m in out]
        self.assertIn("real message", texts)
        self.assertTrue(all("Liked" not in (t or "") for t in texts),
                        "tapback leaked into recent(): %r" % texts)


# ==========================================================================
# 6. recent(): includes sent, excludes tapbacks/events, respects limit, order
# ==========================================================================
class TestRecent(ReaderTestBase):
    def test_recent_sent_limit_order(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        # 3 sent + 1 received, staggered times
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (1,'m-oldest',1,?,0)", (apple_ns(400),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (2,'m-mid',0,?,7)", (apple_ns(300),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (3,'m-new',1,?,0)", (apple_ns(200),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (4,'m-newest',1,?,0)", (apple_ns(100),))
        con.commit(); con.close()

        out = main.recent(hours=1, limit=2)
        self.assertEqual(len(out), 2, "limit must be respected")
        self.assertEqual(out[0]["text"], "m-newest", "newest first")
        self.assertEqual(out[1]["text"], "m-new")
        self.assertTrue(out[0]["from_me"])

        allout = main.recent(hours=1, limit=60)
        self.assertEqual(len(allout), 4, "sent messages (handle_id=0) must be included")


# ==========================================================================
# 7. search(): finds a term that appears only in a SENT message
# ==========================================================================
class TestSearch(ReaderTestBase):
    def test_search_finds_sent_term(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (1,'they said hello',0,?,7)", (apple_ns(300),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (2,'unicornsparkle plan',1,?,0)", (apple_ns(200),))
        con.commit(); con.close()
        out = main.search("unicornsparkle", days=7)
        self.assertEqual(len(out), 1, "term only in a SENT message must be found")
        self.assertTrue(out[0]["from_me"])


# ==========================================================================
# 8. list_threads(): 1:1 + group + a chat you only sent into; count; latest
# ==========================================================================
class TestListThreads(ReaderTestBase):
    def test_enumerates_all_chats(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO handle(ROWID,id) VALUES (8,'+15559990000')")
        # chat 1: 1:1 with two messages
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'oneone a',0,?,7)", (apple_ns(500),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (11,'oneone latest',1,?,0)", (apple_ns(400),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10),(1,11)")
        # chat 2: named group
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (2,'Weekend Crew','chat999')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (20,'group hi',0,?,8)", (apple_ns(300),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (2,20)")
        # chat 3: one you ONLY sent into (all handle_id=0)
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (3,NULL,'+15550001111')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (30,'only me here',1,?,0)", (apple_ns(200),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (3,30)")
        con.commit(); con.close()

        out = main.list_threads(hours=1, limit=40)
        convs = {d["conversation"]: d for d in out}
        self.assertIn("Weekend Crew", convs, "named group must appear")
        self.assertIn("+15550001111", convs, "a chat you only sent into must appear")
        self.assertIn("+15551234567", convs, "1:1 must appear")
        # count for 1:1 = 2 messages
        self.assertEqual(convs["+15551234567"]["count"], 2, "count must reflect message total")
        # latest message text for the 1:1
        self.assertEqual(convs["+15551234567"]["text"], "oneone latest", "latest message must be surfaced")


# ==========================================================================
# 9. read_chat(): group chat by name, both sides
# ==========================================================================
class TestReadChat(ReaderTestBase):
    def test_group_by_name_both_sides(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (8,'+15559990000')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (2,'Book Club','chat42')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (20,'from a member',0,?,8)", (apple_ns(300),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (21,'my reply',1,?,0)", (apple_ns(200),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (2,20),(2,21)")
        con.commit(); con.close()
        out = main.read_chat("Book Club")
        texts = sorted(m["text"] for m in out)
        self.assertEqual(texts, ["from a member", "my reply"],
                         "read_chat must return both sides of a named group")
        self.assertTrue(any(m["from_me"] for m in out))
        self.assertTrue(any(not m["from_me"] for m in out))


# ==========================================================================
# 10. Edge / robustness
# ==========================================================================
class TestEdgeCases(ReaderTestBase):
    def test_person_in_1to1_and_group_prefers_1to1(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO handle(ROWID,id) VALUES (8,'+15559990000')")
        # 1:1 (single participant)
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'direct only',0,?,7)", (apple_ns(300),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        # group containing same handle 7 plus handle 8
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (2,'Group','chat2')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (2,7),(2,8)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (20,'GROUP LEAK',0,?,7)", (apple_ns(100),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (2,20)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        texts = [m["text"] for m in out]
        self.assertEqual(texts, ["direct only"],
                         "1:1 must be preferred; group message leaked: %r" % texts)

    def test_handle_in_zero_chats_no_crash(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'orphan',0,?,7)", (apple_ns(60),))
        con.commit(); con.close()
        # handle exists but is in no chat -> fallback path
        out = main.read_thread("+15551234567")
        self.assertEqual([m["text"] for m in out], ["orphan"],
                         "fallback (no chat membership) must still return received messages")

    def test_totally_blank_message_dropped_from_recent(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,attributedBody,is_from_me,date,handle_id,balloon_bundle_id) "
                    "VALUES (10,NULL,NULL,0,?,7,NULL)", (apple_ns(120),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (11,'has text',0,?,7)", (apple_ns(60),))
        con.commit(); con.close()
        out = main.recent(hours=1, limit=50)
        self.assertEqual([m["text"] for m in out], ["has text"],
                         "a fully blank message must be dropped from recent()")

    def test_null_date_no_crash(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'no date',0,NULL,7)")
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(len(out), 1)
        self.assertIsNone(out[0]["ts"], "NULL date must yield ts=None without crashing")

    def test_null_is_from_me_no_crash(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'weird',NULL,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(len(out), 1)
        self.assertFalse(out[0]["from_me"])

    def test_null_names_in_list_threads(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,NULL)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'anon chat',0,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.list_threads(hours=1, limit=40)
        self.assertEqual(len(out), 1, "chat with NULL name+identifier must not crash list_threads")
        self.assertIsNone(out[0]["conversation"])

    def test_identical_dates_no_duplicate(self):
        # Fixed in v1.4.0: list_threads picks exactly one latest message per chat
        # (highest ROWID at the max date), so two messages sharing the latest
        # timestamp no longer fan the chat out into duplicate rows.
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,'Dup Chat','chat1')")
        dt = apple_ns(120)
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'first',0,?,7)", (dt,))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (11,'second',1,?,0)", (dt,))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10),(1,11)")
        con.commit(); con.close()
        out = main.list_threads(hours=1, limit=40)
        names = [d["conversation"] for d in out]
        self.assertEqual(names.count("Dup Chat"), 1,
                         "two messages sharing the max date must not duplicate the chat in "
                         "list_threads; got rows=%r" % (names,))

    def test_unicode_emoji_roundtrip(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        msg = "Hey \U0001F389 café naïve 你好"
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,?,0,?,7)", (msg, apple_ns(60)))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(out[0]["text"], msg, "unicode/emoji must round-trip unchanged")

    def test_limit_zero_and_large(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'a',0,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()
        self.assertEqual(main.read_thread("+15551234567", limit=0), [],
                         "limit=0 must return no rows")
        self.assertEqual(len(main.read_thread("+15551234567", limit=100000)), 1,
                         "a very large limit must be fine")

    def test_attachments_surfaced(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id,cache_has_attachments) "
                    "VALUES (10,'see pic',0,?,7,1)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.execute("INSERT INTO attachment(ROWID,filename) VALUES (55,'/var/mobile/Attachments/ab/photo.jpg')")
        con.execute("INSERT INTO message_attachment_join(message_id,attachment_id) VALUES (10,55)")
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual(out[0].get("attachments"), ["photo.jpg"],
                         "attachment basename must be surfaced by read_thread")


# ==========================================================================
# 11. Schema variants (missing chat tables / missing optional columns)
# ==========================================================================
class TestSchemaVariants(ReaderTestBase):
    def test_missing_chat_tables_fallback(self):
        con = new_db(self.db, schema="no_chat_tables")
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'received only',0,?,7)", (apple_ns(60),))
        con.commit(); con.close()
        out = main.read_thread("+15551234567")
        self.assertEqual([m["text"] for m in out], ["received only"],
                         "missing chat tables must degrade to the received-by-handle fallback")

    def test_missing_optional_columns(self):
        con = new_db(self.db, schema="min_cols")
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (1,'plain sent',1,?,0)", (apple_ns(120),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (2,'plain recv',0,?,7)", (apple_ns(60),))
        con.commit(); con.close()
        # recent must not reference item_type/associated_message_type/balloon columns
        out = main.recent(hours=1, limit=50)
        texts = sorted(m["text"] for m in out)
        self.assertEqual(texts, ["plain recv", "plain sent"],
                         "reader must work when optional message columns are absent")


# ==========================================================================
# 12. _amount false-positive probe (no bogus $ from id/timestamp/phone)
# ==========================================================================
class TestAmountFalsePositive(ReaderTestBase):
    BBID = "PeerPaymentMessagesExtension"

    def test_long_id_no_bogus_amount(self):
        payload = b"\x00transactionID=A1B2C3D4E5F60718293A4B5C6D\x00"
        self.assertEqual(main._balloon_label(self.BBID, payload), "[Apple Cash payment]",
                         "a long hex id must NOT be read as a dollar amount")

    def test_integer_timestamp_no_bogus_amount(self):
        payload = b"\x00date=1721000000 seconds=703980000\x00"
        self.assertEqual(main._balloon_label(self.BBID, payload), "[Apple Cash payment]",
                         "an integer/epoch timestamp must NOT be read as a dollar amount")

    def test_phone_like_no_bogus_amount(self):
        payload = b"\x00from=+15551234567 to=+15559990000\x00"
        self.assertEqual(main._balloon_label(self.BBID, payload), "[Apple Cash payment]",
                         "a phone-like number must NOT be read as a dollar amount")

    def test_design_probe_bare_decimal(self):
        """
        DESIGN PROBE (not a hard failure): the second _amount() regex matches any
        bare N.NN token. A payload containing an incidental decimal (e.g. a build
        string or ratio) with NO currency token becomes a dollar figure. Recorded
        here to document the false-positive surface; asserted loosely.
        """
        payload = b"\x00build 30.14 ratio\x00"
        got = main._balloon_label(self.BBID, payload)
        # We only *document* the behaviour; a bare decimal currently yields $30.14.
        self.assertIn(got, ("[Apple Cash payment]", "[Apple Cash: $30.14]"))
        if got != "[Apple Cash payment]":
            sys.stderr.write(
                "\n[DESIGN NOTE] _amount() false-positive: bare decimal '30.14' -> %s\n" % got
            )


# ==========================================================================
# 13. JSON-RPC subprocess round-trip
# ==========================================================================
class TestJsonRpc(ReaderTestBase):
    def _build_min_db(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'rpc hi',0,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()

    def test_full_rpc_session(self):
        self._build_min_db()
        env = dict(os.environ)
        env["IMSG_DB"] = self.db
        lines = [
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
            json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                        "params": {"name": "imsg_read_thread", "arguments": {"handle": "+15551234567"}}}),
            json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),  # no response
            "{ this is not json",                                                   # malformed, ignored
            json.dumps({"jsonrpc": "2.0", "id": 4, "method": "does/not/exist"}),    # error, stays up
            json.dumps({"jsonrpc": "2.0", "id": 5, "method": "tools/list"}),        # proves survival
        ]
        proc = subprocess.run(
            [sys.executable, MAIN_PATH],
            input="\n".join(lines) + "\n",
            capture_output=True, text=True, env=env, timeout=30,
        )
        responses = {}
        for ln in proc.stdout.splitlines():
            ln = ln.strip()
            if not ln:
                continue
            obj = json.loads(ln)
            responses[obj.get("id")] = obj

        # initialize -> serverInfo.version
        self.assertIn(1, responses)
        self.assertEqual(responses[1]["result"]["serverInfo"]["version"], main.VERSION)
        # tools/list -> 5 tools
        self.assertIn(2, responses)
        self.assertEqual(len(responses[2]["result"]["tools"]), 5)
        # tools/call read_thread -> content with our message
        self.assertIn(3, responses)
        payload = json.loads(responses[3]["result"]["content"][0]["text"])
        self.assertEqual(payload[0]["text"], "rpc hi")
        # notification produced no response id
        self.assertNotIn(None, responses, "a notification must not produce a response")
        # unknown method -> JSON-RPC error, server did not die
        self.assertIn(4, responses)
        self.assertIn("error", responses[4])
        self.assertEqual(responses[4]["error"]["code"], -32601)
        # malformed line ignored AND server survived to answer id=5
        self.assertIn(5, responses, "server must survive a malformed line and keep serving")
        self.assertEqual(len(responses[5]["result"]["tools"]), 5)


# ==========================================================================
# 14. Hardening — the defects the adversarial review found (v1.4.0)
# ==========================================================================
class TestHardening(ReaderTestBase):
    def test_valid_non_object_json_does_not_kill_server(self):
        # The CRITICAL bug: a spec-legal-but-non-object JSON line (a number, a
        # string, a bool, null, or a JSON-RPC batch array) used to hit req.get()
        # on a non-dict, raise, and take the whole stdin loop down permanently.
        self._min_db()
        env = dict(os.environ); env["IMSG_DB"] = self.db
        lines = [
            "5", '"hello"', "true", "null",
            json.dumps([{"jsonrpc": "2.0", "id": 99, "method": "tools/list"}]),  # batch array
            json.dumps({"jsonrpc": "2.0", "id": 9, "method": "tools/list"}),      # must still answer
        ]
        proc = subprocess.run([sys.executable, MAIN_PATH], input="\n".join(lines) + "\n",
                              capture_output=True, text=True, env=env, timeout=30)
        responses = {json.loads(l).get("id"): json.loads(l)
                     for l in proc.stdout.splitlines() if l.strip()}
        self.assertIn(9, responses, "server must survive non-object JSON and keep serving")
        self.assertEqual(len(responses[9]["result"]["tools"]), 5)

    def _min_db(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'hi',0,?,7)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10)")
        con.commit(); con.close()

    def test_clamp_never_unlimited(self):
        # Negative LIMIT is UNLIMITED in SQLite — the DoS the cap prevents.
        self.assertEqual(main._clamp(-1, 20, 500), 0)     # negative -> nothing, never -1
        self.assertEqual(main._clamp(-9999, 20, 500), 0)
        self.assertEqual(main._clamp(0, 20, 500), 0)      # 0 honoured as "none"
        self.assertEqual(main._clamp(10, 20, 500), 10)
        self.assertEqual(main._clamp(10_000_000, 20, 500), 500)  # capped
        self.assertEqual(main._clamp(None, 20, 500), 20)  # missing -> default
        self.assertEqual(main._clamp("nope", 20, 500), 20)

    def test_read_thread_huge_limit_is_bounded(self):
        self._min_db()
        # A caller asking for 10M rows must not be honoured literally.
        out = main.read_thread("+15551234567", limit=10_000_000)
        self.assertLessEqual(len(out), main.LIMIT_MAX)

    def test_amount_rejects_plist_noise(self):
        # payload_data is an archived plist full of '$' keys and stray numbers.
        # A confident wrong amount is worse than the honest label, so _amount
        # accepts ONLY a currency token followed by cents.
        self.assertEqual(main._amount(b'bplist00 ... USD 50.00 ...'), '$50.00')
        self.assertEqual(main._amount(b'... total $1,250.00 paid ...'), '$1,250.00')
        self.assertEqual(main._amount(b'$class$archiver$version 100000 $top'), '')  # plist keys/ints
        self.assertEqual(main._amount(b'NSParagraphStyle 12.00 NSFont 14.00'), '')  # font/metrics
        self.assertEqual(main._amount(b'$5000000'), '')          # currency but NO cents -> reject
        self.assertEqual(main._amount(b'call me at 5551234567'), '')  # bare digits
        self.assertEqual(main._amount(None), '')
        # and the label falls back cleanly rather than fabricating a number
        pay = 'com.apple.messages.MSMessageExtensionBalloonPlugin:0:com.apple.PassbookUIService.PeerPaymentMessagesExtension'
        self.assertEqual(main._balloon_label(pay, b'$class$version 100000'), '[Apple Cash payment]')
        self.assertEqual(main._balloon_label(pay, b'USD 25.00'), '[Apple Cash: $25.00]')

    def test_search_recall_beyond_scan_cap(self):
        # A text-column match must be found even when it is older than thousands
        # of newer body-bearing messages. The old single-pass code capped the scan
        # at 4000 rows and silently dropped anything beyond it; the two-pass search
        # lets SQL filter the text column, so text-match recall is complete.
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,NULL,'+15551234567')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (1,'the needle is here',0,?,7)",
                    (apple_ns(100000),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,1)")
        ab = make_typedstream("just noise")
        base = apple_ns(50000)
        noise = [(1000+i, "noise", ab, 0, base + i*1_000_000_000, 7) for i in range(4100)]
        con.executemany("INSERT INTO message(ROWID,text,attributedBody,is_from_me,date,handle_id) VALUES (?,?,?,?,?,?)", noise)
        con.executemany("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,?)", [(1000+i,) for i in range(4100)])
        con.commit(); con.close()
        out = main.search("needle", days=3650, limit=10)
        self.assertTrue(any("needle" in (m["text"] or "") for m in out),
                        "a text-column match beyond the body scan cap must still be found")

    def test_list_threads_ordered_newest_first(self):
        con = new_db(self.db)
        con.execute("INSERT INTO handle(ROWID,id) VALUES (7,'+15551234567'),(8,'+15559990000')")
        con.execute("INSERT INTO chat(ROWID,display_name,chat_identifier) VALUES (1,'Older','c1'),(2,'Newer','c2')")
        con.execute("INSERT INTO chat_handle_join(chat_id,handle_id) VALUES (1,7),(2,8)")
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (10,'old',0,?,7)", (apple_ns(9000),))
        con.execute("INSERT INTO message(ROWID,text,is_from_me,date,handle_id) VALUES (11,'new',0,?,8)", (apple_ns(60),))
        con.execute("INSERT INTO chat_message_join(chat_id,message_id) VALUES (1,10),(2,11)")
        con.commit(); con.close()
        out = main.list_threads(hours=99999, limit=40)
        self.assertEqual([d["conversation"] for d in out][:2], ["Newer", "Older"],
                         "list_threads must order conversations newest-first")


if __name__ == "__main__":
    unittest.main(verbosity=2)
