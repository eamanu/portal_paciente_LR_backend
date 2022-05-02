FROM python:3.9
# Use Debian

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./templates/ ./code/templates/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install mysqlclient

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
