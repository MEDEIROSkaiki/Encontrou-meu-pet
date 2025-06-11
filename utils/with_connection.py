from db import get_connection

def with_connection(func):
    def wrapper(*args, **kwargs):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            result = func(cursor, *args, **kwargs)
            conn.commit()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            raise Exception(f"Erro de banco: {e}")
    return wrapper
