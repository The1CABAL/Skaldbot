FROM python:3.7
ADD . ./SkaldBotAPI
WORKDIR /SkaldBotAPI
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ/etc/localtime && echo %TZ > /etc/timezone

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python", "./runserver.py"]