import psycopg2
from resources.db_creds import PostgresCreds



def get_db_info():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=PostgresCreds.HOST,
            port=PostgresCreds.PORT,
            dbname=PostgresCreds.DATABASE,
            user=PostgresCreds.USERNAME,
            password=PostgresCreds.PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print(f'Подключено к PostgreSQL: {version[0]}')

    except Exception as e:
        print('Ошибка при работе с PostgreSQL: ', e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    get_db_info()