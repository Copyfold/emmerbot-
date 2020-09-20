FROM python:latest

RUN pip3 install discord.py

WORKDIR /bot
COPY . /bot

ENTRYPOINT python3 bot.py
