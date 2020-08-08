FROM python:3.7
ADD . ./SkaldBotUI
WORKDIR /SkaldBotUI
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ/etc/localtime && echo %TZ > /etc/timezone
RUN	apt-get update && \
	apt install --assume-yes nodejs npm && \
	npm install -g @vue/cli && \
	npm install -g @vue/cli-service && \
	npm install -g serve &&\
	npm audit fix && \
	npm run build

EXPOSE 5478
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["serve", "- s ./dist"]