# iTrack

Eye tracking for accessibility.

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

For Windows and Linux users, you can follow the installation instructions [here](https://pyautogui.readthedocs.io/en/latest/install.html).
