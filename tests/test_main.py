import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import starlette.status

from api.db import get_db, Base
from api.main import app


ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    # デスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用のDBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session
    
    app.dependency_overrides[get_db] = get_test_db
    
    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/tasks", json={"title": "test task"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test task"

    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "test task"
    assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "test task 2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test task 2"

    # 完了フラグを立てる
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 既に完了フラグが立っているので、400を返却
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # 完了フラグを外す
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 既に完了フラグが外れているので、404を返却
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_param, exception", 
    [
        ("2023-12-31", starlette.status.HTTP_200_OK), 
        ("2023-12-32", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY)
    ],
)
async def test_due_date(async_client, input_param, exception):
    response = await async_client.post("/tasks", json={"title": "test task 3", "due_date": input_param})
    assert response.status_code == exception