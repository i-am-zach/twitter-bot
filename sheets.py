import gspread
from oauth2client.service_account import ServiceAccountCredentials

"""
docs: https://github.com/burnash/gspread
"""

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('twitter-bot').sheet1

messages = sheet.col_values(1)

if __name__ == "__main__":
    from pprint import pprint
    pprint(messages)