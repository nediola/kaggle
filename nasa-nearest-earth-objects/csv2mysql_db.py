#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import pandas as pd
import mysql.connector

parser = argparse.ArgumentParser(description='Load Neo csv-file to MySQL DataBase')
parser.add_argument('-f', '--file', type=str, default='data/neo_v2.csv', help='.csv file')
parser.add_argument('-u', '--user', type=str, required=True, help='MySQL Server username')
parser.add_argument('-p', '--password', type=str, required=True, help='MySQL Server password')
parser.add_argument('-t', '--tablename', type=str, default='Neo', help='Result MySQL table name')

args = parser.parse_args()
table = args.tablename
db_connection = mysql.connector.connect(user=args.user, password=args.password)
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS NeoDB;")
db_cursor.execute("USE NeoDB;")
db_cursor.execute(f"DROP TABLE IF EXISTS {table}")

db_cursor.execute(
    f"CREATE TABLE {table}(\
     id INT, \
     name VARCHAR(1000), \
     est_diameter_min FLOAT, \
     est_diameter_max FLOAT, \
     relative_velocity FLOAT, \
     miss_distance FLOAT, \
     orbiting_body VARCHAR(1000), \
     sentry_object BOOLEAN, \
     absolute_magnitude FLOAT, \
     hazardous BOOLEAN);"
)

df = pd.read_csv(args.file)
df.name = '"' + df.name + '"'
df.orbiting_body = '"' + df.orbiting_body + '"'
tuples = list(df.itertuples(index=False, name=None))
tuples_string = ",".join(["(" + ",".join([str(w) for w in t]) + ")" for t in tuples])

db_cursor.execute(
    f"INSERT INTO {table} (\
     id, \
     name, \
     est_diameter_min, \
     est_diameter_max, \
     relative_velocity, \
     miss_distance, \
     orbiting_body, \
     sentry_object, \
     absolute_magnitude, \
     hazardous) VALUES " + tuples_string + ";")
db_cursor.execute("FLUSH TABLES;")
