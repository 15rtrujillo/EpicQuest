from collections import deque

import tkinter as tk


class TextToAdd:
    """Text to be added to the screen"""

    def __init__(self, text: str, end: str):
        self.text = text
        self.end = end
        self.total_delay = 10


class TextToTW(TextToAdd):
    """Text to be typewritten to the screen"""

    def __init__(self, text: str, delay: int, end: str):
        super().__init__(text, end)
        self.delay = delay
        self.total_delay = delay * len(text) + 250
        self.running = False


class TextManager:
    """An object to manage the text that gets added to the textbox"""

    def __init__(self, root: tk.Tk, textbox: tk.Text):
        self.root = root
        self.textbox = textbox
        self.queue: deque[TextToAdd] = deque()

    def add(self, text: TextToAdd):
        """Add text to the queue to be added to the screen"""
        self.running = True
        delay = self.get_total_delay()
        self.queue.append(text)       
        if isinstance(text, TextToTW):
            self.root.after(delay, self.typewrite_text, text)
        elif isinstance(text, TextToAdd):
            self.root.after(delay, self.add_text, text)

    def add_text(self, text: TextToAdd):
        self.textbox.insert("end", text.text + text.end)
        self.queue.remove(text)
        if len(self.queue) == 0:
                self.running = False

    def typewrite_text(self, text: TextToTW, index: int = 0):
        self.textbox.insert("end", text.text[index])
        index += 1
        if index < len(text.text):
            self.root.after(text.delay, self.typewrite_text, text, index)
        else:
            # If there's nothing else to typewrite, add the ending character
            self.textbox.insert("end", text.end)
            self.queue.remove(text)
            if len(self.queue) == 0:
                self.running = False

    def get_total_delay(self):
        return sum([item.total_delay for item in self.queue])
