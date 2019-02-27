#include <iostream>
#include <chrono>
#include <iostream>
#include <queue>
#include <stdio.h>
#include <math.h>
#include <string>

#include <sys/types.h>
#include <sys/socket.h>
#include <thread>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#define PORT 8123

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

int main() {
    char* test;
    while(std::cin>>test) {
        sendMsg(test);
    }
    return 0;
}