"""wav音频文件播放"""

import wave
import pyaudio

wav_file = "resource/daomadi.wav"


def play(wav_file):
    chunk = 1024  
    wf = wave.open(wav_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), 
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(), 
                    output=True)

    data = wf.readframes(chunk)  # 读取数据
    while data != b'':  # 播放
        stream.write(data)
        data = wf.readframes(chunk)

    # 停止数据流
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    play(wav_file)