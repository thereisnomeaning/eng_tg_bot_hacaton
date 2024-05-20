from database import all_users, user_in_table, get_tts_tokens, get_stt_blocks, get_gpt_tokens

from config import (MAX_USERS, MAX_TTS_TOKENS_PER_PERSON, MAX_TTS_TOKENS_PER_MESSAGE, MAX_STT_BLOCKS_PER_PERSON,

                            MAX_GPT_TOKENS_PER_PERSON, MAX_GPT_TOKENS_PER_MESSAGE)

from gpt import gpt_tokenizer


# Проверяем, что количество пользователей в пределе
def is_user_amount_limit(user_id):
    amount_of_users = all_users()

    is_user = user_in_table(user_id)

    if not (amount_of_users < MAX_USERS or is_user):
        return False

    return True


# Проверяем, что количество ттс символов на одного пользователя находится в пределе
def is_tts_symbol_limit_per_person(user_id):
    all_tts_tokens = get_tts_tokens(user_id)

    if all_tts_tokens >= MAX_TTS_TOKENS_PER_PERSON:
        return False

    return True


# Проверяем, что количество ттс символов на одно соообщение находится в пределе.
def is_tts_symbol_limit_per_message(text):
    if len(text) > MAX_TTS_TOKENS_PER_MESSAGE:
        return False

    return True


# Проверяем, что количество стт блоков на одного пользователя находится в пределе.
def is_stt_blocks_limit_per_person(user_id):
    all_stt_blocks = get_stt_blocks(user_id)

    if all_stt_blocks >= MAX_STT_BLOCKS_PER_PERSON:
        return False

    return True


# Проверяем, что количество стт блоков на одно сообщение находится в пределе.
def is_stt_blocks_limit_per_message(voice_duration):
    if voice_duration >= 30:
        return False

    return True


# Проверяем, что количество гпт токенов на одного пользователя находится в пределе.
def is_gpt_tokens_limit_per_person(user_id):
    all_gpt_tokens = get_gpt_tokens(user_id)

    if all_gpt_tokens >= MAX_GPT_TOKENS_PER_PERSON:
        return False

    return True


# Проверяем, что количество гпт токенов на одно сообщение в пределе.
def is_gpt_tokens_limit_per_message(text, sys_prompt):
    state, tokens_in_message = gpt_tokenizer(text, sys_prompt)

    if not state:
        tokens_in_message = len(text) // 6

    if tokens_in_message > MAX_GPT_TOKENS_PER_MESSAGE:
        return False, tokens_in_message

    return True, tokens_in_message




