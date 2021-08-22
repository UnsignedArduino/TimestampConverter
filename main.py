import tkinter as tk

import arrow
from TkZero.Entry import Entry
from TkZero.Label import Label
from TkZero.MainWindow import MainWindow


class TimestampConverter(MainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Timestamp Converter"
        self.resizable(False, False)
        self.make_gui()
        self.on_close = self.close_window
        self.shown = False
        self.hide()

        self.shift_pressed = False
        self.bind_shift_keys()

        self.last_cb_entry = self.clipboard_get()
        self.check_for_new_clipboard_entry()

    def make_gui(self):
        """
        Make the GUI.
        """
        self.ts_label = Label(parent=self, text="Timestamp detected:")
        self.ts_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_entry = Entry(parent=self, width=30)
        self.ts_entry.read_only = True
        self.ts_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_label = Label(parent=self, text="Absolute date: ")
        self.ts_abs_label.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_abs_entry = Entry(parent=self, width=30)
        self.ts_abs_entry.read_only = True
        self.ts_abs_entry.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW)

        self.ts_rel_label = Label(parent=self, text="Relative to now: ")
        self.ts_rel_label.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW)

        self.ts_rel_entry = Entry(parent=self, width=30)
        self.ts_rel_entry.read_only = True
        self.ts_rel_entry.grid(row=2, column=1, padx=1, pady=1, sticky=tk.NW)

    def check_for_new_clipboard_entry(self, reschedule: int = 1000):
        """
        Checks for a new clipboard entry.

        :param reschedule: How many milliseconds to wait before executing
         again. Send a number less then 0 to cancel.
        """
        current_cb_entry = self.clipboard_get()
        if current_cb_entry != self.last_cb_entry:
            self.last_cb_entry = current_cb_entry
            filtered_entry = current_cb_entry.replace(",", "").replace(".", "")
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

        self.ts_entry.read_only = False
        self.ts_entry.value = str(timestamp)
        self.ts_entry.read_only = True

        self.ts_abs_entry.read_only = False
        date_format = "HH:mm:ss ddd, MMM Do, YYYY"
        self.ts_abs_entry.value = arrow.get(timestamp).format(date_format)
        self.ts_abs_entry.read_only = True

        self.update_relative_ts(timestamp)

    def update_relative_ts(self, timestamp: float):
        """
        Update the relative timestamp every second until the window is hidden.

        :param timestamp: A float.
        """
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

    def bind_shift_keys(self):
        """
        Create binds to detect whether shift key is pressed or not.
        """
        self.bind_to_event("<Shift_L>", lambda _: self.set_shift_state(True))
        self.bind_to_event("<Shift_R>", lambda _: self.set_shift_state(True))
        self.bind_to_event("<KeyRelease-Shift_L>", lambda _: self.set_shift_state(False))
        self.bind_to_event("<KeyRelease-Shift_R>", lambda _: self.set_shift_state(False))

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
