import os.path
import socket
import pyautogui
from tkinter import *


"""
Commands:
    mc  - mouse click
    if  - increase font
    df  - decrease font
    pu  - page up
    pd  - page down
    ss  - screenshot

You can chain together commands by separating them with the '|' character.
Commands will be executed in the order they are written.
For example, 'mc | df' will click the mouse then decrease the font size.
"""
CMD2NAME = {
    'mc': 'Mouse Click',
    'if': 'Increase Font',
    'df': 'Decrease Font',
    'pu': 'Page Up',
    'pd': 'Page Down',
    'ss': 'Screenshot',
}

# Commmand functions
def mouse_click():
    pyautogui.click()

def increase_font():
    pyautogui.hotkey('command', '+')

def decrease_font():
    pyautogui.hotkey('command', '-')

def page_up():
    pyautogui.scroll(20)

def page_down():
    pyautogui.scroll(-20)

def screenshot():
    if os.path.isfile('screenshot.png'):
        count = 0
        while True:
            fname = 'screenshot_%i.png' % (count)
            if not os.path.isfile('screenshot_%i.png' % (count)):
                pyautogui.screenshot(fname)
                break
            count += 1
    else:
        pyautogui.screenshot('screenshot.png')


# Helper functions
def parse_commands(commands):
    commands = commands.split('|')
    commands = [command.strip() for command in commands]
    return commands

class Mode:
    def __init__(self, name):
        self.name = name
        self.commands = {}

    def set_command(self, movement, name, func, *args):
        self.commands[movement] = [func, name, args]

    def execute(self,movement):
        self.commands[movement][0](*self.commands[movement][2])

reader_mod = Mode("reader")
reader_mod.set_command("left", "Decrease Font", pyautogui.hotkey,'command', '-')
reader_mod.set_command("right", "Increase Font", pyautogui.hotkey,'command', '+')
reader_mod.set_command("wright", "Page Down", page_down)
reader_mod.set_command("wleft", "Page Up", page_up)

# reader_mod.execute("right")
modes = [reader_mod]
mode_pos = 0


if __name__ == '__main__':
    viz = True
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.bind(("localhost", 8123))
    socks.listen(5)
    while 1:
        client = socks.accept()[0]
        message = client.recv(1024)
        client.send(str("recieved").encode("utf-8"))
        commands = [message.decode('ascii')]

        # commands = parse_commands(args.command)
        for command in commands:
            if commands[0] in modes[mode_pos].commands:
                modes[mode_pos].execute(command)
        if viz:
            if commands[0] in modes[mode_pos].commands:
                c = modes[mode_pos].commands[commands[0]][1]
                window = Tk()
                window.title('iTrack')
                w, h = 225, 50
                ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
                window.geometry('%ix%i+%i+%i' % (w,h,ws-w-50,hs-h-50))
                window.after(3000, lambda: window.destroy())
                lbl = Label(window, text=c, font=("Arial", 30))
                lbl.grid(column=0, row=0)
                window.columnconfigure(0, weight=1)
                window.rowconfigure(0, weight=1)
                window.mainloop()

        client.close()
