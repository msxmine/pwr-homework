#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <openssl/ssl.h>

int main(){
    SSL_CTX* sslctx;
    SSL* cSSL;
    
    SSL_load_error_strings();
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    
    int server;
    server = socket(AF_INET, SOCK_STREAM, 0);
    
    struct sockaddr_in config;
    memset(&config, 0, sizeof(config));
    config.sin_addr.s_addr = inet_addr("127.0.0.1");
    config.sin_family = AF_INET;
    config.sin_port = htons(24242);
    
    connect(server, (struct sockaddr*)&config, sizeof(config));
    
    sslctx = SSL_CTX_new(TLS_client_method());
    SSL_CTX_set_options(sslctx, SSL_OP_SINGLE_DH_USE);
    SSL_CTX_load_verify_locations(sslctx, "./myCA.pem", NULL);
    
    cSSL = SSL_new(sslctx);
    SSL_set_fd(cSSL, server);
    
    SSL_connect(cSSL);
    
    char name[80];
    printf("Nazwa:\n");
    //fgets(name, 75, stdin);
    scanf("%s", name);
    //name[strlen(name)-1] = '\0';
    
    char nulc = '\0';
    
    SSL_write(cSSL, name, strlen(name));
    SSL_write(cSSL, &nulc, 1);
    
    printf("Użytkownicy:\n");
    while (1){
        char got;
        int res = SSL_read(cSSL, &got, 1);
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
            SSL_write(cSSL, target, strlen(target)+1);
            SSL_write(cSSL, mess+1, strlen(mess));
        }
        
        if (FD_ISSET(server, &monitored)){
            while (1){
                char red;
                int retstat = SSL_read(cSSL, &red, 1);
                if (red == '\0'){
                    break;
                }
                printf("%c", red);
            }
        }
        
    }
    return 0;
}
