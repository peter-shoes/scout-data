
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd


SPREADSHEET_ID = # <Your spreadsheet ID>
RANGE_NAME = sheet_1

# YOU NEED TO PUT YOUR CREDENTIALS FILES INTO THIS FOLDER

def get_google_sheet(spreadsheet_id, range_name):
    # Retrieve sheet data using OAuth credentials and Google Python API.
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet


def gsheet2df(gsheet):
    # Converts Google sheet data to a Pandas DataFrame.
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df


gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
df = gsheet2df(gsheet)

def get_query():
    print('Select column and value to search for')
    print('===================')
    print(df.columns)
    col_choice = input('Column Choice:\n')
    query = input('Value to search for in %s\n:'%col_choice)
    rows = df.loc[df[col_choice] == query]
    try:
        return rows
    except:
        return False
