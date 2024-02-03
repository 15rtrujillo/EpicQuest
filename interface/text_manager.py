from collections import deque


import tkinter as tk


class TextToAdd:
    """Text to be added to the screen"""

    def __init__(self, text: str, end: str):
        """
        An object that stores text to add to the screen
        :param str text: THe text to add
        :param str end: The character to append to the end of the text
        """
        self.text = text
        self.end = end
        self.total_delay = 10


class TextToTW(TextToAdd):
    """Text to be typewritten to the screen"""

    def __init__(self, text: str, delay: int, end: str):
        """
        An object that stores text to typewrite to the screen
        :param str text: THe text to add
        :param int delay: The delay between adding each character to the screen
        :param str end: The character to append to the end of the text
        """
        super().__init__(text, end)
        self.delay = delay
        self.total_delay = delay * len(text) + 250
        self.running = False


class TextManager:
    """An object to manage the text that gets added to the textbox"""

    def __init__(self, root: tk.Tk, textbox: tk.Text):
        """
        Create a new Text Manager
        :param tk.Tk root: The tkinter root associated with this text manager
        :param tk.Text textbox: A textbox to add text to
        """
        self.root = root
        self.textbox = textbox
        self.queue: deque[TextToAdd] = deque()
        self.running = False

    def add(self, text: TextToAdd):
        """
        Add text to the queue to be added to the screen
        :param TextToAdd text: The text to be added to the queue
        """
        self.running = True
        delay = self.__get_total_delay()
        self.queue.append(text)       
        if isinstance(text, TextToTW):
            self.root.after(delay, self.__typewrite_text, text)
        elif isinstance(text, TextToAdd):
            self.root.after(delay, self.__add_text, text)

    def __add_text(self, text: TextToAdd):
        """
        Display text to the text box
        :param TextToAdd text: THe text to add to the text box
        """
        self.textbox.insert("end", text.text + text.end)
        self.queue.remove(text)
        if len(self.queue) == 0:
            self.running = False

    def __typewrite_text(self, text: TextToTW, index: int = 0):
        """
        Typewrite text to the text box
        :param TextToTW text: The text to be typewritten
        :param index: The position of the character to add
        """
        self.textbox.insert("end", text.text[index])
        index += 1
        if index < len(text.text):
            self.root.after(text.delay, self.__typewrite_text, text, index)
        else:
            # If there's nothing else to typewrite, add the ending character
            self.textbox.insert("end", text.end)
            self.queue.remove(text)
            if len(self.queue) == 0:
                self.running = False

    def __get_total_delay(self) -> int:
        """
        Get the total delay for all current items in the queue
        :rtype: int
        :return: The total delay for all the TextToAdd objects in the queue
        """
        return sum([item.total_delay for item in self.queue])
