#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(){
    int server;
    server = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in config;
    memset(&config, 0, sizeof(config));
    config.sin_addr.s_addr = inet_addr("127.0.0.1");
    config.sin_family = AF_INET;
    config.sin_port = htons(24242);
    
    connect(server, (struct sockaddr*)&config, sizeof(config));
    
    char name[80];
    printf("Nazwa:\n");
    //fgets(name, 75, stdin);
    scanf("%s", name);
    //name[strlen(name)-1] = '\0';
    
    char nulc = '\0';
    
    send(server, name, strlen(name), 0);
    send(server, &nulc, 1, 0);
    
    printf("Użytkownicy:\n");
    while (1){
        char got;
        int res = recv(server, &got, 1, 0);
        if (got == '\0'){
            break;
        }
        printf("%c", got);
    }
    printf("Wysyłaj wiadomości pisząc '<Adresat> <Wiadomosc><enter>'\n");
    while (1){
        int maxfd = server;
        fd_set monitored;
        FD_ZERO(&monitored);
        FD_SET(STDIN_FILENO, &monitored);
        FD_SET(server, &monitored);
        
        select(maxfd+1, &monitored, NULL, NULL, NULL);
        
        if (FD_ISSET(STDIN_FILENO, &monitored)){
            char target[95];
            scanf("%s", target);
            char mess[1000];
            fgets(mess, 980, stdin);
            send(server, target, strlen(target)+1, 0);
            send(server, mess+1, strlen(mess), 0);
        }
        
        if (FD_ISSET(server, &monitored)){
            while (1){
                char red;
                int retstat = recv(server, &red, 1, 0);
                if (red == '\0'){
                    break;
                }
                printf("%c", red);
            }
        }
        
    }
    return 0;
}
