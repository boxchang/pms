import datetime
import xlwt
from django.http import HttpResponse
from PMS.settings.base import MEDIA_ROOT
from PMS.database import dc_database, database
from bases.utils import get_ip
from production.models import Consumption, Sync_SAP_Log, Record

class sap_record_sync(object):
    db = None
    PROD = False
    DC_SCHEMA = None
    WMS_SCHEMA = None
    IP = None

    def __init__(self, PROD):
        self.IP = get_ip()
        self.PROD = PROD
        self.db = database()

    def export_records(self, plant):
        records = Record.objects.filter(plant=plant, sap_flag=False)
        return records

    def export_consumptions(self, plant):
        records = Consumption.objects.filter(plant=plant, sap_flag=False)
        return records

    def get_batch_no(self):
        now = datetime.datetime.now()
        batch_no = now.strftime("%y%m%d%H%M%S")
        return batch_no

    def create_dc_workhour_data(self, records, batch_no):
        db = dc_database()
        amount = 0
        for record in records:
            tmp_record_dt = record.record_dt.split('-')
            tmp_record_dt = tmp_record_dt[2] + tmp_record_dt[1] + tmp_record_dt[0]
            tmp_status = 'X' if record.status == None else ''

            sql = """insert into SYN_Noah_WorkHour(wo_no, cfm_code, item_no, record_id, 
                             setting_time, mach_time, labor_time, emp_no, record_dt, good_qty, ng_qty, comment,
                             status, batch_no, create_by, create_at) 
                             values('{wo_no}', '{cfm_code}', '{item_no}', '{record_id}', {setting_time}, 
                             {mach_time}, {labor_time}, '{emp_no}', '{record_dt}', {good_qty}, {ng_qty},
                             '{comment}', '{status}', '{batch_no}', '{create_by}', GETDATE())""" \
                .format(wo_no=record.wo_no, cfm_code=record.cfm_code, item_no=record.item_no,
                        record_id=record.id, setting_time=0, mach_time=record.mach_time,
                        labor_time=record.labor_time,
                        emp_no=record.sap_emp_no, record_dt=tmp_record_dt, good_qty=record.good_qty,
                        ng_qty=record.ng_qty, comment=record.comment, status=tmp_status,
                        batch_no=batch_no, create_by=self.IP)
            try:
                db.execute_sql(sql)

                # 成功塞到中介就將Flag改成True
                record.sap_flag = True
                record.save()

                amount += 1
            except Exception as e:
                print(e)
                print(sql)
        return amount

    def create_dc_consumption_data(self, records, batch_no):
        db = dc_database()
        amount = 0
        for record in records:
            sql = """insert into SYN_Noah_Consumption(wo_no, cfm_code, item_no, record_id, 
                             qty, batch_no, create_by, create_at) 
                             values('{wo_no}', '{cfm_code}', '{item_no}', '{record_id}', {qty}, {batch_no},
                             '{create_by}', GETDATE())""" \
                .format(wo_no=record.wo_no, cfm_code=record.cfm_code, item_no=record.item_no,
                        record_id=record.id, qty=record.qty,
                        batch_no=batch_no, create_by=self.IP)
            try:
                db.execute_sql(sql)

                # 成功塞到中介就將Flag改成True
                record.sap_flag = True
                record.save()

                amount += 1
            except Exception as e:
                print(e)
                print(sql)
        return amount

    def get_dc_workhour_data(self, batch_no):
        db = dc_database()
        sql = "select * from SYN_Noah_WorkHour where batch_no='{batch_no}'".format(dc_schema=self.DC_SCHEMA, batch_no=batch_no)
        records = db.select_sql_dict(sql)
        return records

    def get_dc_consumption_data(self, batch_no):
        db = dc_database()
        sql = "select * from SYN_Noah_Consumption where batch_no='{batch_no}'".format(dc_schema=self.DC_SCHEMA, batch_no=batch_no)
        records = db.select_sql_dict(sql)
        return records

    def save_log(self, func, batch_no, amount, create_by, file_name):
        Sync_SAP_Log.objects.create(function=func, batch_no=batch_no, amount=amount, create_by=create_by, file_name=file_name)

    def prod_sap_workhour_excel(self, file_name, batch_no):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = "attachment; filename={file_name}".format(file_name=file_name)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Confirmation')
        ws.col(0).width = 256 * 20
        ws.col(1).width = 256 * 20
        ws.col(2).width = 256 * 20
        ws.col(3).width = 256 * 20
        ws.col(4).width = 256 * 20
        ws.col(5).width = 256 * 20
        ws.col(6).width = 256 * 20
        ws.col(7).width = 256 * 20
        ws.col(8).width = 256 * 20
        ws.col(9).width = 256 * 20
        ws.col(10).width = 256 * 20

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['afrud_pernr', 'afrud_budat', 'afrud_aufnr', 'afrud_rueck', 'caufvd_matnr',
                   'afrud_ism01', 'afrud_ism02', 'afrud_ism03', 'Yield to Confirm', 'Scrap to Confirm', 'ConfText']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        records = self.get_dc_workhour_data(batch_no)

        for record in records:
            row_num += 1
            ws.write(row_num, 0, record['emp_no'], font_style)  # SAP員編
            ws.write(row_num, 1, record['record_dt'], font_style)  # 工作執行日
            ws.write(row_num, 2, record['wo_no'], font_style)  # 生產工單
            ws.write(row_num, 3, record['cfm_code'], font_style)  # 確認單
            ws.write(row_num, 4, record['item_no'], font_style)  # 料號
            ws.write(row_num, 5, "0", font_style)  # setting time
            ws.write(row_num, 6, record['mach_time'], font_style)  # machine time
            ws.write(row_num, 7, record['labor_time'], font_style)  # labor time
            ws.write(row_num, 8, record['good_qty'], font_style)  # Yield to Confirm
            ws.write(row_num, 9, record['ng_qty'], font_style)  # Scrap to Confirm
            ws.write(row_num, 10, record['comment'], font_style)  # ConfText
        wb.save(MEDIA_ROOT+'sync_sap_excel\\'+file_name)  # 儲存一份在主機上
        wb.save(response)
        return response

    def prod_sap_consumption_excel(self, file_name, batch_no):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = "attachment; filename={file_name}".format(file_name=file_name)

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

        records = self.get_dc_consumption_data(batch_no)

        for record in records:
            row_num += 1
            ws.write(row_num, 0, record['wo_no'], font_style)  # 生產工單
            ws.write(row_num, 1, record['cfm_code'], font_style)  # 確認單
            ws.write(row_num, 2, record['item_no'], font_style)  # 料號
            ws.write(row_num, 3, record['record_id'], font_style)  # Record ID
            ws.write(row_num, 4, record['qty'], font_style)  # Setting Time
        wb.save(MEDIA_ROOT + 'sync_sap_excel\\' + file_name)  # 儲存一份在主機上
        wb.save(response)
        return response