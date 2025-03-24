from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import database
from models.student import Student

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/")
async def show_students(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(Student))  # 모든 Student 레코드 선택
    students = result.scalars().all()           # 결과에서 실제 객체만 추출
    print(students)
    return students