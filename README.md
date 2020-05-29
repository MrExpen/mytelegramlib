# mytelegramlib
```
pip install requests
```


Quick start
```python
from mytelegramlib import *


bot = TelegramBot('TOKEN')


for event in bot.getUpdates():
    print(event)
```
