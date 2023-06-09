# -*- coding: utf-8 -*-
"""
Matej_Višnjić
Projekt iz sustava poslovne inteligencije
Kriminal u Bostonu
"""

# Imports
import pymysql 
import pandas as pd
import numpy as np
import json
import requests
import random
from sqlalchemy import create_engine

CSV_FILE_PATH = r"C:\Users\Matej\Documents\fax\4.SEMESTAR\SUSTAVI POSLOVNE INTELIGENCIJE\PROJEKT\archive\crime.csv"
df = pd.read_csv(CSV_FILE_PATH, delimiter=',', encoding='latin-1')
df[['SHOOTING']] = df[['SHOOTING']].fillna('N')
df[['DISTRICT']] = df[['DISTRICT']].fillna('N')
df[['STREET']] = df[['STREET']].fillna('N')
print("CSV size:", df.shape)

print (df.head())


#Konekcija na bazu
user = 'root'
pasw = '1234'
host = 'localhost'
port = 3306
database = 'crimes'

mydb = create_engine('mysql+pymysql://' + user + ':' + pasw + '@' +host+ ':' +str(port)+ '/' +database, echo = False)
print(mydb)
connection = mydb.connect()

#CREATE DATABASE
create_crimes = "CREATE DATABASE crimes;"
connection.execute(create_crimes)

#DDL
district_ddl = "CREATE TABLE crimes.district (id INT NOT NULL PRIMARY KEY, name VARCHAR(100), UNIQUE INDEX id_UNIQUE (id ASC));"
connection.execute(district_ddl)
street_ddl = "CREATE TABLE crimes.street (id INT NOT NULL PRIMARY KEY, name VARCHAR(100), UNIQUE INDEX id_UNIQUE (id ASC));"
connection.execute(street_ddl)
ucr_part_ddl = "CREATE TABLE crimes.ucr_part (id INT NOT NULL PRIMARY KEY, name VARCHAR(100), UNIQUE INDEX id_UNIQUE(id ASC));"
connection.execute(ucr_part_ddl)
location_ddl = "CREATE TABLE crimes.location (id INT NOT NULL PRIMARY KEY, coordinates VARCHAR(100), street_fk INT,UNIQUE INDEX id_UNIQUE(id ASC), CONSTRAINT street_id FOREIGN KEY (street_fk) REFERENCES crimes.street(id) ON DELETE NO ACTION ON UPDATE CASCADE);"
connection.execute(location_ddl)
police_station_ddl = "CREATE TABLE crimes.police_station (id INT NOT NULL PRIMARY KEY, address VARCHAR(150), district_fk INT NOT NULL,UNIQUE INDEX id_UNIQUE(id ASC), CONSTRAINT district_id FOREIGN KEY (district_fk) REFERENCES crimes.district(id) ON DELETE NO ACTION ON UPDATE CASCADE);"
connection.execute(police_station_ddl)
offense_ddl = "CREATE TABLE crimes.offense (id INT NOT NULL PRIMARY KEY, code_group VARCHAR(100), ucr_part_fk INT NOT NULL, UNIQUE INDEX id_UNIQUE(id ASC), CONSTRAINT ucr_part_id FOREIGN KEY (ucr_part_fk) REFERENCES crimes.ucr_part(id) ON DELETE NO ACTION ON UPDATE CASCADE);"
connection.execute(offense_ddl)
crime_ddl = "CREATE TABLE crimes.crime (id INT NOT NULL PRIMARY KEY, occured_on_date DATETIME, day_of_week VARCHAR(45), hour INT, month INT,year INT, crime_description MEDIUMTEXT, shooting VARCHAR(10), offense_fk INT NOT NULL, location_fk INT NOT NULL, police_station_fk INT NOT NULL,UNIQUE INDEX id_UNIQUE(id ASC), CONSTRAINT offense_id FOREIGN KEY (offense_fk) REFERENCES crimes.offense(id) ON DELETE NO ACTION ON UPDATE CASCADE,CONSTRAINT location_id FOREIGN KEY (location_fk) REFERENCES crimes.location(id) ON DELETE NO ACTION ON UPDATE CASCADE,CONSTRAINT police_station_id FOREIGN KEY (police_station_fk) REFERENCES crimes.police_station(id) ON DELETE NO ACTION ON UPDATE CASCADE);"
connection.execute(crime_ddl)

#DROP DATABASE
drop_crimes = "DROP DATABASE crimes;"
connection.execute(drop_crimes)

#DML 
#####
#DISTRICT
district_names = df['DISTRICT']
district_data = pd.DataFrame({'id':list(range(1, len(district_names)+1)), 'name':district_names})
district_data.to_sql(con=mydb, name='district', if_exists='append', index=False)

#UCR_PART
ucrpart_names = df['UCR_PART']
ucrpart_data = pd.DataFrame({'id':list(range(1, len(ucrpart_names)+1)), 'name':ucrpart_names})
ucrpart_data.to_sql(con=mydb, name='ucr_part', if_exists='append', index=False)

#STREET
street_names = df['STREET']
street_data = pd.DataFrame({'id':list(range(1, len(street_names)+1)), 'name':street_names})
street_data.to_sql(con=mydb, name='street', if_exists='append', index=False)

#LOCATION
street_id=[]
for i, row in df.iterrows():
    street_id.append(int(street_data['id'].iloc[i]))
location_data = pd.DataFrame({'id':list(range(1,len(street_id)+1)), 'coordinates': df['Location'], 'street_fk': street_id})
location_data.to_sql(con=mydb, name='location', if_exists='append', index=False)

#POLICE_STATION
# id,address,district_fk
district_id=[]
for i,row in df.iterrows():
    district_id.append(int(district_data['id'].iloc[i]))
policestation_data = pd.DataFrame({'id':list(range(1,len(district_id)+1)), 'district_fk': district_id})
policestation_data.to_sql(con=mydb, name='police_station', if_exists='append', index=False)

#Adrese za svaku stanicu posebno
policestation_A1 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '40 New Sudbury Street Boston, MA 02114' WHERE d.name = 'A1';"
connection.execute(policestation_A1)
policestation_A15 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '40 New Sudbury Street Boston, MA 02114' WHERE d.name = 'A15';" #ista je adresa jer pokrivaju isti okrug
connection.execute(policestation_A15)
policestation_A7 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '69 Paris Street East Boston, MA 02128' WHERE d.name = 'A7';"
connection.execute(policestation_A7)
policestation_B2 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '2400 Washington Street Roxbury, MA 02119' WHERE d.name = 'B2';"
connection.execute(policestation_B2)
policestation_B3 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '1165 Blue Hill Avenue Mattapan, MA 02124' WHERE d.name = 'B3';"
connection.execute(policestation_B3)
policestation_C11 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '40 Gibson Street Dorchester, MA 02122' WHERE d.name = 'C11';"
connection.execute(policestation_C11)
policestation_C6 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '101 West Broadway South Boston, MA 02127' WHERE d.name = 'C6';"
connection.execute(policestation_C6)
policestation_D14 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '301 Washington Street Brighton, MA 02135' WHERE d.name = 'D14';"
connection.execute(policestation_D14)
policestation_D4 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '650 Harrison Avenue Boston, MA 02116' WHERE d.name = 'D4';"
connection.execute(policestation_D4)
policestation_E13 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '3347 Washington Street Jamaica Plain, MA 02130' WHERE d.name = 'E13';"
connection.execute(policestation_E13)
policestation_E18 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '1249 Hyde Park Avenue Hyde Park, MA 02136' WHERE d.name = 'E18';"
connection.execute(policestation_E18)
policestation_E5 = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '1708 Centre Street West Roxbury, MA 02132' WHERE d.name = 'E5';"
connection.execute(policestation_E5)
policestation_N = "UPDATE police_station ps INNER JOIN district d on d.id = ps.district_fk SET ps.address= '' WHERE d.name = 'N';" # ne znamo koja je policijska postaja uzela slučaj...
connection.execute(policestation_N)


#OFFENSE
#id, code_group, ucr_part_fk
ucrpart_id=[]
for i,row in df.iterrows():
    ucrpart_id.append(int(ucrpart_data['id'].iloc[i]))
offense_data = pd.DataFrame({'id':list(range(1,len(ucrpart_id)+1)), 'code_group': df['OFFENSE_CODE_GROUP'], 'ucr_part_fk': ucrpart_id})
offense_data.to_sql(con=mydb, name='offense', if_exists='append', index=False)

#CRIME
#id, occured_on_date, day_of_week, hour, month, year, crime_description, shooting, offense_fk, location_fk, police_station_fk
offense_id, location_id, policestation_id = [], [], []
for i,row in df.iterrows():
    offense_id.append(int(offense_data['id'].iloc[i]))
    location_id.append(int(location_data['id'].iloc[i]))
    policestation_id.append(int(policestation_data['id'].iloc[i]))
crime_data = pd.DataFrame({'id':list(range(1,len(offense_id)+1)), 'occured_on_date': df['OCCURRED_ON_DATE'], 'day_of_week': df['DAY_OF_WEEK'], 'hour': df['HOUR'], 'month': df['MONTH'], 'year': df['YEAR'], 'crime_description': df['OFFENSE_DESCRIPTION'], 'shooting': df['SHOOTING'], 'offense_fk': offense_id, 'location_fk': location_id, 'police_station_fk': policestation_id})
crime_data.to_sql(con=mydb, name='crime', if_exists='append', index=False)    



