import configparser
import xmlrpc.client
import random
import json
import urllib.request
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

service_run_time=int(config_file['background']['service_run_time'])

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


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url_json = "%s/jsonrpc" % (odoo_url)
uid_json = call(url_json, "common", "login", odoo_db, odoo_username, odoo_password)