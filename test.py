from connect import auth

con = auth()

cur = con.cursor()

cur.execute('SELECT * FROM "INVENTORY"')

inventory = cur.fetchall()

for i in inventory:
    print(i[4])

print(inventory)

con.close()

<body class="bg-blue-100 flex flex-col items-center justify-center min-h-screen text-center p-6"
      style="background-image: url('static/logo_background.jpg'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;">
