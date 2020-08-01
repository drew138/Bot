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

data = sheet.col_values(2)
data = data[1]

date_time_obj = datetime.strptime('1/8/2020', '%d/%m/%Y')

print(datetime.now())
