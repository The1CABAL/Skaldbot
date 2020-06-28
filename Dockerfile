FROM python3.7
WORKDIR /SkaldBot

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r SkaldBot/requirements.txt
CMD ["python", "SkaldBot/SkaldBot.py"]