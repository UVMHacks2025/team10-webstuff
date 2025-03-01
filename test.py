from connect import auth

con = auth()

cur = con.cursor()

cur.execute('SELECT * FROM "INVENTORY"')

inventory = cur.fetchall()

for i in inventory:
    print(i[4])

con.close()

