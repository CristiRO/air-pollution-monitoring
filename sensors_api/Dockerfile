FROM python:3.6

RUN easy_install psycopg2

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY /src /app
WORKDIR /app

EXPOSE 80
CMD ["python", "app.py"]
