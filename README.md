# iTrack

Eye tracking for accessibility.

## Table of Contents  
   * [Installation](#installation)
      * [Installing C++ Code](#installing-c-code)
      * [Installing Python Code](#installing-python-code)
   * [Running and Usage](#running-and-usage)

## Installation

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

To interface with commands on a computer, we use [PyAutoGUI](https://github.com/asweigart/pyautogui). For Mac users, type the following commands into a terminal to install PyAutoGUI:

```
pip3 install pyobjc-core
pip3 install pyobjc
pip3 install pyautogui
```

If you get an error that says something in the lines of ```ModuleNotFoundError: No module named 'Quartz'```, please go to the accessibility tab in your privacy settings and enable permissions for your terminal.

<!--- For Windows and Linux users, you can follow the installation instructions [here](https://pyautogui.readthedocs.io/en/latest/install.html). --->

## Running and Usage

To start up the program, you will need to run two executables at the same time.

to start up the pupil tracking:
```
cd build
./bin/iTrack
```
* Note: when you start this program, it is important that the user is looking at the center of their screen.

To start up front end code:
```
python commands.py
```

Once running, there are 6 main actions that will trigger events:
1. Look left
2. Look right
3. Look Up
4. Close Eyes
5. Right Wink
6. Left Wink
* Note: it takes approximatly 1 second for each action to be recognized, so you have to hold the action for that duration.

Closing your eyes will recalibrate the eye center. If you think commands are triggering when they shouldn't be or aren't triggering when they should be, close your eyes and then look at the center of the screen. Closing your eyes will also close the help menu when it is open.

Looking up opens the help menu, where you can see the current mode you are using. In the help menu, looking left or right will switch modes.

All other commands are dependent on what mode you are in, and the functions of each command are described in the help menu.
