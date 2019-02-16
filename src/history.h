#include <iostream>

class History {
    History() {}
    History(double x1, double y1, double x2, double y2): leftx(x1), lefty(y1), rightx(x2), righty(y2) {}

    void handleNewValue(double x1, double y1, double x2, double y2) {
        if (leftx==0){
            leftx = x1;
            lefty = y1;
            rightx = x2;
            righty = y2;
        }
        else if(x - leftPupil.x > cutoff && w - rightPupil.x > cutoff) {
            std::cout<<"left"<<std::endl;
            // runScript("pu");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
        else if( leftPupil.x - x > cutoff && rightPupil.x - w  > cutoff) {
            std::cout<<"right"<<std::endl;
            // runScript("pd");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
        else if(y - leftPupil.y > cutoff && z - rightPupil.y > cutoff) {
            std::cout<<"up"<<std::endl;
            // runScript("pu");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            x = 0;
        }
        else if( leftPupil.y -y > cutoff && rightPupil.y - z > cutoff) {
            std::cout<<"down"<<std::endl;

            // runScript("pd");
            std::this_thread::sleep_for(std::chrono::milliseconds(waitTime));
            // x = 0;
        }
    }


    double leftx;
    double lefty;
    double rightx;
    double righty;
    double cutoff = 10.0;
    int waitTime = 1000
    char last;
};