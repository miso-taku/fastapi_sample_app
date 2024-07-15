from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

# # DB接続用のエンジンを作成
# db_engine = create_engine(DB_URL, echo=True)
# db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# 非同期DB接続用のエンジンを作成
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()

# DB接続用のセッションを取得する関数
# def get_db():
#     with db_session() as session:
#         yield session
async def get_db():
    async with async_session() as session:
        yield session