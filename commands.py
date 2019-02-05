import argparse
import os.path
import pyautogui


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command', type=str,
                    help='command to run')

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

if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'increase_font':
        increase_font()
    elif args.command == 'decrease_font':
        decrease_font()
    elif args.command == 'page_up':
        page_up()
    elif args.command == 'page_down':
        page_down()
    elif args.command == 'screenshot':
        screenshot()
