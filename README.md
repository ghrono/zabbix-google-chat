# zabbix-google-chat
Python script to send Zabbix notifications to Hangouts Chat (G Suite).

Guidelines on how to use this code are available at:

https://medium.com/monitoracaodeti/enviando-notifica%C3%A7%C3%B5es-do-zabbix-via-api-do-hangouts-chat-aa0c0e8197a1

#***************************************

EXAMPLES
    https://developers.google.com/hangouts/chat/reference/message-formats/


#***************************************

setep 1:
    edit line to google_chat.py
     
     INI_FILE = '<path_to_your>/google_chat.ini'

steep 2:
    edit lines google_chat.ini
   
    enter IP or doman_name your server
     host = http://<your_zabbix_address>/zabbix
    
    enter webhook your google chat /chats
     FirstRoom = webhook_url_generated_in_hangouts_chat_room
     SecondRoom = webhook_url_generated_in_hangouts_chat_room
