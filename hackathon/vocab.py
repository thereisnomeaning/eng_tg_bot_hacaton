import requests


def get_info_of_word(word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        return False, f'Error code {response.status_code}'
    try:
        info = response.json()[0]
    except:
        return False, f'Error receiving json file'
    print(info)
    try:
        definition = info["meanings"][0]['definitions'][0]['definition']
    except:
        definition = None

    try:
        example = info["meanings"][0]['definitions'][0]['example']
    except:
        example = None

    try:
        audio_url = info['phonetics'][0]['audio']
        audio = requests.get(audio_url)
        if audio.status_code < 200 or audio.status_code >= 300:
            return definition, example, f'Error code {response.status_code}'
        audio = audio.content
    except:
        audio = None
    print(audio)
    return definition, example, audio

