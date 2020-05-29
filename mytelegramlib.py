import requests
import json


class TelegramBot:
    def __init__(self, token: str, based_url='https://telegg.ru/orig'):
        self.URl = f'{based_url}/bot{token}/'
        self.functions = []

    def method(self, name: str, params=None):
        response = requests.get(self.URl + name, params=params)
        if response.json()['ok']:
            return response.json()['result']
        print(response.json())
        raise Exception('server return a non "ok" status')

    def getUpdates(self):
        last_update = 0
        while True:
            for event in self.method('getUpdates', {'offset': last_update, 'count': 1}):
                event['type'] = self.getEventType(event)
                yield event
                last_update = event['update_id'] + 1

    def getEventType(self, event):
        if event.get('message'):
            if event['message'].get('text'):
                return 'text'
            elif event['message'].get('sticker'):
                return 'sticker'
            elif event['message'].get('document'):
                return 'document'
            elif event['message'].get('photo'):
                return 'photo'
            elif event['message'].get('voice'):
                return 'voice'
            elif event['message'].get('audio'):
                return 'audio'
            elif event['message'].get('location'):
                return 'location'
            elif event['message'].get('poll'):
                return 'poll'
            elif event['message'].get('contact'):
                return 'contact'
            elif event['message'].get('video_note'):
                return 'video_note'
            elif event['message'].get('video'):
                return 'video'
            elif event['message'].get('forward_message'):
                return 'forward_from'
            elif event['message'].get('reply_to_message'):
                return 'reply_to_message'
            elif event['message'].get('dice'):
                return 'dice'
        elif event.get('edited_message'):
            return 'edit_message'
        elif event.get('callback_query'):
            return 'callback_query'
        return 'unknown'

    def getCommands(self, event):
        commands = set()
        if event['message'].get('entities'):
            for entiti in event['message']['entities']:
                if entiti['type'] == 'bot_command':
                    commands.add(event['message']['text'][entiti['offset']+1:entiti['offset'] + entiti['length']])
        return commands

    def polling(self):
        breakFlag = False
        for event in self.getUpdates():
            for func in self.functions:
                if event['type'] == 'callback_query':
                    if event['callback_query']['data'] in func['callback_datas']:
                        func['func'](event)
                        break
                if event['type'] == 'text':
                    if not self.getCommands(event).isdisjoint(func['commands']):
                        func['func'](event)
                        break
                if event['type'] in func['types'] or 'any' in func['types']:
                    func['func'](event)
                    break

    def eventHendler(self, content_types=[], commands=[], callback_datas=[]):
        def decorator(func):
            self.functions.append({'func': func, 'types': content_types, 'commands':set(commands), 'callback_datas': callback_datas})
            return func
        return decorator


class ReplyKeyboardMarkup:
    def __init__(self, resize_keyboard=False, one_time_keyboard=False, **kwargs):
        self.object = {
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
            **kwargs,
            'keyboard': [[]]
        }

    def getKeyboard(self):
        return json.dumps(self.object)

    def addButton(self, text, **kwargs):
        self.object['keyboard'][-1].append({'text': text, **kwargs})

    def addLine(self):
        self.object['keyboard'].append([])

    def __str__(self):
        return str(self.object)


class InlineKeyboardMarkup:
    def __init__(self):
        self.object = {'inline_keyboard': [[]]}

    def getKeyboard(self):
        return json.dumps(self.object)

    def addButton(self, text, callback_data='', url='', **kwargs):
        self.object['inline_keyboard'][-1].append({
            'text': text,
            'callback_data': callback_data,
            'url': url,
            **kwargs
        })

    def addLine(self):
        self.object['inline_keyboard'].append([])

    def __str__(self):
        return str(self.object)
