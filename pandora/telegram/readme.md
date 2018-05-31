Deze app is iets lastiger om te gebruiken, omdat je niet echt je eigen Telegram bot
in een Telegram channel kan toevoegen. Het zou ook wel met Selenium oid
kunnen maar moeite.

Wat je moet doen is scrollen naar boven in de telegram chat, en dan als je
genoeg data hebt  doe je rechter muisknop op een bericht en 'Inspect Element'. 
In de Inspector (dit is Firefox) scroll je naar boven naar 
<div class="im_history_messages_peer">
- de div die alle berichten bevat, en doe je daarop rechter muisknop en 'Copy
Inner HTML'

Die data plak je in een texteditor en noem je 'berichten.html', en dan run je
parser.py
