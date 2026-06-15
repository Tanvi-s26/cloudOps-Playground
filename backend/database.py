import psycopg2

def test_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="cloudops",
        user="admin",
        password="admin123"
    )

    conn.close()

    return True