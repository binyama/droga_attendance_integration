import configparser
import xmlrpc.client
from datetime import datetime
import psycopg2

# CREATE OBJECT
config_file = configparser.ConfigParser()

# READ CONFIG FILE
config_file.read("setting.ini")

# odoo configuration
odoo_url = config_file['odoo']['odoo_url']
odoo_username = config_file['odoo']['odoo_username']
odoo_password = config_file['odoo']['odoo_password']
odoo_db = config_file['odoo']['odoo_db']

# attendance configuration
attendance_url = config_file['attendance']['attendance_url']
attendance_username = config_file['attendance']['attendance_username']
attendance_password = config_file['attendance']['attendance_password']
attendance_db = config_file['attendance']['attendance_db']
attendance_port = config_file['attendance']['attendance_port']

service_run_time=config_file['background']['service_run_time']

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))

uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

# postgress database

# connection
conn = psycopg2.connect(database=attendance_db,
                        host=attendance_url,
                        user=attendance_username,
                        password=attendance_password,
                        port=attendance_port)
