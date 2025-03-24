from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class Student(Base):
    __tablename__ = 'student'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    age: Mapped[int] = mapped_column(Integer)
    grade: Mapped[str] = mapped_column(String, nullable=False)