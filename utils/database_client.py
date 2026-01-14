import psycopg2
import logging

class DatabaseClient:
    def __init__(self, host, database, user, password, port=5432):
        self.connection = None
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.logger.info("Successfully connected to database")
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Execute SQL query and return results"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")