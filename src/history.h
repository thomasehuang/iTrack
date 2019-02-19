#include <iostream>
#include <thread>
#include <chrono>

class History {
public:
    History() {}
    History(double x1, double y1, double x2, double y2): leftx(x1), lefty(y1), rightx(x2), righty(y2) {}

    void handleNewValue(double x1, double y1, double x2, double y2) {
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
            std::cout<<"left"<<std::endl;
            // runScript("pu");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
        else if( x1 - leftx > cutoff && x2 - rightx  > cutoff) {
            std::cout<<"right"<<std::endl;
            // runScript("pd");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
        else if(lefty - y1 > cutoff && righty - y2 > cutoff) {
            std::cout<<"up"<<std::endl;
            // runScript("pu");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // leftx = 0;
        }
        else if( y1 - lefty > cutoff && y2 - righty > cutoff) {
            std::cout<<"down"<<std::endl;

            // runScript("pd");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
    }

    void reset(){
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        leftx = -1;
    }

    double leftx;
    double lefty;
    double rightx;
    double righty;
    double cutoff = 8.0;
    int waitTime = 10;
    char last;
};