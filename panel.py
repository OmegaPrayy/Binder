import tkinter as tk
from tkinter import filedialog, ttk

class SoundboardGUI:
    def __init__(self, master, get_current_set_callback, update_sound_callback, set_volume_callback, set_ids, set_current_set_callback, add_set_callback, delete_set_callback):
        self.master = master
        self.get_current_set = get_current_set_callback
        self.update_sound = update_sound_callback
        self.set_volume_callback = set_volume_callback
        self.set_current_set_callback = set_current_set_callback
        self.add_set_callback = add_set_callback
        self.delete_set_callback = delete_set_callback

        self.master.title("Soundboard 3x3")
        self.buttons = []

        control_frame = tk.Frame(master)
        control_frame.pack(padx=10, pady=5)

        # Set selector
        self.set_selector = ttk.Combobox(control_frame, values=set_ids, state="readonly")
        self.set_selector.pack(side=tk.LEFT, padx=5)
        self.set_selector.bind("<<ComboboxSelected>>", self._on_set_selected)

        # Add set button
        tk.Button(control_frame, text="Dodaj SET", command=self._on_add_set).pack(side=tk.LEFT, padx=5)

        # Delete set button
        tk.Button(control_frame, text="Usuń SET", command=self._on_delete_set).pack(side=tk.LEFT, padx=5)

        # Volume control
        volume_frame = tk.Frame(master)
        volume_frame.pack(pady=5)
        tk.Label(volume_frame, text="Głośność:").pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=1, resolution=0.01,
                                      orient=tk.HORIZONTAL, length=200,
                                      command=lambda v: self.set_volume_callback(float(v)))
        self.volume_slider.set(1.0)
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        # Indicator
        self.indicator = tk.Canvas(volume_frame, width=20, height=20)
        self.indicator.pack(side=tk.LEFT)
        self.indicator_circle = self.indicator.create_oval(2, 2, 18, 18, fill="gray")

        # Grid
        self.grid_frame = tk.Frame(master)
        self.grid_frame.pack(padx=10, pady=10)

        for i in range(9):
            btn = tk.Button(self.grid_frame, text=f"{i+1}", width=20, height=4,
                            command=lambda idx=i: self.change_sound(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.refresh_grid()

    def refresh_grid(self):
        current_set = self.get_current_set()
        for i in range(9):
            label = current_set[i]["name"] if i < len(current_set) else "(Brak)"
            self.buttons[i].config(text=f"{i+1}\n{label}")

    def change_sound(self, index):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if file_path:
            self.update_sound(index, file_path)
            self.refresh_grid()

    def set_indicator(self, state):
        color = "green" if state else "gray"
        self.indicator.itemconfig(self.indicator_circle, fill=color)

    def update_set_selector(self, new_ids):
        self.set_selector["values"] = new_ids

    def set_selector_value(self, value):
        self.set_selector.set(value)

    def _on_set_selected(self, event):
        selected_id = self.set_selector.get()
        self.set_current_set_callback(int(selected_id))

    def _on_add_set(self):
        self.add_set_callback()

    def _on_delete_set(self):
        self.delete_set_callback()


def launch_gui(get_current_set_callback, update_sound_callback, set_volume_callback, set_ids, set_current_set_callback, add_set_callback, delete_set_callback):
    root = tk.Tk()
    gui = SoundboardGUI(root, get_current_set_callback, update_sound_callback,
                        set_volume_callback, set_ids, set_current_set_callback,
                        add_set_callback, delete_set_callback)
    return root, gui
