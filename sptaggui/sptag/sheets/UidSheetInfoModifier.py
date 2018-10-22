from oauth2client import file

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

SPREADSHEET_ID = "1zRSYqFLEEHLTDiMwv_tjmZ2aUK3V4LZ9E4OVBDFX_OI"

class UidSheetInfoModifier:
    _credentials = None


    def __init__(self):
        cred_file = file.Storage("credentials.json")
        self._credentials = cred_file.get()

        if not self._credentials or self._credentials.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)