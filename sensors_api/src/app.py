#!/usr/bin/python
import psycopg2
import time
from flask import Flask, jsonify, request, Response
from datetime import datetime


app = Flask(__name__)
conn = None


def connect():
    global conn
    if conn is not None:
        return
    try:
        conn = psycopg2.connect(host="db", user="postgres", password="password")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close():
    global conn
    if conn is not None:
        conn.close()


@app.route('/sign_up', methods=['POST'])
def sign_up():
    global conn
    args = request.args
    user = args.get('username')
    passwd = args.get('password')

    connect()
    cursor = conn.cursor()

    sql_check_username = """ SELECT id FROM "users" WHERE username = %s; """
    cursor.execute(sql_check_username, (user, ))

    if cursor.rowcount == 0:
        sql_insert_new_user = """ INSERT INTO users(username, pass) VALUES(%s, %s); """
        cursor.execute(sql_insert_new_user, (user, passwd,))
        conn.commit()
        cursor.close()
        return "User registered successfully!"
    else:
        conn.commit()
        cursor.close()
        return "Error registering user. Username already exists."


@app.route('/sensor', methods=['POST'])
def register_sensor():
    global conn
    args = request.args
    user = args.get('username')
    passwd = args.get('password')
    sensor_lat = float(args.get('lat'))
    sensor_long = float(args.get('long'))

    connect()
    cursor = conn.cursor()

    sql_check_username = """ SELECT id FROM "users" WHERE username = %s AND pass = %s; """
    cursor.execute(sql_check_username, (user, passwd, ))

    if cursor.rowcount == 1:
        owner_id = cursor.fetchone()[0]
        sql_insert_new_sensor = """ INSERT INTO sensors(owner_id, sensor_lat, sensor_long) VALUES(%s, %s, %s) RETURNING sensor_id;"""
        cursor.execute(sql_insert_new_sensor, (owner_id, sensor_lat, sensor_long, ))
        sensor_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()

        return "Successfully registered a new sensor with id " + str(sensor_id) + "!"
    else:
        conn.commit()
        cursor.close()
        return "Error registering sensor, bad login."


@app.route('/sensor_data', methods=['POST'])
def add_sensor_data():
    global conn
    args = request.args
    measure_type = args.get('type')
    measure_value = float(args.get('value'))
    sensor_id = args.get('sensor_id')

    connect()
    cursor = conn.cursor()

    sql_check_sensor_id = """ SELECT * FROM sensors WHERE sensor_id = %s;"""
    cursor.execute(sql_check_sensor_id, (sensor_id, ))

    if cursor.rowcount == 1:
        sql_insert_new_sensor_data = """ INSERT INTO sensor_data(sensor_id, measure_ts, measure_type, measure_value) VALUES(%s, %s, %s, %s); """
        dt = datetime.now()
        cursor.execute(sql_insert_new_sensor_data, (sensor_id, dt, measure_type, measure_value, ))

        conn.commit()
        cursor.close()
        return "Successfully added data from sensor!"
    else:
        conn.commit()
        cursor.close()
        return "Error registering data from sensor. Sensor not registered!"


if __name__ == '__main__':
    # TODO: temporary fix, replace with ./wait-for-it.sh
    time.sleep(5)
    connect()
    app.run(host="0.0.0.0", debug=False)
