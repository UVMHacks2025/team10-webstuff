import psycopg2

def auth():
    hostname = 'rallycat.cgv8ogeaqps7.us-east-1.rds.amazonaws.com'
    database = 'postgres'
    username = 'postgres'
    pwd = 'hackathon'
    port_id = 5432

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username, 
            password = pwd,
            port = port_id)
        # conn.close()
    except Exception as error:
        print(error)
    
    return conn

