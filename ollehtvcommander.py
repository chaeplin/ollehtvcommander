#!/usr/bin/env python2
# encoding: utf-8

import sys
import httplib
import simplejson as json

url = "qookguide.paran.com"
headers = {"Accept-Language": "ko-kr", "User-Agent": "%EC%98%AC%EB%A0%88%20tv%20play/2.0.9 CFNetwork/672.1.15 Darwin/14.0.0"}

# to use this script, device_id is needed
# to get device_id, 
# 1) connect [olleh TV] and [olleh TV play]
# 2) use Fiddler or Charles for proxy, set proxy of phone
# 3) http is used at only one menu, and it has device_id
# 4) select - [menu] - [my olleh tv play] at app
# 5) check Fiddler or Charles http request : device_id=xxxxx-xxxx-xxxx......
# 


device_id = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxxx"


def getauth():
    conn = httplib.HTTPSConnection(url)
    conn.request("GET", "/app/device/authDevice?device_id=" + device_id, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != 'OK':
        sys.exit(httpResponse.reason)
    else:
        return True

def getstatus():
    conn = httplib.HTTPSConnection(url)
    conn.request("GET", "/app/remote/getTvState?device_id=" + device_id, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != 'OK':
        sys.exit(httpResponse.reason)

    d = json.loads(httpResponse.read())
	
    if d['STB_STATE'] == 0:
        print "STB is off"
    else:
        print "STB is on"
        print "CH_NO : %s, CH_NAME : %s, PROGRAMNAME : %s" % (d['SERVICE_CH_NO'], d['CH_NAME'], d['PROGRAMNAME'])

# key
# 409 : on / off
#

def getoff():
    conn = httplib.HTTPSConnection(url)
    conn.request("GET", "/app/remote/inputButton?key_cd=409&device_id=" + device_id, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != 'OK':
        sys.exit(httpResponse.reason)
    else:
        return True


if getauth():
    getstatus()
    #getoff()
