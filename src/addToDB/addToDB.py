import csv
import sqlalchemy as db 
import psycopg2
import os

print(os.getcwd())


from dbInformation.dbinfo import db_info
import pandas as pd

def loadAndInsertIntoDatabase():
  url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
  engine = db.create_engine('postgresql+psycopg2://' + url )      

  # read in all 3 data sets as a list
  df = pd.read_csv('./src/data/dataWithCurrencyVer002.csv')

  # print(df.columns)

  with engine.connect() as connection: 
    # iterate through each row in our data list
    try:
      for row in df.itertuples():

        # read in created csv_file and convert to dataframe, read in dataframe

        sql_stmt = """
        INSERT INTO watchdata (listing_statPrice, product_subtitle, Model, Box, Papers, Age, Movement, ConditionGrade, CaseSize, Case_, Dial, Bracelet, LOT, Location, Seller)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        #execute query
        connection.execute(sql_stmt, row.listing__statPrice, row.product_subtitle, row.Model, row.Box, row.Papers, row.Age, row.Movement,
                           row.ConditionGrade, row.CaseSize, row.Case, row.Dial, row.Bracelet, row.LOT, row.Location,  row.Seller)

    # handle any errors with communication to database
    except (Exception, psycopg2.Error) as err:
        print("Error while interacting with PostgreSQL...\n", err)

if __name__ == '__main__':
  loadAndInsertIntoDatabase()