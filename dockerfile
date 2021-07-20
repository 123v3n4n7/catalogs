FROM python:3.8-slim-buster
WORKDIR /docker
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
RUN pip3 install -r requirements.txt

COPY . .
RUN ["chmod", "+x", "/docker/entrypoint.sh"]
ENTRYPOINT ["sh","./entrypoint.sh"]