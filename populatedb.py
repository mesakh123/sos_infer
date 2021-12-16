import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="dev", user='root', password='linkernetworks123', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

for i in range(3000):
    # Preparing SQL queries to INSERT a record into the database.
    cursor.execute('''INSERT INTO EVENTS(IP_ADDRESS, TYPE, SENT)
     VALUES ('{{i}}', 0, 0)''')

conn.commit()
#Closing the connection
conn.close()