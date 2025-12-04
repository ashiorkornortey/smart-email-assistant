
import sqlite3
import spacy
from generate_replies import generate_reply

DB = "data/emails.sqlite"


nlp = spacy.load("en_core_web_sm")  


KEYWORDS = {
    "Meeting": ["meeting", "call", "schedule", "tapaaminen"],
    "Request": ["please", "could you", "request", "pyydän"],
    "Report": ["report", "attached", "raportti"],
    "Follow-up": ["following up", "reminder", "seurantaa"],
    "Newsletter": ["unsubscribe", "newsletter", "uutiskirje"]
}

CATEGORY_DOCS = {cat: nlp(" ".join(kws)) for cat, kws in KEYWORDS.items()}

def classify_text(text):
    text = (text or "").lower()
    doc = nlp(text)


    for cat, kws in KEYWORDS.items():
        if any(kw in text for kw in kws):
            return cat

    
    max_sim = 0
    best_cat = "Other"
    for cat, cat_doc in CATEGORY_DOCS.items():
        sim = doc.similarity(cat_doc)
        if sim > max_sim and sim > 0.6:
            max_sim = sim
            best_cat = cat
    return best_cat


def annotate():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT id, subject, body, category FROM emails")
    rows = c.fetchall()

    for row in rows:
        msg_id, subject, body, category_existing = row

    
        if category_existing and category_existing != "Other":
            category = category_existing
        else:
            category = classify_text(subject + " " + body)

        c.execute("SELECT draft_reply FROM emails WHERE id=?", (msg_id,))
        draft_row = c.fetchone()
        draft_existing = draft_row[0] if draft_row else None

        if not draft_existing:
            draft = generate_reply(category)
        else:
            draft = draft_existing

        c.execute("""
            UPDATE emails
            SET category=?, draft_reply=?
            WHERE id=?
        """, (category, draft, msg_id))

        print(f"ID: {msg_id[:10]} | Subject: {subject[:30]} | Category: {category} | Draft: {draft[:40]}")

    conn.commit()
    conn.close()
    print(" All emails categorized and draft replies generated!")

if __name__ == "__main__":
    annotate()
