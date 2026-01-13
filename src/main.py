import json
import os
from gmail_service import get_gmail_service
from sheets_service import get_sheets_service, append_row
from email_parser import extract_email_data
from config import STATE_FILE

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state), f)

def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    processed_ids = load_state()

    results = gmail.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = results.get("messages", [])

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        message = gmail.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        sender, subject, date, body = extract_email_data(message)

        append_row(sheets, [sender, subject, date, body])

        gmail.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        processed_ids.add(msg_id)

    save_state(processed_ids)

if __name__ == "__main__":
    main()
