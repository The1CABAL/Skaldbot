#!/bin/bash
echo "export PATH=\"\$PATH:$HOME/sqlpackage\"" >> /home/ib-2020/.bashrc
sudo chmod a+x /home/ib-2020/sqlpackage/sqlpackage
sudo source /home/ib-2020/.bashrc
cd /var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/bin/Debug
sqlpackage /Action:Publish /SourceFile:"SkaldBot.Database.dacpac" /Profile:"/var/lib/go-agent/pipelines/SkaldBot-DBOTest/SkaldBot.Database/Profiles/SkaldBot.Database.publish.xml"