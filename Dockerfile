FROM python:3.8.2-buster-slim

ENV TZ=Europe/Brussels
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/datamonitoring datamonitoring

ENTRYPOINT ["python", "-m", "datamonitoring"]