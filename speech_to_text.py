import boto3
import requests
import time
import json
import os

# Конфигурации


# Регион (p. s. другой выбирать нельзя)
REGION_NAME = 'ru-central1'
# id-статического ключа доступа к Бакету
AWS_SECRET_KEY_ID = 'YOUR__KEY_ID'
# Секретный ключ (статического ключа доступа к Бакету)
AWS_SECRET_ACCESS_KEY = 'YOUR__SECRET_ACCESS_KEY'
# Имя Бакета
bucket_name = 'you__backet_name'

# API-ключ Сервисного аккаунта
api_key = 'your_api_key_your_srv_acc'

# Путь откуда берём аудиозаписи формата .ogg
ogg_path = '/home/user_name/PycharmProjects/asr/ogg'
# Путь куда кладём текст из результатов распознавания .txt
txt_path = '/home/user_name/PycharmProjects/asr/text'


def file_to_storage(file_path, bucket_name, result_file_name):
    '''Функция возращает ссылку на аудиофайл из Бакета SpeechKit
      предварительно загрузив его туда из локальной папки'''

    session = boto3.session.Session(region_name=REGION_NAME, aws_access_key_id=AWS_SECRET_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    link_head = "https://storage.yandexcloud.net/"

    try:
        s3.upload_file(file_path, bucket_name, result_file_name)
        file_link = link_head + bucket_name + "/" + result_file_name
    except:
        file_link = None

    return file_link


def speech_to_text(api_key, filelink, result_file_name):
    '''Функция распознования аудио и формирования текста аудио,
    сохранив его в файл .txt в локальную папку'''

    POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"

    # Формируем сам текст запроса
    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU"
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    # Если вы хотите использовать IAM-токен для аутентификации, замените Api-Key на Bearer.
    header = {'Authorization': 'Api-Key {}'.format(api_key)}

    # Отправить запрос на распознавание.
    req = requests.post(POST, headers=header, json=body)
    data = req.json()
    # print(data)

    id = data['id']

    # Запрашивать на сервере статус операции, пока распознавание не будет завершено.
    while True:
        time.sleep(1)

        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=id), headers=header)
        req = req.json()

        if req['done']: break
        # print("Not ready")

    # Сохранить текст из результатов распознавания в файл.
    f = open(str(txt_path + '/' + result_file_name[:(len(result_file_name) - 4)] + '.txt'), 'w')
    for chunk in req['response']['chunks']:
        if chunk['channelTag'][0] == '1':
            f.write(str(chunk['alternatives'][0]['text']) + '\n')
    f.close()

if __name__ == '__main__':
	list_ogg = os.listdir(path=ogg_path)

	for audio in list_ogg:
    	print(audio)
    	file_path = str(ogg_path + '/' + audio)
    	result_file_name = str(audio[:(len(audio) - 4)] + '.ogg')
    	filelink = str(file_to_storage(file_path, bucket_name, result_file_name))
    	speech_to_text(api_key, filelink, result_file_name)
	print('Speech recognition completed')
