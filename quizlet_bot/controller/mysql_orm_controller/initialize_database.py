# Retry mechanism for database connection
import time

from sqlalchemy import Engine


def initialize_database(engine : Engine):
    retries = 5
    for i in range(retries):
        try:
            with engine.connect() as connection:
                print("Connected to the database!")
                break
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            time.sleep(5)
    else:
        raise Exception("Failed to connect to the database after multiple retries.")