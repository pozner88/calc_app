import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from fastapi.testclient import TestClient
from database import get_db, Base
from config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST

DATABASE_URL_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
engine_test = create_engine(DATABASE_URL_TEST)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.bind = engine_test


def override_get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_right_value(db):
    response = client.post('/calc/rightValue', params={'right_value': 2.2})
    assert response.status_code == 200
    assert response.json() == {"right_value": 2.2}


def test_get_left_value(db):
    response = client.post('/calc/leftValue', params={'left_value': 2})
    assert response.status_code == 200
    assert response.json() == {"left_value": 2}


def test_get_operation(db):
    response = client.post('calc/operation', params={'operation': '*'})
    assert response.status_code == 200
    assert response.json() == {'operation': '*'}


def test_get_result(db):
    response = client.get('calc/getResult')
    assert response.status_code == 200
    assert response.json() == {"left_value": 2.0, "right_value": 2.2, "operation": "*", "result": 4.4}


def test_get_history(db):
    response = client.get('calc/history')
    assert response.status_code == 200
    assert response.json() == [{"left_value": 2.0, "right_value": 2.2, "operation": "*", "result": 4.4}]
