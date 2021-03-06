# iTrack

Eye tracking for accessibility.

## Demo Videos

[Browsing Reddit](https://drive.google.com/file/d/1jGc8VChGGwNRNNVF9BCtkZVZOSYnJPvi/view?usp=sharing)

[Opening a video](https://drive.google.com/file/d/13hMo0tsL6tk6rKjOoj6xIxViYIFEgveX/view?usp=sharing)

[Setup Tutorial](https://drive.google.com/open?id=1EwiEe1INtsU5r0KwHCujp7-T_bhfWiim)

[Walkthrough Tutorial](https://drive.google.com/open?id=1CjY-SZ2-PhIgjgNnKxEUALwUfRLTiOza)

[Usage Demo (no talking)](https://drive.google.com/open?id=1sY4h3UH0sLCuZa52cP-AxpiEmb73R2iX)

## Table of Contents  
   * [Installation](#installation)
      * [Installing C++ Code](#installing-c-code)
      * [Installing Python Code](#installing-python-code)
   * [Running and Usage](#running-and-usage)
   * [Troubleshooting](#troubleshooting)

## Installation

Our software currently only works on MacOS computers, so the installation instructions listed here will be for MacOS users.

### Installing C++ Code

If not already installed, please install CMake and OpenCV

To install CMake:
```
brew install cmake
```

Links for instructions on how to install OpenCV on OSX can be found [here](http://charliegerard.github.io/blog/Installing-OpenCV/).

Once everything is installed, use the following commands to generate the executable:
```
mkdir build
cd build
cmake ../
make
```

### Installing Python Code

For this project, we use Python 3.6.

(Optional) It is recommended that you create a virtual environment first (installation instructions [here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)). Enter the following commands to create a virtual environment and activate it:
```
python3 -m virtualenv env
source env/bin/activate
```

We will use pip to install all the necessary packages for Python. Enter the following command:
```
pip3 install -r requirements.txt
```

To interface with commands on a computer, we use [PyAutoGUI](https://github.com/asweigart/pyautogui). If you get an error that says something in the lines of ```ModuleNotFoundError: No module named 'Quartz'```, go to the accessibility tab in your privacy settings and enable permissions for your terminal.

<!--- For Windows and Linux users, you can follow the installation instructions [here](https://pyautogui.readthedocs.io/en/latest/install.html). --->

## Running and Usage

To start up the program, you will need to run two executables at the same time.

to start up the pupil tracking:
```
cd build
./bin/iTrack
```
* Note: when you start this program, it is important that the user is looking at the center of their screen.
* Running iTrack with -s will start a setup process for a custom sensitivity.

To start up front end code:
```
python commands.py
```
* Note: Running with the -v flag will enable the "voice" feature, which will speak all commands that get executed.

After both files are running, you should be able to use your eye movements to control your computer.

There are 6 main actions that will trigger events:
1. Look left
2. Look right
3. Look Up
4. Left Wink
5. Right Wink
6. Close Eyes
* Note: it takes approximatly 1 second for each action to be recognized, so you have to hold the action for that duration.

Closing your eyes will recalibrate the eye center. If you think commands are triggering when they shouldn't be or aren't triggering when they should be, close your eyes and then look at the center of the screen.

Looking up toggles the help menu, where you can see the current mode you are using. In the help menu, looking left or right will switch modes. Winking with your left eye will lock or unlock the system. When the system is locked, no commands will be triggered with any eye movement.

All other commands are dependent on what mode you are in, and the functions of each command are described in the help menu.

### Modes

We support modes, which allow you to have different mappings from the actions (look left, look right, left wink, right wink) to commands on the computer. By default, we support three modes: reader, watcher, and navigational. The action mappings are listed below:

| | Look Left | Look Right | Left Wink | Right Wink | Notes |
| - | - | - | - | - | - |
| **Reader** | Decrease Font | Increase Font | Page Up | Page Down | |
| **Navigational** | Back | Enter | Next | Previous | Works best with Google Chrome. |
| **Watcher** | Decrease Volume | Increase Volume | Fullscreen | Pause | Works best with YouTube. |
| **URL** | Open Reddit | Open Gmail | Open Youtube | Open NY Times | |

Users can also make their own custom modes with custom commands. To enter the custom mode creater, execute a right wink command while in the help menu.

## Troubleshooting

- We encountered some issue with Anaconda and Tkinter. Switching to Python 3 resolved the issue.
