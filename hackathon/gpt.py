import requests
import time
import logging
from config import TOKENIZER, GPT, IEM_TOKEN_INFO, IEM

logger = logging.getLogger('__main__')


# Подсчитываем количество токенов в сообщении.
def gpt_tokenizer(user_prompt, sys_prompt):
    data = TOKENIZER.data.copy()

    data["messages"].append(
        {
            "role": 'user',
            "text": user_prompt
        })

    if sys_prompt:
        data['messages'].append(
            {
                "role": 'system',
                "text": sys_prompt
            }
        )

    try:
        return True, len(requests.post(url=TOKENIZER.url, headers=TOKENIZER.headers, json=data).json()['tokens'])
    except Exception as e:
        logging.error(f'Error occured in gpt tokenizer')
        return False, None


# Отправляем промт модели.
def gpt(user_prompt, sys_prompt=None):
    data = GPT.data.copy()
    data['messages'] = [{'role': 'system', 'text': sys_prompt}]

    for i in user_prompt:
        data['messages'].append(i)

    response = requests.post(url=GPT.url, headers=GPT.headers, json=data)
    if response.status_code < 200 or response.status_code >= 300:
        return False, f'Error code {response.status_code}'
    try:
        full_response = response.json()
    except:
        return False, f'Error receiving json file'
    if 'error' in full_response or 'result' not in full_response:
        return False, full_response
    result = full_response["result"]["alternatives"][0]["message"]["text"]
    if not result:
        return True, f'Объяснение закончено'
    return True, result


# Проверяем и создаем, если это необходимо, IEM токен.
def check_and_create_IEM_token(TOKEN_EXPIRES_IN):
    if TOKEN_EXPIRES_IN <= time.time():
        try:
            response = requests.get(url=IEM.metadata_url, headers=IEM.headers)
            if response.status_code == 200:
                token_data = response.json()
                IEM_TOKEN_INFO["IEM_TOKEN"] = token_data['access_token']
                IEM_TOKEN_INFO["EXPIRES_IN"] = time.time() + token_data['expires_in']
                logging.info('Token succesfully created')
                return True
            else:
                logging.error(f'Failed to retrieve IAM token. Status code {response.status_code}')
                return False
        except:
            logging.error('Failed to get request to retrive IAM token.')
            return False
    else:
        return True
