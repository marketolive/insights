FROM ubuntu:latest
WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential libpq-dev
RUN pip3 install debugpy

COPY requirements.txt /app
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3"]
CMD ["/app/run.py"]