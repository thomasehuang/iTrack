#include <iostream>
#include <thread>
#include <chrono>
#include <deque>

class History {
public:
    History() {}
    History(double x1, double y1, double x2, double y2): leftx(x1), lefty(y1), rightx(x2), righty(y2) {}

    int handleNewValue(double x1, double y1, double x2, double y2) {
        int res = -1;
        if (leftx==-1){
            leftx = 0;
        }
        if (leftx==0){
            leftx = x1;
            lefty = y1;
            rightx = x2;
            righty = y2;
        }
        else if(leftx - x1 > cutoff && rightx - x2 > cutoff) {
            res = push_back(3);
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
        }
        else if( x1 - leftx > cutoff && x2 - rightx  > cutoff) {
            res = push_back(4);
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
        }
        else if(lefty - y1 > cutoff/2 && righty - y2 > cutoff/2) {
            res = push_back(5);
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
        }
        else if( y1 - lefty > cutoff && y2 - righty > cutoff) {
            res = push_back(6);
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
        }
        return res;
    }

    void reset(){
        std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
        leftx = -1;
    }

    int push_back(int cmd) {
        if (cmds.size() == frames) {
            int res = check_frames();
            if (res != -1) {
                cmds.clear();
                return res;
            } else {
                cmds.pop_front();
                cmds.push_back(cmd);
                return -1;
            }
        } else {
            cmds.push_back(cmd);
            return -1;
        }
    }

    int check_frames() {
        int count;
        for (int i=0; i<frames; i++) {
            if (cmds[i] == -1) {
                continue;
            }
            count=0;
            for (int j=0 ; j<frames ; j++) {
                if (cmds[i] == cmds[j]) count++;
            }
            if (count > threshold) {
                return cmds[i];
            }
        }
        return -1;
    }

    double leftx;
    double lefty;
    double rightx;
    double righty;
    double cutoff = 8.0;
    int waitTime = 10;
    int frames = 10;
    int threshold = 8;
    char last;
    std::deque<int> cmds; 
};