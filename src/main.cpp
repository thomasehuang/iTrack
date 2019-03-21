#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <queue>
#include <stdio.h>
#include <math.h>
#include <string>

#include <sys/types.h>
#include <sys/socket.h>
#include "constants.h"
#include "findEyeCenter.h"
#include "findEyeCorner.h"
#include "history.h"
#include <thread>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>

#include <chrono>
#define PORT 8123


/** Constants **/

int sensitivityCalibration = 0;
double sensitivityValueLeft = 0;
double sensitivityValueRight = 0;
double sensitivityValueUp = 0;


/** Function Headers */
void detectAndDisplay( cv::Mat frame );

/** Global variables */
//-- Note, either copy these two files from opencv/data/haarscascades to your current folder, or change these locations
cv::String face_cascade_name = "../res/haarcascade_frontalface_alt.xml";
// cv::String eye_cascade_name = "../res/haarcascade_eye_tree_eyeglasses.xml";
cv::String eye_cascade_name = "../res/haarcascade_eye.xml";
cv::CascadeClassifier face_cascade;
cv::CascadeClassifier eye_cascade;
std::string main_window_name = "Capture - Face detection";
std::string face_window_name = "Capture - Face";
cv::RNG rng(12345);
cv::Mat debugImage;
cv::Mat skinCrCbHist = cv::Mat::zeros(cv::Size(256, 256), CV_8UC1);

History history(0,0,0,0);
double x = 0;



struct sockaddr_in address; 
int sock = 0, valread; 
struct sockaddr_in serv_addr; 
char *hello = "Hello from client"; 


int sendMsg(char* msg) {
  char buffer[1024] = {0}; 
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
  { 
      printf("\n Socket creation error \n"); 
      return -1; 
  } 

  memset(&serv_addr, '0', sizeof(serv_addr)); 

  serv_addr.sin_family = AF_INET; 
  serv_addr.sin_port = htons(PORT); 
     
  // Convert IPv4 and IPv6 addresses from text to binary form 
  if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)  
  { 
      printf("\nInvalid address/ Address not supported \n"); 
      return -1; 
  } 

  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) 
  { 
      printf("\nConnection Failed \n"); 
      return -1; 
  } 
  send(sock , msg , strlen(msg) , 0 ); 
  valread = read( sock , buffer, 1024); 
  close(sock);
  return 0;
}

void on_trackbar( int, void* ) {
}

/**
 * @function main
 */
int main( int argc, const char** argv ) {
  if(argc > 1) {
    sensitivityCalibration = 1;
  }
  cv::Mat frame;

  // Load the cascades
  if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading face cascade, please change face_cascade_name in source code.\n"); return -1; };
  if( !eye_cascade.load( eye_cascade_name ) ){ printf("--(!)Error loading eye cascade, please change eye_cascade_name in source code.\n"); return -1; };


  cv::namedWindow(face_window_name,cv::WINDOW_NORMAL);
  cv::moveWindow(face_window_name, 10, 100);
  // cv::namedWindow("Sensitivity",cv::WINDOW_NORMAL);

  // cv::createTrackbar( "", "Sensitivity", &history.cutoff, 30, on_trackbar );
  // cv::resizeWindow("Sensitivity", 400,50);


  createCornerKernels();
  ellipse(skinCrCbHist, cv::Point(113, 155.6), cv::Size(23.4, 15.2),
          43.0, 0.0, 360.0, cv::Scalar(255, 255, 255), -1);

  // I make an attempt at supporting both 2.x and 3.x OpenCV
#if CV_MAJOR_VERSION < 3
  CvCapture* capture = cvCaptureFromCAM( 0 );
  if( capture ) {
    while( true ) {
      frame = cvQueryFrame( capture );
#else
  cv::VideoCapture capture(0);
  if( capture.isOpened() ) {
    while( true ) {
      capture.read(frame);
#endif
      // mirror it
      cv::flip(frame, frame, 1);
      frame.copyTo(debugImage);

      // Apply the classifier to the frame
      if( !frame.empty() ) {
        detectAndDisplay( frame );
      }
      else {
        printf(" --(!) No captured frame -- Break!");
        break;
      }

      // imshow(main_window_name,debugImage);

      int c = cv::waitKey(10);
      if( (char)c == 'c' ) { break; }
      if( (char)c == 'f' ) {
        imwrite("frame.png",frame);
      }

    }
  }

  releaseCornerKernels();

  return 0;
}

void runScript(const char* s){
  char s2[] = "python ../commands.py --command ";
  const char* m = strcat(s2, s);
  system(m);
  // system()
}

void findEyes(cv::Mat frame_gray, cv::Rect face) {
  cv::Mat faceROI = frame_gray(face);
  cv::Mat debugFace = faceROI;

  if (kSmoothFaceImage) {
    double sigma = kSmoothFaceFactor * face.width;
    GaussianBlur( faceROI, faceROI, cv::Size( 0, 0 ), sigma);
  }
  //-- Find eye regions and draw them
  int eye_region_width = face.width * (kEyePercentWidth/100.0);
  int eye_region_height = face.width * (kEyePercentHeight/100.0);
  int eye_region_top = face.height * (kEyePercentTop/100.0);
  cv::Rect leftEyeRegion(face.width*(kEyePercentSide/100.0),
                         eye_region_top,eye_region_width,eye_region_height);
  cv::Rect rightEyeRegion(face.width - eye_region_width - face.width*(kEyePercentSide/100.0),
                          eye_region_top,eye_region_width,eye_region_height);

  //-- Find Eye Centers
  cv::Point leftPupil = findEyeCenter(faceROI,leftEyeRegion,"Left Eye");
  cv::Point rightPupil = findEyeCenter(faceROI,rightEyeRegion,"Right Eye");
  std::vector<cv::Rect> eyes;
  // cv::Mat test(faces[0]);

  eye_cascade.detectMultiScale(
              faceROI,
              eyes,
              1.1,
              10,
              0|cv::CASCADE_SCALE_IMAGE|cv::CASCADE_FIND_BIGGEST_OBJECT,
              cv::Size(30, 30));


  cv::Rect leftRightCornerRegion(leftEyeRegion);
  leftRightCornerRegion.width -= leftPupil.x;
  leftRightCornerRegion.x += leftPupil.x;
  leftRightCornerRegion.height /= 2;
  leftRightCornerRegion.y += leftRightCornerRegion.height / 2;
  cv::Rect leftLeftCornerRegion(leftEyeRegion);
  leftLeftCornerRegion.width = leftPupil.x;
  leftLeftCornerRegion.height /= 2;
  leftLeftCornerRegion.y += leftLeftCornerRegion.height / 2;
  cv::Rect rightLeftCornerRegion(rightEyeRegion);
  rightLeftCornerRegion.width = rightPupil.x;
  rightLeftCornerRegion.height /= 2;
  rightLeftCornerRegion.y += rightLeftCornerRegion.height / 2;
  cv::Rect rightRightCornerRegion(rightEyeRegion);
  rightRightCornerRegion.width -= rightPupil.x;
  rightRightCornerRegion.x += rightPupil.x;
  rightRightCornerRegion.height /= 2;
  rightRightCornerRegion.y += rightRightCornerRegion.height / 2;
  rectangle(debugFace,leftRightCornerRegion,200);
  rectangle(debugFace,leftLeftCornerRegion,200);
  rectangle(debugFace,rightLeftCornerRegion,200);
  rectangle(debugFace,rightRightCornerRegion,200);
  // change eye centers to face coordinates
  rightPupil.x += rightEyeRegion.x;
  rightPupil.y += rightEyeRegion.y;
  leftPupil.x += leftEyeRegion.x;
  leftPupil.y += leftEyeRegion.y;
  // draw eye centers
  circle(debugFace, rightPupil, 3, 1234);
  circle(debugFace, leftPupil, 3, 1234);
  //-- Find Eye Corners
  if (kEnableEyeCorner) {
    cv::Point2f leftRightCorner = findEyeCorner(faceROI(leftRightCornerRegion), true, false);
    leftRightCorner.x += leftRightCornerRegion.x;
    leftRightCorner.y += leftRightCornerRegion.y;
    cv::Point2f leftLeftCorner = findEyeCorner(faceROI(leftLeftCornerRegion), true, true);
    leftLeftCorner.x += leftLeftCornerRegion.x;
    leftLeftCorner.y += leftLeftCornerRegion.y;
    cv::Point2f rightLeftCorner = findEyeCorner(faceROI(rightLeftCornerRegion), false, true);
    rightLeftCorner.x += rightLeftCornerRegion.x;
    rightLeftCorner.y += rightLeftCornerRegion.y;
    cv::Point2f rightRightCorner = findEyeCorner(faceROI(rightRightCornerRegion), false, false);
    rightRightCorner.x += rightRightCornerRegion.x;
    rightRightCorner.y += rightRightCornerRegion.y;
    circle(faceROI, leftRightCorner, 3, 200);
    circle(faceROI, leftLeftCorner, 3, 200);
    circle(faceROI, rightLeftCorner, 3, 200);
    circle(faceROI, rightRightCorner, 3, 200);
  }

  int res;

  imshow(face_window_name, faceROI);
  if(eyes.size() == 1) {
    // one eye closed
    if(eyes[0].x < x) {
      res = history.push_back(0);
    }
    else {
      res = history.push_back(1);
    }
  } else if(eyes.size() == 0) {
    // eyes closed
    res = history.push_back(2);
  } else {
    // eyes open
    x = ( eyes[0].x + eyes[1].x ) / 2;
    res = history.handleNewValue(leftPupil.x, leftPupil.y, rightPupil.x,
      rightPupil.y);

  }

  if (sensitivityCalibration == 0) {
    switch(res) {
      case 0:
        std::cout<<"right wink"<<std::endl;
        sendMsg("wright");
        break;
      case 1:
        std::cout<<"left wink"<<std::endl;
        sendMsg("wleft");
        break;
      case 2:
        std::cout<<"eyes closed"<<std::endl;
        sendMsg("closed");
        history.reset();
        break;
      case 3:
        std::cout<<"left"<<std::endl;
        sendMsg("left");
        break;
      case 4:
        std::cout<<"right"<<std::endl;
        sendMsg("right");
        break;
      case 5:
        std::cout<<"up"<<std::endl;
        sendMsg("up");
        break;
      case 6:
        std::cout<<"down"<<std::endl;
        sendMsg("down");
        break;
    }
  }
  else if (sensitivityCalibration == 1) {
    sendMsg("print Welcome to an interactive sensitivity set up. To continue close and reopen your eyes (eyes should be closed for 2-3 seconds).");
    sensitivityCalibration += 1;
  }
  else if (sensitivityCalibration == 2) {
    if(res == 2) {
      sendMsg("print Close your eyes and upon opening them look to the right.");
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 3){
    if(eyes.size() == 2) {
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 4) {
    if(res == 2) {
      sendMsg("print Awsome! Now do the same action but looking to the left now.");
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 5){
    if(eyes.size() == 2) {
      sensitivityValueLeft = leftPupil.x;
      sensitivityValueRight = rightPupil.x;
      sensitivityValueUp = ( leftPupil.y + rightPupil.y ) / 2;
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 6) {
    if(res == 2) {
      sendMsg("print Do the same action one last time looking up.");
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 7){
    if(eyes.size() == 2) {
      sensitivityValueLeft -= leftPupil.x;
      sensitivityValueRight -= rightPupil.x;
      sensitivityValueUp += ( leftPupil.y + rightPupil.y ) / 2;
      sensitivityValueLeft = sensitivityValueLeft/2;
      sensitivityValueRight = sensitivityValueRight/2;
      sensitivityValueUp = sensitivityValueUp/2;
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 8) {
    if(res == 2) {
      sendMsg("print You're all done!");
      sensitivityCalibration += 1;
    }
  }
  else if (sensitivityCalibration == 9){
    if(eyes.size() == 2) {
      sensitivityCalibration +=1;
    }

  }
  else if (sensitivityCalibration == 10){
    sendMsg("print~");
    sensitivityValueUp =( ( leftPupil.y + rightPupil.y ) / 2) - sensitivityValueUp;
    history.cutoff = 30.0 - (.6*((sensitivityValueLeft + sensitivityValueRight)/2));
    std::cout<<history.cutoff<<std::endl;
    sensitivityCalibration = 0;
  }



  // cv::waitKey(10);
//  cv::Rect roi( cv::Point( 0, 0 ), faceROI.size());
//  cv::Mat destinationROI = debugImage( roi );
//  faceROI.copyTo( destinationROI );
}


cv::Mat findSkin (cv::Mat &frame) {
  cv::Mat input;
  cv::Mat output = cv::Mat(frame.rows,frame.cols, CV_8U);

  cvtColor(frame, input, cv::COLOR_BGR2GRAY);

  for (int y = 0; y < input.rows; ++y) {
    const cv::Vec3b *Mr = input.ptr<cv::Vec3b>(y);
//    uchar *Or = output.ptr<uchar>(y);
    cv::Vec3b *Or = frame.ptr<cv::Vec3b>(y);
    for (int x = 0; x < input.cols; ++x) {
      cv::Vec3b ycrcb = Mr[x];
//      Or[x] = (skinCrCbHist.at<uchar>(ycrcb[1], ycrcb[2]) > 0) ? 255 : 0;
      if(skinCrCbHist.at<uchar>(ycrcb[1], ycrcb[2]) == 0) {
        Or[x] = cv::Vec3b(0,0,0);
      }
    }
  }
  return output;
}

/**
 * @function detectAndDisplay
 */
void detectAndDisplay( cv::Mat frame ) {
  std::vector<cv::Rect> faces;
  //cv::Mat frame_gray;

  std::vector<cv::Mat> rgbChannels(3);
  cv::split(frame, rgbChannels);
  cv::Mat frame_gray = rgbChannels[2];

  //cvtColor( frame, frame_gray, CV_BGR2GRAY );
  //equalizeHist( frame_gray, frame_gray );
  //cv::pow(frame_gray, CV_64F, frame_gray);
  //-- Detect faces
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|cv::CASCADE_SCALE_IMAGE|cv::CASCADE_FIND_BIGGEST_OBJECT, cv::Size(150, 150) );
//  findSkin(debugImage);



  for( int i = 0; i < faces.size(); i++ )
  {
    rectangle(debugImage, faces[i], 1234);
  }
  //-- Show what you got

  if (faces.size() > 0) {
    auto max = faces[0].width;
    int pos = 0;
    for(int i = 1; i < faces.size(); i++){
      if(faces[i].width > max){
        max = faces[i].width;
        pos = i;
      }
    }
    findEyes(frame_gray, faces[0]);
  }
}
