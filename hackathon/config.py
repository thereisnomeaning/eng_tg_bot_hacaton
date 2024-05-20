from dotenv import load_dotenv

from os import getenv

import time

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
FOLDER_ID = getenv('FOLDER_ID')
IEM_TOKEN_INFO = {'IEM_TOKEN': 't1.9euelZqVi8jOzpONi8mPm5STi8uUx-3rnpWax5KYnJ2JjcqQk5ydmsyXz83l8_dTflJN-e90F3oz_N3z9xMtUE3573QXejP8zef1656VmsuTy5GXm5OPi5HKkpzJipWY7_zF656VmsuTy5GXm5OPi5HKkpzJipWYveuelZqJnJCRjo_JjpjPio2XmszOj7XehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.RLCQmxeXyRdamaVJPvsit1vEQSypBgm0mLiBuuGHVWI5-DtRSkTHyq47ffnrjXSO0rdjU2NpDPakXVpvEYkWCA',
                  'EXPIRES_IN': time.time() + 40000}
ADMIN_ID = int(getenv('ADMIN_ID'))

MAX_MODEL_TOKENS = 200
MAX_USERS = 6
MAX_STT_BLOCKS_PER_PERSON = 3
MAX_GPT_TOKENS_PER_PERSON = 1000
MAX_TTS_TOKENS_PER_PERSON = 1000
MAX_GPT_TOKENS_PER_MESSAGE = 500
MAX_TTS_TOKENS_PER_MESSAGE = 500

SYSTEM_PROMPT = '''Ты дружелюбный англичанин-ассистент. Коротко поддерживай беседу и задавай вопрос в конце.'''

SYSTEM_PROMPT_TRANSLATION = '''Переведи сообщение на русский.'''


class TTS:
    headers = {'Authorization': f'Bearer {IEM_TOKEN_INFO["IEM_TOKEN"]}'}
    url = getenv('TTS_URL')
    data = {
        'text': None,  # текст, который нужно преобразовать в голосовое сообщение
        'lang': 'en-US',  # язык текста - русский
        'voice': 'john',
        'folderId': FOLDER_ID
    }


class STT_ENG:
    # Указываем параметры запроса
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={FOLDER_ID}",
        "lang=en-US"  # распознаём голосовое сообщение на русском языке
    ])
    url = getenv('STT_URL') + params
    headers = {'Authorization': f'Bearer {IEM_TOKEN_INFO["IEM_TOKEN"]}'}


class STT_RU:
    # Указываем параметры запроса
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={FOLDER_ID}",
        "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
    ])
    url = getenv('STT_URL') + params
    headers = {'Authorization': f'Bearer {IEM_TOKEN_INFO["IEM_TOKEN"]}'}


class TOKENIZER:
    url = getenv('TOKENIZER_URL')

    headers = {
        'Authorization': f'Bearer {IEM_TOKEN_INFO["IEM_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
        "maxTokens": MAX_MODEL_TOKENS,
        "messages": []
    }


class GPT:
    url = getenv('GPT_URL')

    headers = {
        'Authorization': f'Bearer {IEM_TOKEN_INFO["IEM_TOKEN"]}',
        'Content-Type': 'application/json'}

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",  # модель для генерации текста
        "completionOptions": {
            "stream": False,  # потоковая передача частично сгенерированного текста выключена
            "temperature": 0.6,  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
            "maxTokens": "50"  # максимальное число сгенерированных токенов
        },
        "messages": [
            {
                "role": "system",
                "text": None
            }
        ]
    }


class IEM:
    headers = {"Metadata-Flavor": "Google"}
    metadata_url = getenv('IEM_TOKEN_URL')
