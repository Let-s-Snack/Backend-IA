import unittest
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class TestConnections(unittest.TestCase):
    def test_database(self):
        try:
            cnxn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_DATABASE1'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PWD'),
                port=os.getenv('DB_PORT')
            )
            self.assertIsNotNone(cnxn)
            cnxn.close()
            print("✔️  SQL database connection success!")
        except Exception as e:
            self.fail(f"❌  Failed to connect to SQL database: {e}")
    
if __name__ == "__main__":
    unittest.main()