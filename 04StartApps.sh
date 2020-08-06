#!/bin/bash

exec python3 ./SkaldBot.py & \
exec python3 ./SkaldBotAPI/runserver.py & \
exec npm run build & \
serve -s ./SkaldBotUI/dist