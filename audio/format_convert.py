# 使用ffmpeg将m4a转换为wav格式

import os
import subprocess


def m4a2wav(input, output):

    cmd_head = 'ffmpeg -i '
    cmd = cmd_head + input + ' -ar 16000 ' + output
    subprocess.Popen(cmd, shell=True, stdout=None, stderr=None).wait()


path = 'D:/Data/Jiyao_address/002/'
# path = "D:/Code/ASRT_SpeechRecognition_V1.3.0/data/20220829_091159.m4a"

save_path = ''

if not save_path:
    save_path = path

# 判断文件还是文件夹
if path.endswith('.m4a'):
    files = [path]
else:
    files = [path + i for i in os.listdir(path)]

# 判断文件格式
for file in files:
    if 'wav' not in file:

        name = file.split('/')[-1].split('.')[0]
        save_name = os.path.join(save_path, name + '.wav')  

        m4a2wav(file, save_name)

        print('', name, '  ->  ', save_name)
        print('--Over')