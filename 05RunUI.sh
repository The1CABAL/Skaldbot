#!/bin/bash

exec python3 ./SkaldBotAPI/runserver.py && \
serve -s ./SkaldBotUI/dist
