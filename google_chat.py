#!/usr/bin/python3

from httplib2 import Http
from json import dumps
import json
import sys
import datetime
import configparser
from pprint import pprint

INI_FILE = '<path_to_your>/google_chat.ini'

def prin_test(var1, var2):
    try: 
        print ( var1 +' ' +var2)
        
        msg = sys.argv[2]
        event = msg.split('#')

        print('status ',event[0])
        print('time ',event[1])
        print('date ',event[2])
        print('trigger_name ',event[3])
        print('host_name ',event[4])
        print('severity ',event[5])
        print('event_id ',event[6])
        print('trigger_url ',event[7])
        print('trigger_id ',event[8])
        print('host_description ',event[9])

    except IndexError :
        print ('no argument')

def get_config(path):
    """
    Returns the config object
    """
  
    config = configparser.RawConfigParser()
    config.read(path)
    
    return config
 
def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )
    
    #print(msg)
    return value

def pars_msg(inmsg):
    
    msg = inmsg
    event = msg.split('#')
    HOST = get_setting(INI_FILE, 'zabbix', 'host')

    # resolv status     
    stat_ev = None
    unit_to_stat = {
        '0': 'PROBLEM',
        '1': 'RESOLV',
        '2': 'update',
    }
    stat_ev = unit_to_stat[ event[0] ]
    
    # resolv url img    
    image_url = None
    unit_to_img_url = {
        '0': get_setting(INI_FILE, 'pictures', 'PROBLEM_IMG'),
        '1': get_setting(INI_FILE, 'pictures', 'RESOLVED_IMG'),
        '2': get_setting(INI_FILE, 'pictures', 'ACK_IMG'),
    }
    image_url = unit_to_img_url[ event[0] ]
    
    if event[0] != "2":
        bot_message = {
        "cards": [{
            
            "header": 
                { 
                  "title": "Severidade: " + event[5],
                  "subtitle": stat_ev,
                  "imageUrl": image_url,
                  "imageStyle": "IMAGE"
                },
            
            "sections": [
                 { "widgets": [
                       { "keyValue": 
                             { 
                               "topLabel": "Alarme",
                               "content": event[3],
                               "contentMultiline": "true"
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "Host",
                               "content": event[4] + " " + event[9],
                               "contentMultiline": "true"
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "Data/time",
                               "content": event[2] + " - " + event[1]
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "ID Event",
                               "content": event[6]
                             }
                       }
                 ]},
                 { "widgets": [
                       { "buttons": [
                             {
                               "textButton": 
                                   {
                                     "text": "VIEW EVET",
                                     "onClick": 
                                         {
                                           "openLink": 
                                             {
                                                "url": HOST + "/tr_events.php?triggerid=" + event[8] + "&eventid=" + event[6]
                                             }
                                         }
                                   }
                             }
                         ]}
                 ]}       
             ]}
         ]}

    else:
    	bot_message = {
        "cards": [{
            
            "header": 
                { 
                  "title": stat_ev,
                  "subtitle": event[3],
                  "imageUrl": image_url,
                  "imageStyle": "IMAGE"
                },
            
            "sections": [
                 { "widgets": [
                       { "keyValue": 
                             { 
                               "topLabel": "Message",
                               "content": event[4],
                               "contentMultiline": "true"
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "Current alarm status",
                               "content": event[5]
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "Data/time",
                               "content": event[2] + " - " + event[1]
                             }
                       },
                       { "keyValue": 
                             {
                               "topLabel": "ID Event",
                               "content": event[6]
                             }
                       }
                 ]},
                 { "widgets": [
                       { "buttons": [
                             {
                               "textButton": 
                                   {
                                     "text": "VIEW EVET",
                                     "onClick": 
                                         {
                                           "openLink": 
                                             {
                                                "url": HOST + "/tr_events.php?triggerid=" + event[7] + "&eventid=" + event[6]
                                             }
                                         }
                                   }
                             }
                         ]}
                 ]}       
             ]}
         ]}

    return bot_message

def send_mess(send_to, bmes):
     
    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri= get_setting(INI_FILE, 'chat', send_to),
        method='POST',
        headers=message_headers,
        body=dumps(bmes),
    )
    #pprint(response)

def main():
   #prin_test(sys.argv[1], sys.argv[2])
   #pprint (pars_msg(sys.argv[2]))
   send_mess(sys.argv[1], pars_msg(sys.argv[2]))
   
if __name__ == '__main__':
    main()