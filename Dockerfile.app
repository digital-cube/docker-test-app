FROM python:3.11.4

WORKDIR /app

COPY app /app

# RUN apt upgrade
# RUN apt update
# RUN apt install postgresql-client -y

RUN pip install --upgrade pip
RUN pip install wheel tornado tortoise-orm asyncpg

ENV PYTHONPATH /app

RUN mkdir /var/log/app
RUN touch /var/log/app/app.log

CMD /usr/local/bin/python /app/app.py
