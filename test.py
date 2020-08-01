import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("WEBSERVERFECHASDISCORD").sheet1

old = ""
new = ", ".join([old, "examen"])
print(new)
