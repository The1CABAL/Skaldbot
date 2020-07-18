#!/bin/bash

sqlpackage /Action:Publish /SourceFile:"/var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/bin/Debug/SkaldBot.Database.dacpac", /Profile:"/var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/Profiles/SkaldBot.Database.publish"