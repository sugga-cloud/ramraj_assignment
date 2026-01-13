import pickle
from googleapiclient.discovery import build
from config import SPREADSHEET_ID, SHEET_NAME

TOKEN_FILE = "credentials/token.pickle"

def get_sheets_service():
    with open(TOKEN_FILE, "rb") as token:
        creds = pickle.load(token)
    return build("sheets", "v4", credentials=creds)

def append_row(service, row):
    body = {"values": [row]}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
