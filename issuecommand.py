#! /usr/bin/env python
from rustadmin import RustAdmin

cs = RustAdmin(url='192.168.1.137:5678', passwd='password')
mess = cs.sndcommand(msg='inventory.giveto dayhkr wood 10000')

print mess['Message']
#inventory.giveto dayhkr wood 100
#server.writecfg
#weather.clouds
#weather.fog
#weather.wind
#weather.rain
#global.playerlist
#global.users
#global.say
#global.ownerid
#global.moderatorid
#global.status
#global.kick
#global.listid
