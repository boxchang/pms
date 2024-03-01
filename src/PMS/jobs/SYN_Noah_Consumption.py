import datetime
import sys
import os

import xlwt

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from PMS.database import database, dc_database, sqlite_database
from jobs.func import get_ip

class SYN_Noah_Consumption(object):
    db = None
    PROD = False
    DC_SCHEMA = None
    WMS_SCHEMA = None
    IP = None

    def __init__(self, PROD):
        self.IP = get_ip()
        self.PROD = PROD
        if PROD:
            self.DC_SCHEMA = "DC.dbo"
            self.WMS_SCHEMA = "WMS2.dbo"
        else:
            self.DC_SCHEMA = "DC_Dev.dbo"
            self.WMS_SCHEMA = "WMS2_Dev.dbo"
        self.db = database()

    def get_batch_no(self):
        now = datetime.datetime.now()
        batch_no = now.strftime("%y%m%d%H%M%S")
        return batch_no

    def get_latest_series(self):
        last_s = ""
        db = sqlite_database()
        sql = "select series_no from production_sync_sap_series where function = 'consumption'"
        series = db.select_sqlite_dict(sql)
        if series:
            last_s = series[0]["series_no"]
        return last_s

    def export_records(self, last_s):
        db = sqlite_database()
        sql = "select * from production_record where id > {last_s}".format(last_s=last_s)
        records = db.select_sqlite_dict(sql)
        return records

    def update_sap_series(self, last_s):
        db = sqlite_database()
        sql = """update production_sync_sap_series set series_no={series} where function='consumption'""".format(series=last_s)
        db.execute_sqlite_sql(sql)


    def create_dc_data(self, records, batch_no):
        series = ""
        db = dc_database(self.PROD)
        for record in records:
            sql = """insert into {dc_schema}.SYN_Noah_Consumption(wo_no, cfm_code, item_no, record_id, 
                     qty, batch_no, create_by, create_at) 
                     values('{wo_no}', '{cfm_code}', '{item_no}', {record_id}, {qty}, 
                     '{create_by}', GETDATE())"""\
                .format(wo_no=record['wo_no'], cfm_code=record['cfm_code'], item_no=record['item_no'],
                        record_id=record['id'], qty=record['qty'],
                        batch_no=batch_no, create_by=self.IP, dc_schema=self.DC_SCHEMA)
            print(sql)
            db.execute_sql(sql)
            series = record['id']
        return series

    def prod_sap_file(self, batch_no):
        today = datetime.datetime.now().strftime("%Y%m%d")
        file_name = "Consumption_{today}_{batch_no}.xls".format(today=today, batch_no=batch_no)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Confirmation')
        ws.col(0).width = 256 * 20
        ws.col(1).width = 256 * 20
        ws.col(2).width = 256 * 20
        ws.col(3).width = 256 * 20
        ws.col(4).width = 256 * 20

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['order_no', 'cfm_code', 'material', 'x_id', 'qty']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        db = dc_database(self.PROD)
        sql = "select * from {dc_schema}.SYN_Noah_Consumption where batch_no='{batch_no}'".format(batch_no=batch_no, dc_schema=self.DC_SCHEMA)
        records = db.select_sql_dict(sql)

        for record in records:
            row_num += 1
            ws.write(row_num, 0, record['wo_no'], font_style)  # 生產工單
            ws.write(row_num, 1, record['cfm_code'], font_style)  # 確認單
            ws.write(row_num, 2, record['item_no'], font_style)  # 料號
            ws.write(row_num, 3, record['record_id'], font_style)  # Record ID
            ws.write(row_num, 4, record['qty'], font_style)  # Setting Time
        wb.save(file_name)

    def save_log(self, batch_no, start_s, end_s):
        db = sqlite_database()
        sql = """insert into production_sync_sap_log(function,batch_no,from_series_no,to_series_no,create_by) 
                 values('{function}', '{batch_no}', {from_series_no}, {to_series_no}, '{create_by}')"""\
                 .format(function='consumption', batch_no=batch_no, from_series_no=start_s, to_series_no=end_s, create_by=self.IP)
        db.execute_sqlite_sql(sql)

    def execute(self):
        start_s = self.get_latest_series()
        records = self.export_records(start_s)
        batch_no = self.get_batch_no()
        end_s = self.create_dc_data(records, batch_no)
        if end_s:
            self.update_sap_series(end_s)
            self.prod_sap_file(batch_no)
            self.save_log(batch_no, start_s, end_s)

wh = SYN_Noah_Consumption(False)
wh.execute()