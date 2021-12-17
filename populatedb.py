import psycopg2
import datetime
import pytz
import time

def run():
   #establishing the connection
   conn = psycopg2.connect(
      database="sos_infer_db", user='root', password='linkeradmin123', host='127.0.0.1', port= '5432'
   )
   conn.autocommit = True

   #Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   for i in range(50):
      # Preparing SQL queries to INSERT a record into the database.
      time.sleep(1)
      cursor.execute('''INSERT INTO EVENTS(IP_ADDRESS, TYPE, SENT)
      VALUES ('{}', 0, 0)'''.format(str(datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S'))))

   conn.commit()
   #Closing the connection
   conn.close()

run()