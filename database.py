from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание соединения с базой данных SQLite
engine = create_engine('sqlite:///todo.db', echo=False)

# Создание сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Создание класса базовой модели
Base = declarative_base()
