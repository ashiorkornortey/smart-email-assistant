import os
import imaplib
import email
import sqlite3
from email.header import decode_header

IMAP_HOST = os.environ.get("IMAP_HOST")  
IMAP_USER = os.environ.get("IMAP_USER")
IMAP_PASS = os.environ.get("IMAP_PASS")

DB = os.path.join(os.path.dirname(__file__), "..", "data", "emails.sqlite")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            date TEXT,
            body TEXT,
            category TEXT,
            priority TEXT,
            draft_reply TEXT
        )
    ''')
    conn.commit()
    return conn

def decode_str(s):
    parts = decode_header(s)
    out = []
    for text, enc in parts:
        if isinstance(text, bytes):
            out.append(text.decode(enc or "utf-8", errors="ignore"))
        else:
            out.append(text)
    return "".join(out)

def fetch():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")

    typ, data = mail.search(None, '(SINCE "01-Dec-2025")')
    email_ids = data[0].split()
    print(f"Found {len(email_ids)} emails to fetch.")

    conn = init_db()
    c = conn.cursor()

    for num in email_ids:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        msg_id = msg.get('Message-ID') or num.decode()
        subject = decode_str(msg.get('Subject', ''))
        sender = decode_str(msg.get('From', ''))
        date = msg.get('Date', '')
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and part.get_content_disposition() in (None,'inline'):
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")


        c.execute("""
            INSERT OR IGNORE INTO emails 
            (id, sender, subject, date, body, category, priority, draft_reply)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (msg_id, sender, subject, date, body, None, None, None))

    conn.commit()
    conn.close()
    mail.logout()
    print("Emails fetched and saved successfully!")

if __name__ == "__main__":
    fetch()
