from fastapi.exceptions import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
from starlette import status

load_dotenv()
DATABASE_CONN = os.getenv("ASYNC_DATABASE_URL")
print("database_conn: ", DATABASE_CONN)

# 비동기 SQLAlchemy 엔진 생성 (pool 재사용 설정 포함)
engine = create_async_engine(DATABASE_CONN, echo=True,
                             pool_size=10, max_overflow=0,
                             pool_recycle=300  
                             )

# 비동기 세션을 생성하기 위한 sessionmaker 설정
SessionLocal = async_sessionmaker(engine)

# 베이스 클래스 생성 (ORM 모델 정의용)
class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="요청하신 서비스가 잠시 내부적으로 문제가 발생하였습니다."
            )
        finally:
            if db:
                await db.close()