from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools, client

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = "1zRSYqFLEEHLTDiMwv_tjmZ2aUK3V4LZ9E4OVBDFX_OI"
SPREADSHEET_RANGE_PREFIX = "Test!A"
SPREADSHEET_UID_SEARCH_RANGE = SPREADSHEET_RANGE_PREFIX + "1:A"


class UidSheetInfoModifier:
    _credentials = None
    _sheets_service = None

    class PartInfo(object):
        uid = None
        name = None
        description = None
        location = None
        imageUrl = None

        def __init__(self, uid=None, name=None, description=None, location=None,
                     imageUrl=None):
            self.uid = uid
            self.name = name
            self.description = description
            self.location = location
            self.imageUrl = imageUrl


    def __init__(self):
        cred_file = file.Storage("credentials.json")
        self._credentials = cred_file.get()

        if not self._credentials or self._credentials.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            self._credentials = tools.run_flow(flow, cred_file)

        self._sheets_service = build('sheets', 'v4',
                                     http=self._credentials.authorize(Http()))

    def _uid_to_row_number(self, uid):
        rawUidGetResult = self._sheets_service.spreadsheets().values().get(
                                            spreadsheetId=SPREADSHEET_ID,
                                            range=SPREADSHEET_UID_SEARCH_RANGE).\
                                            execute()
        uidsFound = rawUidGetResult.get('values', [])

        if uidsFound:
            for i in range(len(uidsFound)):
                if uid == int(uidsFound[i]):
                    return i

        # No UIDs representing this UID found in this table.
        return None

    def return_part_info(self, uid):
        rowNumToUse = self._uid_to_row_number(uid)

        if not rowNumToUse:
            return None

        SPREADSHEET_PART_INFO_RANGE = SPREADSHEET_RANGE_PREFIX + \
                                      str(rowNumToUse) + ":" + "E" + str(rowNumToUse)

        rawPartInfoGetResult = self._sheets_service.spreadsheets().values().get(
                                            spreadsheetId=SPREADSHEET_ID,
                                            range=SPREADSHEET_PART_INFO_RANGE).\
                                            execute()
        partInfoArray = rawPartInfoGetResult.get('values', [])

        if len(partInfoArray) >= 5:
            return UidSheetInfoModifier.PartInfo(partInfoArray[0],
                                            partInfoArray[1], partInfoArray[2],
                                            partInfoArray[3], partInfoArray[4])
        else:
            return None