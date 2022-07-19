import os
import xlrd
from xlwt import Workbook


xl_loc = 'fa_trans.xls'
text_loc = 'fa_trans_sql.txt'  # redacted file path

wb = xlrd.open_workbook(xl_loc)
sheet = wb.sheet_by_index(0)
wbk = Workbook()

sql_sheet = wbk.add_sheet('SQLs')

row = 0
cumulative_row = 1

max_row_idx = -1


def go_back_add_sql(start_idx, end_idx, skip_idx):
    with open(text_loc, 'a') as txt_file:
        for i in range(start_idx, end_idx):
            if i == skip_idx:
                pass
            else:
                txt_file.write(f"delete from fa_trans where unique_key = {int(sheet.cell_value(i, 3))};\n")


if os.path.exists(text_loc) and os.path.isfile(text_loc):
    os.remove(text_loc)

while row < sheet.nrows and cumulative_row <= sheet.nrows:
    cur_row = sheet.cell_value(row, 0)
    next_row = sheet.cell_value(cumulative_row, 0)

    print('cur_row is', cur_row)
    print('next row is', next_row)

    while sheet.cell_value(row, 0) == sheet.cell_value(cumulative_row, 0):
        print('row is', row)
        print('cumulative row is', cumulative_row)
        if sheet.cell_value(row, 3) > sheet.cell_value(cumulative_row, 3):
            max_row_idx = row
        else:
            max_row_idx = cumulative_row

        cumulative_row += 1

    go_back_add_sql(row, cumulative_row, max_row_idx)

    row = cumulative_row
    cumulative_row += 1
