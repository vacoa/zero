from __future__ import print_function
import pickle
import os.path
from pprint import pprint
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class Gsheet():
    
    def __init__(self,secret):
        creds = None
        credFolder = os.path.dirname(secret)
        pickleFile = credFolder + '/token.pickle'
        # If modifying these scopes, delete the file token.pickle.
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(pickleFile):
            with open(pickleFile, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    secret, scopes)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(pickleFile, 'wb') as token:
                pickle.dump(creds, token)

        self.service = discovery.build('sheets', 'v4', credentials=creds, cache_discovery=False)

         
        # The A1 notation of a range to search for a logical table of data.
        # Values will be appended after the last row of the table.
        self.range_ = 'A1'  
        # How the input data should be interpreted.
        self.value_input_option = 'USER_ENTERED' 
        # How the input data should be inserted.
        self.insert_data_option = 'INSERT_ROWS'

    def append(self,spreadsheet_id,values):

        # The ID of the spreadsheet to update.
        #spreadsheet_id = 'id_of_the_spreadsheet' 

        #value_range_body = {
         #   "values": [
         #   ["Cost", "Stocked", "Ship Date"],
         #   ["$20.50", "4", "3/1/2016"]
         # ]
        #}

        value_range_body = {
            "values": values
        }

        request = self.service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=self.range_, valueInputOption=self.value_input_option, insertDataOption=self.insert_data_option, body=value_range_body)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        pprint(response)

