FROM python:3.7
ADD . ./SkaldBot
WORKDIR /SkaldBot
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ/etc/localtime && echo %TZ > /etc/timezone
RUN apt-get update && \
	apt-get install --assume-yes ffmpeg && \
	apt-get install --assume-yes nodejs npm && \
	npm install -g @vue/cli && \
	npm install -g serve

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python", "./SkaldBot.py"]
