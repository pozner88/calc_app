FROM python:3.10

RUN mkdir /calc_api

WORKDIR /calc_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000