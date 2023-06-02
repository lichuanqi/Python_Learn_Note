# 测试pyaudio录音时的输入输出设备

import pyaudio


p = pyaudio.PyAudio()
device_count = p.get_device_count()

device_inputs = []
device_outputs = []
for i in range(device_count):
    device = p.get_device_info_by_index(i)

    if device['maxInputChannels'] >0:
        device_inputs.append(device)
    elif device['maxOutputChannels'] >0:
        device_outputs.append(device)

# 输入设备列表
for i, dev_in in enumerate(device_inputs):
    name = dev_in['name']
    print(f'input - {i}: {name}')

# 输出设备列表
for i, dev_out in enumerate(device_outputs):
    name = dev_out['name']
    print(f'output - {i}: {name}')

# 默认的输入设备信息
default_input = p.get_default_input_device_info()
print(f'default_input: {default_input}')