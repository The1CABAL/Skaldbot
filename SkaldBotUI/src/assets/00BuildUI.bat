@echo off
TITLE Running cmds
taskkill /IM cmd.exe
call 01VueCli
call 02VueCliService
call 03BuildUI
