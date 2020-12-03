import os
from pydub import AudioSegment

# Конфигурации

# Путь к аудиозаписям в формате .wav
wav_path = '/home/username/PycharmProjects/asr/wav'

# Путь куда кладём аудиозаписи формата .ogg
ogg_path = '/home/username/PycharmProjects/asr/ogg'

# Частота дискретизации
ogg_sample_rate = 48000


# a = os.listdir(path="/home/artem/PycharmProjects/asr/vrem")
# print(a)



def wav_to_ogg(wav_file_path, ogg_file_path, ogg_sample_rate, mono=False, left=True):
    '''Функция коныертации аудио в формат .ogg
    Так же можно выделять каждлого из спикеров при помощи "mono" и 'left'
    '''
    f = open(wav_file_path, 'r')
    audio = AudioSegment.from_wav(f.name)
    audio = audio.set_frame_rate(ogg_sample_rate)
    if mono == True:
        if left == True:
            audio = audio.split_to_mono()[0]
        else:
            audio = audio.split_to_mono()[1]
    print(audio)
    audio.export(ogg_file_path, format="opus", bitrate='256k')
    f.close()



if __name__ == '__main__':
	list_wav = os.listdir(path=wav_path)


	for audio in list_wav:
	    wav_file_path = str(wav_path + '/' + audio)
	    ogg_file_path = str(ogg_path + '/' + audio[:	(len(audio)-4)] + '.ogg')
	    wav_to_ogg(wav_file_path, ogg_file_path, 	ogg_sample_rate)
