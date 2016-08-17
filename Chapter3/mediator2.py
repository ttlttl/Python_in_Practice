"""
中介者模式，使用协程
"""


from Qtrac import coroutine


class Form:
    def __init__(self):
        self.create_widgets()
        self.create_mediator()

    def create_widgets(self):
        self.nameText = Text()
        self.emailText = Text()
        self.okButton = Button("OK")
        self.cancelButton = Button("Cancel")

    def create_mediator(self):
        self.mediator = self._update_ui_mediator(self._clicked_mediator())
        for widget in (self.nameText, self.emailText, self.okButton, self.cancelButton):
            widget.mediator = self.mediator
        self.mediator.send(None)

    @coroutine
    def _update_ui_mediator(self, successor=None):
        while True:
            widget = (yield)
            self.okButton.enabled = (bool(self.nameText.text) and bool(self.emailText.text))
            if successor is not None:
                successor.send(widget)

    @coroutine
    def _clicked_mediator(self, successor=None):
        while True:
            widget = (yield)
            if widget == self.okButton:
                print("OK")
            elif widget == self.cancelButton:
                print("Cancel")
            elif successor is not None:
                successor.send(widget)


class Mediated:
    def __init__(self):
        self.mediator = None

    def on_change(self):
        if self.mediator is not None:
            self.mediator.send(self)


class Button(Mediated):
    def __init__(self, text=""):
        super().__init__()
        self.enabled = True
        self.text = text

    def click(self):
        if self.enabled:
            self.on_change()

    def __str__(self):
        return "Button({!r}) {}".format(self.text,
                                        "enabled" if self.enabled else "disabled")


class Text(Mediated):
    def __init__(self, text=""):
        super().__init__()
        self.__text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if self.text != text:
            self.__text = text
            self.on_change()

    def __str__(self):
        return "Text({!r})".format(self.text)


def test_user_interaction_with(form):
    form.okButton.click()  # Ignored because it is disabled
    print(form.okButton.enabled)  # False
    form.nameText.text = "ttlttl"
    print(form.okButton.enabled)  # False
    form.emailText.text = "wangmingape@gmail.com"
    print(form.okButton.enabled)  # True
    form.okButton.click()  # OK
    form.emailText.text = ""
    print(form.okButton.enabled)  # False
    form.cancelButton.click()  # Cancel


def main():
    form = Form()
    test_user_interaction_with(form)


if __name__ == "__main__":
    main()


