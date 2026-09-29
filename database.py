import psycopg2


# PostgreSQL configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "placement"
DB_USER = "postgres"
DB_PASSWORD = "123"


def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connection