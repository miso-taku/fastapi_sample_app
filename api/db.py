from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

# 非同期DB接続用のエンジンを作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()

# DB接続用のセッションを取得する関数
async def get_db():
    async with async_session() as session:
        yield session