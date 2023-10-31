FROM python:3-alpine
LABEL authors="Juan Manuel Aidar"

RUN apk update
RUN apk add git
RUN git clone https://github.com/um-computacion-tm/scrabble-2023-jaidar2003.git
WORKDIR /scrabble-2023-jaidar2003
RUN pip install -r requirements.txt

CMD [ "sh", "-c", "coverage run -m unittest && coverage report -m && python -m game.main" ]