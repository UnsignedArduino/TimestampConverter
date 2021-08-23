import tkinter as tk
from pathlib import Path

import arrow
from PIL import Image
from TkZero.Entry import Entry
from TkZero.Label import Label
from TkZero.MainWindow import MainWindow
from pystray import Icon, Menu, MenuItem
from threading import Thread

date_format = "HH:mm:ss ddd, MMM Do, YYYY"


class TimestampConverter(MainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Timestamp Converter"
        self.make_gui()
        self.update()
        self.resizable(False, False)
        icon_path = Path.cwd() / "icon.ico"
        assert icon_path.exists()
        self.iconbitmap(str(icon_path))
        self.on_close = self.close_window
        self.shown = False
        self.hide()

        self.shift_pressed = False
        self.bind_to_event("<Shift_L>", lambda _: self.set_shift_state(True))
        self.bind_to_event("<Shift_R>", lambda _: self.set_shift_state(True))
        self.bind_to_event("<KeyRelease-Shift_L>", lambda _: self.set_shift_state(False))
        self.bind_to_event("<KeyRelease-Shift_R>", lambda _: self.set_shift_state(False))

        self.last_cb_entry = self.clipboard_get()
        self.check_for_new_clipboard_entry()

        image = Image.open(icon_path)
        menu = Menu(MenuItem("Quit", self.destroy))
        self.icon = Icon("name", image, "Timestamp Converter", menu)
        # This won't work on macOS cause macOS' tray icon implementation
        # requires that icon runs in the main thread but Tkinter also needs
        # to run in the main thread. So we sacrifice macOS compatibility.
        t = Thread(target=self.icon.run, daemon=True)
        t.start()

    def make_gui(self):
        """
        Make the GUI.
        """
        self.ts_label = Label(parent=self, text="Detected timestamp: ")
        self.ts_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_entry = Entry(parent=self, width=30)
        self.ts_entry.read_only = True
        self.ts_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_now_label = Label(parent=self, text="Timestamp now: ")
        self.ts_now_label.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_now_entry = Entry(parent=self, width=30)
        self.ts_now_entry.read_only = True
        self.ts_now_entry.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_label = Label(parent=self, text="Detected absolute date: ")
        self.ts_abs_label.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_entry = Entry(parent=self, width=30)
        self.ts_abs_entry.read_only = True
        self.ts_abs_entry.grid(row=2, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_now_label = Label(parent=self, text="Date now: ")
        self.ts_abs_now_label.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_now_entry = Entry(parent=self, width=30)
        self.ts_abs_now_entry.read_only = True
        self.ts_abs_now_entry.grid(row=3, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_rel_label = Label(parent=self, text="Detected relative to now: ")
        self.ts_rel_label.grid(row=4, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_rel_entry = Entry(parent=self, width=30)
        self.ts_rel_entry.read_only = True
        self.ts_rel_entry.grid(row=4, column=1, padx=1, pady=1, sticky=tk.NW)

    def check_for_new_clipboard_entry(self, reschedule: int = 1000):
        """
        Checks for a new clipboard entry.

        :param reschedule: How many milliseconds to wait before executing
         again. Send a number less then 0 to cancel.
        """
        current_cb_entry = self.clipboard_get()
        if current_cb_entry != self.last_cb_entry:
            self.last_cb_entry = current_cb_entry
            filtered_entry = current_cb_entry.replace(",", "").replace(".", "").replace(" ", "")
            if filtered_entry.isnumeric():
                self.show_timestamp(float(current_cb_entry))
        if reschedule >= 0:
            self.after(reschedule, self.check_for_new_clipboard_entry)

    def show_timestamp(self, timestamp: float):
        """
        Show the main window.

        :param timestamp: A float.
        """
        self.position = self.winfo_pointerxy()

        self.show()

        self.update_now_ts()

        self.ts_entry.read_only = False
        self.ts_entry.value = str(timestamp)
        self.ts_entry.read_only = True

        self.ts_abs_entry.read_only = False
        self.ts_abs_entry.value = arrow.get(timestamp).format(date_format)
        self.ts_abs_entry.read_only = True

        self.update_date_now()

        self.update_relative_ts(timestamp)

    def update_now_ts(self):
        """
        Update the now timestamp every second until the window is hidden.
        """
        if not self.ts_now_entry.selection_present():
            self.ts_now_entry.read_only = False
            self.ts_now_entry.value = str(arrow.now().timestamp())
            self.ts_now_entry.read_only = True

        if self.shown:
            self.after(50, self.update_now_ts)

    def update_date_now(self):
        """
        Update the date now every second until the window is hidden.
        """
        if not self.ts_abs_now_entry.selection_present():
            self.ts_abs_now_entry.read_only = False
            self.ts_abs_now_entry.value = str(arrow.now().format(date_format))
            self.ts_abs_now_entry.read_only = True

        if self.shown:
            self.after(1000, self.update_date_now)

    def update_relative_ts(self, timestamp: float):
        """
        Update the relative timestamp every second until the window is hidden.

        :param timestamp: A float.
        """
        if not self.ts_rel_entry.selection_present():
            self.ts_rel_entry.read_only = False
            self.ts_rel_entry.value = arrow.get(timestamp).humanize()
            self.ts_rel_entry.read_only = True

        if self.shown:
            self.after(1000, lambda: self.update_relative_ts(timestamp))

    def close_window(self):
        """
        Close the window.
        """
        if self.shift_pressed:
            self.destroy()
        else:
            self.hide()

    def destroy(self):
        self.icon.stop()
        super().destroy()

    def set_shift_state(self, pressed: bool):
        """
        Set whether the shift key is pressed or not.

        :param pressed: A bool.
        """
        self.shift_pressed = pressed

    def hide(self):
        """
        Withdraw the window.
        """
        self.withdraw()
        self.shown = False

    def show(self):
        """
        Bring the window back.
        """
        self.deiconify()
        self.lift()
        self.shown = True


tsc = TimestampConverter()
tsc.mainloop()
