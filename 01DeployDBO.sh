#!/bin/bash
cd /var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/bin/Debug
sqlpackage /Action:Publish /SourceFile:"SkaldBot.Database.dacpac" /Profile:"/var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/Profiles/SkaldBot.Database.publish.xml"