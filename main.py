from TkZero.MainWindow import MainWindow


class TimestampConverter(MainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Timestamp Converter"
        self.hide()
        self.bind_shift_keys()

    def bind_shift_keys(self):
        """
        Create binds to detect whether shift key is pressed or not.
        """
        self.shift_pressed = False
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
        print(pressed)

    def hide(self):
        """
        Withdraw the window.
        """
        self.withdraw()

    def show(self):
        """
        Bring the window back.
        """
        self.deiconify()
        self.lift()


tsc = TimestampConverter()
tsc.mainloop()
