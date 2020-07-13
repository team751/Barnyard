
import gspread
import uuid

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
MAIN_SPREADSHEET_KEY = "1zRSYqFLEEHLTDiMwv_tjmZ2aUK3V4LZ9E4OVBDFX_OI"
NEW_BOM_SHEET = [["Date", "UUID", "Name", "Item Name", "Price per Item", "#", "Price total", "Robot?", "Exempt?",
                  "Owned?", "Link", "Status", "Shipping", "Tax", "Notes", ""]]

CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", SCOPES)


def add_part(name, description, location, image_url, component_group, sheets=None):
    if sheets is None:
        sheets = gspread.authorize(CREDENTIALS)

    part_info_sheet = sheets.open_by_key(MAIN_SPREADSHEET_KEY).worksheet(get_setting("Part Sheet Name"))

    temp_uuid = "tempuuid-" + str(uuid.uuid4())
    uids_found = len(part_info_sheet.col_values(1))

    part_info_sheet.update_cell(uids_found + 1, 1,
                                temp_uuid)
    part_info_sheet.update_cell(uids_found + 1, 2,
                                name)
    part_info_sheet.update_cell(uids_found + 1, 3,
                                description)
    part_info_sheet.update_cell(uids_found + 1, 4,
                                location)
    part_info_sheet.update_cell(uids_found + 1, 5,
                                image_url)
    part_info_sheet.update_cell(uids_found + 1, 6,
                                component_group)

    return temp_uuid


def add_part_bom(name, description, location, image_url, component_group,
                 price, quantity, on_robot, exempt, asap, order_link):
    print("Adding part...")

    bom_sheet_key = get_setting("BOM Sheet Key")
    credentials = ServiceAccountCredentials. \
        from_json_keyfile_name("client_secret.json", SCOPES)
    sheets = gspread.authorize(credentials)
    temp_uuid = add_part(name, description, location, image_url, component_group, sheets)

    if bom_sheet_key[0].lower().startswith("https://"):
        bom_sheet = sheets.open_by_url(bom_sheet_key[0])
    else:
        bom_sheet = sheets.open_by_key(bom_sheet_key[0])

    try:
        component_worksheet = bom_sheet.worksheet(component_group)
    except gspread.WorksheetNotFound:
        component_worksheet = bom_sheet.add_worksheet(title=component_group, rows=1000, cols=26)

        if len(NEW_BOM_SHEET) > 0:
            cells = []

            for r in range(len(NEW_BOM_SHEET)):
                cells.append([])

                for c in range(len(NEW_BOM_SHEET[0])):
                    cells[r].append(NEW_BOM_SHEET[r][c])

            component_worksheet.update("", cells)

    row_num = len(NEW_BOM_SHEET) + 1

    if asap:
        status = get_setting("ASAP Status Name")
    else:
        status = get_setting("Requested Status Name")

    component_worksheet.update_cell(row_num, 1, str(datetime.now()))
    component_worksheet.update_cell(row_num, 2, temp_uuid)
    component_worksheet.update_cell(row_num, 3, "TEMP")
    component_worksheet.update_cell(row_num, 4, name)
    component_worksheet.update_cell(row_num, 5, str(price))
    component_worksheet.update_cell(row_num, 6, str(quantity))
    component_worksheet.update_cell(row_num, 7, str(price * quantity))
    component_worksheet.update_cell(row_num, 8, str(on_robot))
    component_worksheet.update_cell(row_num, 9, str(exempt))
    component_worksheet.update_cell(row_num, 10, str(False))
    component_worksheet.update_cell(row_num, 11, order_link)
    component_worksheet.update_cell(row_num, 12, status[0])


def get_component_groups():
    GROUPS = ()

    for component_group in get_setting("Component Group Names"):
        GROUPS += ((component_group, component_group),)

    return GROUPS


def get_parts(parts_limit: int = -1):
    sheets = gspread.authorize(CREDENTIALS)
    return_value = []

    part_info_sheet = sheets.open_by_key(MAIN_SPREADSHEET_KEY).worksheet(get_setting("Part Sheet Name"))

    if parts_limit < 0:
        part_values = part_info_sheet.get_all_values()
    else:
        part_values = part_info_sheet.get("A2:F" + str(parts_limit))

    for part_value in part_values:
        if parts_limit >= 0 or part_value >= parts_limit:
            break
        elif part_value[1].lower() == "Name":
            continue

        return_value.append({
            "uuid": part_value[0],
            "name": part_value[1],
            "description": part_value[2],
            "location": part_value[3],
            "image_url": part_value[4],
            "component_group": part_value[5]
        })

    return return_value


def get_setting(setting_name):
    sheets = gspread.authorize(CREDENTIALS)

    settings_sheet = sheets.open_by_key(MAIN_SPREADSHEET_KEY).worksheet("Barnyarditricins only")
    settings = settings_sheet.row_values(1)
    setting_row = 0

    for i in range(len(settings)):
        if settings[i].lower() == setting_name.lower():
            setting_row = i
            break

    setting_data = settings_sheet.col_values(setting_row + 1)

    for i in range(len(setting_data)):
        if setting_data[i].lower() == setting_name.lower():
            setting_data.remove(setting_name)
            break

    return setting_data
