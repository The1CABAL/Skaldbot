#!/bin/bash
chmod a+x /home/ib-2020/sqlpackage/sqlpackage
source /home/ib-2020/.bashrc
cd /var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/bin/Debug
sqlpackage /Action:Publish /SourceFile:"SkaldBot.Database.dacpac" /Profile:"/var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/Profiles/SkaldBot.Database.publish.xml"