import xmlrpc.client
import helper
from datetime import datetime
import psycopg2
import psycopg2.extras
import time
import lxml

def import_attendance():
    try:

        today = datetime.utcnow().strftime("%Y-%m-%d H%:M%:S%")
        today = '2023-07-08'
        cursor = helper.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            "select ap.id,pe.id,pe.emp_code,pe.first_name ,pe.last_name,ap.att_date ,ap.week ,ap.weekday ,ap.clock_in ,ap.in_date ,ap.in_time ,"
            "ap.clock_out,ap.out_date ,ap.out_time ,ap.workday from personnel_employee pe inner join att_payloadparing ap on pe.id=ap.emp_id "
            "where ap.att_date >='" + today + "'")

        records = cursor.fetchall()

        for record in records:
            empid = get_emp_id(record['emp_code'])

            # search empolyee record in odoo
            employee = helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'hr.employee',
                                                'search_read', [[['barcode', '=', empid]]])

            for emp in employee:
                # get odoo employee id
                odoo_emp_id = emp['id']
                attendance_machine_trans_id = record['id']
                clock_in = record['clock_in']
                clock_out = record['clock_out']

                if clock_in is None:
                    clock_in = False
                else:
                    clock_in = clock_in.strftime("%Y-%m-%d %H:%M:%S")

                if clock_out is None:
                    clock_out = False
                else:
                    clock_out = clock_out.strftime("%Y-%m-%d %H:%M:%S")

                # check existing attendance
                attendance = helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'hr.attendance',
                                                      'search_read',
                                                      [[['attendance_machine_trans_id', '=',
                                                         attendance_machine_trans_id]]])

                if len(attendance) == 0:  # insert new record
                    if clock_in is not None and odoo_emp_id != ' ':
                        helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'hr.attendance',
                                                 'create',
                                                 [{'employee_id': odoo_emp_id, 'check_in': clock_in,
                                                   'check_out': clock_out,
                                                   'attendance_machine_trans_id': attendance_machine_trans_id}])
                else:  # update the record
                    if clock_out is not None and odoo_emp_id != ' ':
                        helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'hr.attendance',
                                                 'write', [[attendance.id], {'check_out': clock_out,
                                                                             'attendance_machine_trans_id': attendance_machine_trans_id}])


    except Exception as e:
        print('Error for employee ', record['emp_code'])

def get_emp_id(emp_id):
    if len(emp_id) == 1:
        return 'DP000' + emp_id
    elif len(emp_id) == 2:
        return 'DP00' + emp_id
    elif len(emp_id) == 3:
        return 'DP0' + emp_id
    elif len(emp_id) == 4:
        return 'DP' + emp_id
    else:
        return emp_id

def main():
    while True:
        import_attendance()
        time.sleep(helper.service_run_time)


if __name__ == "__main__":
    main()
