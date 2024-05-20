from validation import (is_stt_blocks_limit_per_person, is_stt_blocks_limit_per_message,
                        is_gpt_tokens_limit_per_person,
                        is_tts_symbol_limit_per_person)
from gpt import check_and_create_IEM_token, gpt
from config import IEM_TOKEN_INFO, SYSTEM_PROMPT, SYSTEM_PROMPT_TRANSLATION
from speechkit import speech_to_text, text_to_speech
from database import get_user_prompts, get_last_message_and_translation
import logging

logger = logging.getLogger('__main__')


def stt(user_id, audio_file, duration, language):
    if not is_stt_blocks_limit_per_person(user_id):
        logging.info(f'User_id {user_id} run out of stt blocks')

        return 'LIMIT', 'Ваш лимит общения с ботом голосом исчерпан, попробуйте общаться текстом.'

    if not is_stt_blocks_limit_per_message(duration):
        logging.info(f'User_id sent too large voice message (over 30 second)')
        return 'LIMIT_LENGHT', 'Слишком длинное голосовое сообщение, должно быть меньше 30 секунд.'

    if not check_and_create_IEM_token(IEM_TOKEN_INFO['EXPIRES_IN']):
        logging.error(f'User_id {user_id} got an error accessing SpeachKit tts')
        return 'IEM_ERROR', 'Произошла ошибка взаимодействия с нейронной сетью. Приносим свои извинения.'

    status, text = speech_to_text(audio_file, language)

    if not status:
        logging.error(f'User_id {user_id} got an error accessing SpeachKit stt in sts')
        return 'STT_ERROR', 'Не получилось расшифровать ваше голосовое сообщение, приносим извинения.'
    return 'SUCCESS', text


def ttt(user_id, text, session_id, tokens_limit, action):
    if not is_gpt_tokens_limit_per_person(user_id):
        logging.info(f'User_id {user_id} ran out of gpt tokens')
        return 'LIMIT', 'Ваш лимит диалога превышен.'

    if not tokens_limit:
        return 'LIMIT', 'Слишком длинное голосовое сообщение, укоротите его.'

    if not check_and_create_IEM_token(IEM_TOKEN_INFO['EXPIRES_IN']):
        return 'IEM_ERROR', 'Произошла ошибка взаимодействия с нейронной сетью. Приносим свои извинения.'

    if action == 'generating':
        prompt = get_user_prompts(user_id, session_id)
        status, gpt_text = gpt(prompt, SYSTEM_PROMPT)

    elif action == 'translation':
        prompt = [{'role': 'user', 'text': get_last_message_and_translation(user_id)[0]}]
        status, gpt_text = gpt(prompt, SYSTEM_PROMPT_TRANSLATION)

    if not status:
        logging.error(f'User_id {user_id} got an error accessing gpt model: {text}')

        return 'TTT_ERROR', 'Произошла ошибка, приносим свои извинения.'
    return 'SUCCESS', gpt_text


def tts(user_id, text):
    if not is_tts_symbol_limit_per_person(user_id):

        logging.info(f'User_id {user_id} ran out of tts tokens')
        return 'LIMITS', 'Ваши лимиты голосового общения исчерпаны.'

    if not check_and_create_IEM_token(IEM_TOKEN_INFO['EXPIRES_IN']):
        logging.error(f'Got an error extracting IEM TOKEN')
        return 'IEM_ERROR', 'Произошла ошибка взаимодействия с нейронной сетью. Приносим свои извинения.'

    status, audio = text_to_speech(text)

    if not status:
        logging.error(f'User_id {user_id} got an error accessing SpeachKit tts')
        return 'TTS_ERROR', ('Что-то пошло не так с голосовым ответом.'
                       'В качестве извинения приподносим вам текст языковой модели.')
    return 'SUCCESS', audio