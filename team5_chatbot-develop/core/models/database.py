from sqlmodel import create_engine, SQLModel
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

database_url = config.get('sqlite', 'DATABASE_URL')
connect_args = { 'check_same_thread': False }

engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
