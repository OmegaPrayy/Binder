import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class SoundboardGUI:
    def __init__(self, master, get_current_set_callback, update_sound_callback,
                 set_volume_callback, set_ids, set_current_set_callback,
                 add_set_callback, delete_set_callback):
        self.get_current_set = get_current_set_callback
        self.update_sound = update_sound_callback
        self.set_volume_callback = set_volume_callback
        self.set_current_set_callback = set_current_set_callback
        self.add_set_callback = add_set_callback
        self.delete_set_callback = delete_set_callback

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master = master
        self.master.title("Soundboard 3x3")
        self.buttons = []

        # Folder icon
        self.folder_icon = ctk.CTkImage(Image.open("folder.png"), size=(24, 24))

        # Control bar
        control_frame = ctk.CTkFrame(master)
        control_frame.pack(padx=10, pady=5, fill="x")

        self.set_selector = ctk.CTkComboBox(control_frame, values=[str(i) for i in set_ids],
                                            command=self._on_set_selected, width=120)
        self.set_selector.pack(side="left", padx=5)

        ctk.CTkButton(control_frame, text="Dodaj SET", command=self._on_add_set).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Usuń SET", command=self._on_delete_set).pack(side="left", padx=5)

        # Volume control
        volume_frame = ctk.CTkFrame(master)
        volume_frame.pack(pady=5)

        ctk.CTkLabel(volume_frame, text="Głośność:").pack(side="left", padx=5)
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=1, number_of_steps=100,
                                           command=lambda v: self.set_volume_callback(float(v)))
        self.volume_slider.set(1.0)
        self.volume_slider.pack(side="left", padx=5)

        # Indicator
        self.indicator = ctk.CTkLabel(volume_frame, text="", width=20, height=20, fg_color="gray",
                                      corner_radius=10)
        self.indicator.pack(side="left", padx=5)

        # Grid
        self.grid_frame = ctk.CTkFrame(master)
        self.grid_frame.pack(padx=10, pady=10)

        for i in range(9):
            btn = ctk.CTkButton(self.grid_frame,
                                text=f"{i+1}",
                                image=self.folder_icon,
                                compound="top",
                                width=120, height=100,
                                command=lambda idx=i: self.change_sound(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.refresh_grid()

    def refresh_grid(self):
        current_set = self.get_current_set()
        for i in range(9):
            label = current_set[i]["name"] if i < len(current_set) else "(Brak)"
            self.buttons[i].configure(text=f"{i+1}\n{label}")

    def change_sound(self, index):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if file_path:
            self.update_sound(index, file_path)
            self.refresh_grid()

    def set_indicator(self, state):
        self.indicator.configure(fg_color="green" if state else "gray")

    def update_set_selector(self, new_ids):
        self.set_selector.configure(values=[str(i) for i in new_ids])

    def set_selector_value(self, value):
        self.set_selector.set(str(value))

    def _on_set_selected(self, value):
        self.set_current_set_callback(int(value))

    def _on_add_set(self):
        self.add_set_callback()

    def _on_delete_set(self):
        self.delete_set_callback()




def launch_gui(get_current_set_callback, update_sound_callback, set_volume_callback, set_ids, set_current_set_callback, add_set_callback, delete_set_callback):
    root = ctk.CTk()
    gui = SoundboardGUI(root, get_current_set_callback, update_sound_callback,
                        set_volume_callback, set_ids, set_current_set_callback,
                        add_set_callback, delete_set_callback)
    return root, gui