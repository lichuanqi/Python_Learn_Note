# 使用ffmpeg将m4a转换为wav格式

import os
import subprocess


file_path = "D:/Code/ASRT_SpeechRecognition_V1.3.0/data/20220829_091159.m4a"

if 'wav' not in file_path:
    f = file_path.split('/')[-1].split('.')[-1]
    save_path = file_path.replace(f, 'wav')

    cmd_head = 'ffmpeg -i '
    cmd = cmd_head + file_path + ' -ar 16000 ' + save_path

    print('开始执行以下命令：\n', cmd)
    subprocess.Popen(cmd, shell=True, stdout=None, stderr=None).wait()