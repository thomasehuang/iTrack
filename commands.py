import argparse
import os.path
import pyautogui


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command', type=str,
                    help='Commands to run.')

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


if __name__ == '__main__':
    args = parser.parse_args()
    commands = parse_commands(args.command)
    for command in commands:
        if command == 'mc':
            mouse_click()
        elif command == 'if':
            increase_font()
        elif command == 'df':
            decrease_font()
        elif command == 'pu':
            page_up()
        elif command == 'pd':
            page_down()
        elif command == 'ss':
            screenshot()
