import pymysql

class Database:
    def __init__(self, host='193.112.82.102', user='camera_lens', password='gx19930804', db='camera_lens'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conn = None

    def connect(self):
        if not self.conn:
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db,
                    cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的数据
                )
                print("Database connection established.")
            except pymysql.MySQLError as e:
                print(f"Error connecting to database: {e}")
                raise
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")

    def execute(self, query, params=None):
        """Execute a SQL query."""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            return False

    def fetchone(self, query, params=None):
        """Fetch one result from a SQL query."""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
            return None

    def fetchall(self, query, params=None):
        """Fetch all results from a SQL query."""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
            return None


# 创建一个全局数据库连接实例
db = Database()
