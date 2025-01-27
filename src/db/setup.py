from sqlmodel import SQLModel, create_engine

mysql_file_name = "database.db"
mysql_url = "mysql+pymysql://127.0.0.1:3306/cat_market_py?user=root&password=123456"

engine = create_engine(mysql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

