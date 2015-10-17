#!/usr/bin/env python2
# encoding: utf-8
# code from https://github.com/ubaransel/lgcommander
# code from https://github.com/ypid/lgcommander
# 
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

# 올레 tv play.. 의 문제점은 페어링 이후 device_id 로만 모든게 처리된다는 것.(어쩔수 없나....)
# - 셋탑박스 메뉴에서 큐알이나 전화번호로 인증 받아서 device_id 할당 받고, 웹주소만(KT서버) 알면 
# 어디에서나/어느브라우저라도 시청 중인 채널을 알수 있고, 셋탑박스를 끌 수 있고, 채널도 변경 가능하고.....
# device_id 는 ssl proxy 없이 tcpdump/http proxy만 해도 보이는 메뉴가 있..
#
# + TV 742번 메뉴 연결 관리에서 등록된 디바이스 확인/삭제 가능.

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

    if 'STB_STATE' in d:

        if d['STB_STATE'] == '0':
            print ("-----> STB IS OFF")

        elif d['STB_STATE'] == '2':
            print ("-----> STB IS ON")

            if d['RUN_MODE'] == '0':
                print ("-----> PROGRAMNAME : %s") % d['PROGRAMNAME']               
            elif d['RUN_MODE'] == '2':
                print ("-----> VOD CONTENT_ID : %s, PROGRAMNAME : %s") % (d['CONTENT_ID'], d['PROGRAMNAME'])
            elif d['RUN_MODE'] == '1':
                print ("-----> CH_NO : %s, CH_NAME : %s, PROGRAMNAME : %s") % (d['SERVICE_CH_NO'], d['CH_NAME'], d['PROGRAMNAME'])

            else:
                print ("-----> PROGRAMNAME : ???")

        else:
            print ("-----> STB IS ???")

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

