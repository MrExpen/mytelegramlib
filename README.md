# mytelegramlib
```
pip install requests
```

```python
from mytelegramlib import *


bot = TelegramBot('TOKEN')


for event in bot.getUpdates():
    print(event)
```
