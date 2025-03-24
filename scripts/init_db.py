import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from models.student import Student

# Load environment variables
load_dotenv()
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

# Create synchronous engine and session
sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(bind=sync_engine)

def initialize_database():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)

    with SyncSessionLocal() as session:
        student1 = Student(name="Jerin", age=27, grade="Fifth")
        student2 = Student(name="Anita", age=24, grade="Fourth")
        student3 = Student(name="Jefin", age=21, grade="Third")

        session.add_all([student1, student2, student3])
        session.commit()

    print("✅ DB 초기화 및 테스트 데이터 삽입 완료!")