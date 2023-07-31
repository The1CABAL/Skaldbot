FROM python:3.8
ADD . ./SkaldBot
WORKDIR /SkaldBot
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ/etc/localtime && echo %TZ > /etc/timezone
RUN apt-get update && \
	apt-get install --assume-yes ffmpeg

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python", "./SkaldBotCore.py"]
