#include <iostream>
#include <chrono>
#include <thread>
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

int sendMsg(char* msg) {
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }
    send(sock, msg, strlen(msg), 0);
    valread = read(sock, buffer, 1024);
    close(sock);
    return 0;
}

void test_news() {
    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    sendMsg("up");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));


    sendMsg("right");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("up");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("right");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("right");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("up");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("right");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    sendMsg("up");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    sendMsg("wright");
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
}

int main() {
    char* test = new char[100];
    while(std::cin >> test) {
        if (strcmp(test, "test_news") == 0) {
            test_news();
        } else {
            sendMsg(test);
        }
    }
    return 0;
}
