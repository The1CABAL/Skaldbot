FROM python:3.7
ADD . ./SkaldBot
COPY ../../jsons/SkaldBotToken.json ~/
WORKDIR /SkaldBot

RUN apt-get update && \
	apt-get install --assume-yes ffmpeg

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python", "./SkaldBot.py"]
