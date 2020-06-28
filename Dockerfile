FROM python:3.7
WORKDIR /SkaldBot

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "SkaldBot/SkaldBot.py"]