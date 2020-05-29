# mytelegramlib
```
pip install requests
```


Simple echo bot:
```python
from mytelegramlib import *


bot = TelegramBot('TOKEN')


for event in bot.getUpdates():
    if event['type'] == 'text':
        bot.method('sendMessage', {
            'chat_id': event['message']['chat']['id'],
            'text': event['message']['text']
        })
```
or:
```python
from mytelegramlib import *

bot = TelegramBot('TOKEN')


@bot.onMessage(content_type=['text'])
def messaageHendler(event):
    bot.method('sendMessage', {
            'chat_id': event['message']['chat']['id'],
            'text': event['message']['text']
        })

bot.polling()
```