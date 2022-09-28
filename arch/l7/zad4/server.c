#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>

struct client {
    int sock_fd;
    char name[100];
    int state;
    SSL* sconn;
};

int main(){
    SSL_CTX* sslctx;
    
    SSL_load_error_strings();
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    
    sslctx = SSL_CTX_new( TLS_server_method());
    SSL_CTX_set_options(sslctx, SSL_OP_SINGLE_DH_USE);
    SSL_CTX_use_certificate_file(sslctx, "./serv.crt", SSL_FILETYPE_PEM);
    SSL_CTX_use_PrivateKey_file(sslctx, "./serv.key", SSL_FILETYPE_PEM);
    
    int server_socket_fd;
    server_socket_fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, IPPROTO_IP);
    
    struct sockaddr_in server_config;
    bzero((char*)&server_config, sizeof(server_config));
    server_config.sin_family = AF_INET;
    server_config.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_config.sin_port = htons(24242);
    
    bind(server_socket_fd, (struct sockaddr*)&server_config, sizeof(server_config));
    
    listen(server_socket_fd, 3);
    
    int clinum = 0;
    struct client* clients = malloc(sizeof(struct client) * 2);
    
    int run = 1;
    
    while(run){
        printf("Iteracja\n");
        int maxfd = server_socket_fd;
        fd_set monitored;
        FD_ZERO(&monitored);
        FD_SET(server_socket_fd, &monitored);
        
        for (int i = 0; i < clinum; i++){
            if (clients[i].state < 99){
                maxfd = clients[i].sock_fd > maxfd ? clients[i].sock_fd : maxfd;
                FD_SET(clients[i].sock_fd, &monitored);
            }
        }
        
        select((maxfd+1), &monitored, NULL, NULL, NULL);
        
        if (FD_ISSET(server_socket_fd, &monitored)){
            struct sockaddr_in client_config;
            int client_config_len = sizeof(struct sockaddr_in);
            int newfd = accept(server_socket_fd, (struct sockaddr*)&client_config, &client_config_len);

            
            clients[clinum].sconn = SSL_new(sslctx);
            SSL_set_fd(clients[clinum].sconn, newfd);
            SSL_accept(clients[clinum].sconn);
            
            clients[clinum].sock_fd = newfd;
            strcpy(clients[clinum].name, "???");
            clients[clinum].state = 1;
            
            clinum++;
            clients = realloc(clients, sizeof(struct client)*(clinum+2));
            printf("Nowy klient\n");
        }
        
        for (int i = 0; i < clinum; i++){
            if (FD_ISSET(clients[i].sock_fd, &monitored)){
                char testbyte;
                int socktest = recv(clients[i].sock_fd,  &testbyte, 1, MSG_DONTWAIT | MSG_PEEK);
                if (socktest == 0){
                    clients[i].state = 99;
                    printf("Disconnect\n");
                    continue;
                }
                if (clients[i].state == 1){
                    printf("Czytam\n");
                    char recvname[100];
                    int failedrecv = 0;
                    for (int idx = 0; idx < 100; idx++){
                        int readret = SSL_read(clients[i].sconn, &recvname[idx], 1);
                        if (readret != 1 || idx == 99){
                            failedrecv = 1;
                            break;
                        }
                        if (recvname[idx] == '\0'){
                            break;
                        }
                        printf("Przeczytano %d\n", recvname[idx]);
                    }
                    if (failedrecv){
                                printf("Niepowodzenie\n");
                        continue;
                    }
                    for (int idx = 0; idx < clinum; idx++){
                                printf("status\n");
                        if (clients[idx].state == 2){
                            char sep = '\n';
                            SSL_write(clients[i].sconn, clients[idx].name, strlen(clients[idx].name));
                            SSL_write(clients[i].sconn, &sep, 1);
                        }
                    }
                    char endsymb = '\0';
                    SSL_write(clients[i].sconn, &endsymb, 1);
                    strcpy(clients[i].name, recvname);
                    clients[i].state = 2;
                    continue;
                }
                if (clients[i].state == 2){
                    char targetname[100];
                    char message[1000];
                    int failedrecv = 0;
                    for (int idx = 0; idx < 100; idx++){
                        int readret = SSL_read(clients[i].sconn, &targetname[idx], 1);
                        if (readret != 1 || idx == 99){
                            failedrecv = 1;
                            break;
                        }
                        if (targetname[idx] == '\0'){
                            break;
                        }
                    }
                    if (failedrecv){
                        continue;
                    }
                    for (int idx = 0; idx < 1000; idx++){
                        int readret = SSL_read(clients[i].sconn, &message[idx], 1);
                        if (readret != 1 || idx == 99){
                            failedrecv = 1;
                            break;
                        }
                        if (message[idx] == '\0'){
                            break;
                        }
                    }
                    if (failedrecv){
                        continue;
                    }
                    int targetfd = -1;
                    SSL* targetsc;
                    for (int idx = 0; idx < clinum; idx++){
                        if (strcmp(targetname, clients[idx].name)  == 0 && clients[idx].state == 2){
                            targetfd = clients[idx].sock_fd;
                            targetsc = clients[idx].sconn;
                            break;
                        }
                    }
                    if (targetfd == -1){
                        continue;
                    }
                    SSL_write(targetsc, message, strlen(message));
                    char endsymb = '\0';
                    SSL_write(targetsc, &endsymb, 1);
                    
                }
            }
        }
        
    }
    
    
    return 0;
}
