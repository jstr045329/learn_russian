import pyaudio 
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"


# detect devices:
p = pyaudio.PyAudio()
host_info = p.get_host_api_info_by_index(0)    
device_count = host_info.get('deviceCount')
devices = []

# iterate between devices:
speaker_idx = None
for i in range(0, device_count):
    device = p.get_device_info_by_host_api_device_index(0, i)
    print(str(device))
    devices.append(device['name'])
    if ("Stereo Mix" in device['name']) and ("Realtek(R) Audio" in device['name']):
        speaker_idx = device['index']

stream = p.open(format=FORMAT,
                channels=2,
                rate=RATE,
                input=True,
                input_device_index=speaker_idx,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

