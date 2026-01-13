import base64

def extract_email_data(message):
    headers = message["payload"]["headers"]

    def get_header(name):
        for h in headers:
            if h["name"] == name:
                return h["value"]
        return ""

    sender = get_header("From")
    subject = get_header("Subject")
    date = get_header("Date")

    body = ""
    payload = message["payload"]

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                break
    else:
        data = payload["body"].get("data", "")
        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return sender, subject, date, body
