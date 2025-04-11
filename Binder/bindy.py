import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
import threading
import os
import time

# KONFIG
mic_device = 1  # <-- ID mikrofonu fizycznego
vcable_device = 7# <-- ID VB-CABLE Output

sound_sets = [
    ['set1/1.mp3', 'set1/2.wav', 'set1/3.wav', 'set1/4.wav', 'set1/5.wav', 'set1/6.wav', 'set1/7.wav', 'set1/8.wav', 'set1/9.wav'],
    ['set2/1.wav', 'set2/2.wav', 'set2/3.wav', 'set2/4.wav', 'set2/5.wav', 'set2/6.wav', 'set2/7.wav', 'set2/8.wav', 'set2/9.wav'],
    ['set3/1.wav', 'set3/2.wav', 'set3/3.wav', 'set3/4.wav', 'set3/5.wav', 'set3/6.wav', 'set3/7.wav', 'set3/8.wav', 'set3/9.wav'],
]

numpad_binds = {
    79: 0, 80: 1, 81: 2, 75: 3, 76: 4, 77: 5,
    71: 6, 72: 7, 73: 8,
    82: 'switch'
}

current_set = 0
stream_active = True  # steruje wątek mikrofonu

def mic_loop():
    def callback(indata, outdata, frames, time, status):
        if not stream_active:
            outdata[:] = np.zeros_like(outdata)
            return
        outdata[:] = indata

    with sd.Stream(device=(mic_device, vcable_device),
                   samplerate=44100, channels=1,
                   dtype='float32', callback=callback):
        while True:
            time.sleep(0.1)

def play_sound(index):
    global current_set, stream_active
    try:
        file = sound_sets[current_set][index]
        if not os.path.exists(file):
            print(f"Plik nie istnieje: {file}")
            return
        print(f"[SET {current_set + 1}] {file}")
        stream_active = False  # wycisz mikrofon
        time.sleep(0.1)  # krótka pauza zanim zaczniemy bind
        data, fs = sf.read(file, dtype='float32')
        sd.play(data, fs, device=vcable_device)
        sd.wait()
        time.sleep(0.05)
        stream_active = True  # wznow mikrofon
    except Exception as e:
        print(f"Błąd: {e}")

def switch_set():
    global current_set
    current_set = (current_set + 1) % len(sound_sets)
    print(f"Przełączono na SET {current_set + 1}")

def on_key(event):
    if event.event_type == 'down':
        action = numpad_binds.get(event.scan_code)
        if action == 'switch':
            switch_set()
        elif isinstance(action, int):
            threading.Thread(target=play_sound, args=(action,), daemon=True).start()

def main():
    global mic_device, vcable_device
    print("Soundboard aktywny! Numpad 1–9 = dźwięki, Numpad 0 = zmień SET, ESC = wyjście.")
    print(sd.query_devices())
    threading.Thread(target=mic_loop, daemon=True).start()
    keyboard.hook(on_key)
    keyboard.wait('esc')
    print("Zamykanie soundboardu.")

if __name__ == "__main__":
    main()
1