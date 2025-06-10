import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
import threading
import json
import os
import time
from panel import launch_gui

mic_device = 1
vcable_device = 7
headphones = 5
stream_active = True
volume = 1.0

with open("soundslist.json", "r", encoding="utf-8") as f:
    sound_data = json.load(f)["sets"]

current_set = 0
gui = None

def get_sound_path(index):
    return sound_data[str(current_set)][index]["file"]

def get_sound_name(index):
    return sound_data[str(current_set)][index]["name"]

def get_current_set():
    return sound_data.get(str(current_set), [])

def get_all_set_ids():
    return list(sound_data.keys())

def get_current_set_id():
    return str(current_set)

numpad_binds = {
    79: 0, 80: 1, 81: 2,
    75: 3, 76: 4, 77: 5,
    71: 6, 72: 7, 73: 8,
    82: 'switch'
}

def mic_loop():
    def callback(indata, outdata, frames, time_info, status):
        if not stream_active:
            outdata[:] = np.zeros_like(outdata)
        else:
            outdata[:] = indata

    with sd.Stream(device=(mic_device, vcable_device),
                   samplerate=44100, channels=1,
                   dtype='float32', callback=callback):
        while True:
            time.sleep(0.1)

def play_sound(index):
    global current_set, stream_active
    try:
        file = get_sound_path(index)
        if not os.path.exists(file):
            print(f"Plik nie istnieje: {file}")
            return
        print(f"[SET {current_set}] Odtwarzam: {get_sound_name(index)} -> {file}")
        stream_active = False
        if gui:
            gui.set_indicator(True)
        time.sleep(0.1)
        data, fs = sf.read(file, dtype='float32')
        #data *= volume
        sd.play(data, fs, device=vcable_device)
        sd.play(data, fs, device=headphones)
        sd.wait()
        time.sleep(0.05)
        stream_active = True
        if gui:
            gui.set_indicator(False)
    except Exception as e:
        print(f"Błąd: {e}")

def switch_set():
    global current_set
    ids = get_all_set_ids()
    if not ids:
        return
    index = ids.index(str(current_set))
    new_index = (index + 1) % len(ids)
    set_current_set(int(ids[new_index]))

def on_key(event):
    if event.event_type == 'down':
        action = numpad_binds.get(event.scan_code)
        if action == 'switch':
            switch_set()
        elif isinstance(action, int):
            play_sound(action)

def update_sound(index, file_path):
    name = os.path.basename(file_path)
    while len(sound_data[str(current_set)]) <= index:
        sound_data[str(current_set)].append({"name": "(Brak)", "file": ""})
    sound_data[str(current_set)][index] = {"name": name, "file": file_path}
    save_data()
    if gui:
        gui.refresh_grid()

def set_volume(v):
    global volume
    volume = v

def set_current_set(set_id):
    global current_set
    current_set = set_id
    if gui:
        gui.refresh_grid()
        gui.set_selector_value(str(set_id))

def add_set():
    new_id = str(max([int(k) for k in sound_data.keys()] + [-1]) + 1)
    sound_data[new_id] = []
    save_data()
    if gui:
        gui.update_set_selector(get_all_set_ids())
        set_current_set(int(new_id))

def delete_set():
    global current_set
    if len(sound_data) <= 1:
        print("Nie można usunąć ostatniego SETu")
        return
    del sound_data[str(current_set)]
    save_data()
    new_ids = get_all_set_ids()
    set_current_set(int(new_ids[0]))
    if gui:
        gui.update_set_selector(new_ids)

def save_data():
    with open("soundslist.json", "w", encoding="utf-8") as f:
        json.dump({"sets": sound_data}, f, ensure_ascii=False, indent=4)

def main():
    global gui
    print("Soundboard aktywny! Numpad 1–9 = dźwięki, Numpad 0 = zmień SET")
    print(sd.query_devices())

    threading.Thread(target=lambda: keyboard.hook(on_key), daemon=True).start()
    threading.Thread(target=mic_loop, daemon=True).start()

    root, gui_instance = launch_gui(get_current_set, update_sound, set_volume,
                                    get_all_set_ids(), set_current_set,
                                    add_set, delete_set)
    gui = gui_instance
    gui.set_selector_value(get_current_set_id())
    root.mainloop()

if __name__ == "__main__":
    main()