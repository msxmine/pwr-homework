#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <chrono>
#include <thread>
#include <math.h>
#include <signal.h>
#include <termios.h>

struct termios old_settings;
struct termios new_settings;

bool *framebuffer;
int fbwidth;
int fbheight;

const float paddle_height = 0.1;
const float ball_speed = 0.2;

float p1paddle_pos = 0.5;
float p2paddle_pos = 0.5;
float ballx = 0.5;
float bally = 0.5;
float ballvelx = -ball_speed;
float ballvely = 0;

std::chrono::steady_clock::time_point last_tick_time;

int score1 = 0;
int score2 = 0;

const char *cells[] = {" ", "▘", "▝", "▀", "▖", "▌", "▞", "▛", "▗", "▚", "▐", "▜", "▄", "▙", "▟", "█"};

bool refreshHeader = true;

void draw(){
    struct winsize w;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
    //printf("lines %d\n", w.ws_row);
    //printf("columns %d\n", w.ws_col);
    if (fbwidth != w.ws_col*2 || fbheight != (w.ws_row)*2){
        framebuffer = (bool*)realloc(framebuffer, sizeof(bool) * w.ws_col*2 * (w.ws_row)*2);
        fbwidth = w.ws_col*2;
        fbheight = (w.ws_row)*2;
        refreshHeader = true;
    }
    memset(framebuffer, 0, sizeof(bool) * fbwidth * fbheight);
    
    
    //Scoreboard divider
    
    for (int x = 0; x < fbwidth; x++){
        framebuffer[(x) + ((2)*fbwidth)] = true;
    }
    
    //Paddles
    
    int top1 = 3 + ((fbheight - 3) * (p1paddle_pos - (paddle_height / 2)));
    top1 = (top1 < 3 ? 3 : top1);
    int bottom1 = 3 + ((fbheight - 3) * (p1paddle_pos + (paddle_height / 2)));
    bottom1 = (bottom1 > (fbheight-1) ? (fbheight-1) : bottom1);
    
    int top2 = 3 + ((fbheight - 3) * (p2paddle_pos - (paddle_height / 2)));
    top2 = (top2 < 3 ? 3 : top2);
    int bottom2 = 3 + ((fbheight - 3) * (p2paddle_pos + (paddle_height / 2)));
    bottom2 = (bottom2 > (fbheight-1) ? (fbheight-1) : bottom2);
    
    for (int y = top1; y <= bottom1; y++){
        framebuffer[(0) + ((y)*fbwidth)] = true;
    }
    
    for (int y = top2; y <= bottom2; y++){
        framebuffer[(fbwidth-1) + ((y)*fbwidth)] = true;
    }
    
    //Middle Divider
    
    int middlex = fbwidth / 2;
    
    for (int y = 3; y < fbheight; y++){
        framebuffer[(middlex) + ((y)*fbwidth)] = ((y % 6) < 3);
    }
    
    //Ball
    
    int balldrawx = fbwidth * ballx;
    int balldrawy = 3 + ((fbheight - 3) * bally);
    balldrawx = (balldrawx < 0 ? 0 : balldrawx);
    balldrawx = (balldrawx > (fbwidth-1) ? (fbwidth-1) : balldrawx);
    balldrawy = (balldrawy < 0 ? 0 : balldrawy);
    balldrawy = (balldrawy > (fbheight-1) ? (fbheight-1) : balldrawy);
    framebuffer[(balldrawx) + ((balldrawy)*fbwidth)] = true;
    
    
    printf("\x1b[H");
    printf("\n");
    
    for (int y = 2; y < fbheight; y += 2){
        for (int x = 0; x < fbwidth; x+=2){
            int cellval = (framebuffer[(x) + ((y)*fbwidth)] | (framebuffer[(x+1) + ((y)*fbwidth)] << 1) | (framebuffer[(x) + ((y+1)*fbwidth)] << 2) | (framebuffer[(x+1) + ((y+1)*fbwidth)] << 3) );
            printf("%s", cells[cellval]);
        }
        //printf("\n");
    }
    
    if (refreshHeader){
        refreshHeader = false;
        printf("\x1b[H");
        printf("\x1b[K");
        char p1score[100];
        char p2score[100];
        sprintf(p1score, "Gracz 1: %d", score1);
        sprintf(p2score, "%d :Gracz 2", score2);
        
        if (w.ws_col % 2 == 0){
            printf("\x1b[1;%dHPONG", (w.ws_col/2)-1);
            printf("\x1b[H%s", p1score);
            printf("\x1b[1;%luH%s", (w.ws_col+1)  - strlen(p2score) , p2score);

        }
        else{
            printf("\x1b[1;%dHP O N G", (w.ws_col/2)-2);
            printf("\x1b[H%s", p1score);
            printf("\x1b[1;%luH%s", (w.ws_col+1)  - strlen(p2score) , p2score);

        }
        
    }
    
    fflush(stdout);
    sync();
    
    
}

void calculateball(){
    std::chrono::steady_clock::time_point this_tick_time = std::chrono::steady_clock::now();
    std::chrono::duration<double> delta = (this_tick_time - last_tick_time);
    float secondsdelta = delta.count();
    
    float deltax = (secondsdelta*ballvelx);
    float deltay = (secondsdelta*ballvely);
    float newballx = ballx+deltax;
    float newbally = bally+deltay;
    
    if (newballx < 0){
        float inspacefrac = fabs(ballx/deltax);
        float impacty = bally+(deltay * inspacefrac );
        if (impacty < (p1paddle_pos + (paddle_height * 0.5)) && impacty > (p1paddle_pos - (paddle_height * 0.5)) ){
            float yvelmodifier = (impacty-p1paddle_pos)/(paddle_height/2);
            float newyvel = ballvely + yvelmodifier;
            float newxvel = fabs(ballvelx);
            float normalfactor = ball_speed / sqrt((newyvel*newyvel) + (newxvel*newxvel));
            newyvel = newyvel * normalfactor;
            newyvel = (fabs(newyvel) > (0.7 * ball_speed) ? copysign((0.7 * ball_speed), newyvel) : newyvel);
            newxvel = newxvel * normalfactor;
            newxvel = (fabs(newxvel) < (0.7 * ball_speed) ? copysign((0.7 * ball_speed), newxvel) : newxvel);
            normalfactor = ball_speed / sqrt((newyvel*newyvel) + (newxvel*newxvel));
            ballvely = newyvel * normalfactor;
            ballvelx = newxvel * normalfactor;
            newballx = 0 + (ballvelx * secondsdelta * (1 - inspacefrac));
            newbally = impacty + (ballvely * secondsdelta * (1 - inspacefrac));
        }
        else{
            score2++;
            refreshHeader = true;
            ballvely = 0;
            ballvelx = ball_speed;
            newbally = 0.5;
            newballx = 0.5;
        }
    }
    if (newballx > 1){
        float inspacefrac = fabs((ballx-1)/deltax);
        float impacty = bally+(deltay * inspacefrac );
        if (impacty < (p2paddle_pos + (paddle_height * 0.5)) && impacty > (p2paddle_pos - (paddle_height * 0.5)) ){
            float yvelmodifier = (impacty-p2paddle_pos)/(paddle_height/2);
            float newyvel = ballvely + yvelmodifier;
            float newxvel = -fabs(ballvelx);
            float normalfactor = ball_speed / sqrt((newyvel*newyvel) + (newxvel*newxvel));
            newyvel = newyvel * normalfactor;
            newyvel = (fabs(newyvel) > (0.7 * ball_speed) ? copysign((0.7 * ball_speed), newyvel) : newyvel);
            newxvel = newxvel * normalfactor;
            newxvel = (fabs(newxvel) < (0.7 * ball_speed) ? copysign((0.7 * ball_speed), newxvel) : newxvel);
            normalfactor = ball_speed / sqrt((newyvel*newyvel) + (newxvel*newxvel));
            ballvely = newyvel * normalfactor;
            ballvelx = newxvel * normalfactor;
            newballx = 1 + (ballvelx * secondsdelta * (1 - inspacefrac));
            newbally = impacty + (ballvely * secondsdelta * (1 - inspacefrac));
        }
        else{
            score1++;
            refreshHeader = true;
            ballvely = 0;
            ballvelx = -ball_speed;
            newbally = 0.5;
            newballx = 0.5;
        }
    }
    
    if (newbally < 0){
        ballvely = fabs(ballvely);
        newbally = fabs(newbally);
    }
    if (newbally > 1){
        ballvely = -fabs(ballvely);
        newbally = 1 - fabs(newbally-1);
    }
    ballx = newballx;
    bally = newbally;
    
    last_tick_time = this_tick_time;
}

void handleInput(){
    bool p1up = false;
    bool p1down = false;
    bool p2up = false;
    bool p2down = false;
    
    int specialstage = 0;
    int toRead = 0;
    if (ioctl(STDIN_FILENO, FIONREAD, &toRead) < 0){
        toRead = 0;
    }
    while (toRead > 0){
        unsigned char inByte;
        read(STDIN_FILENO, &inByte, 1);
        toRead--;
        
        if (specialstage == 2){
            if(inByte == 'A'){
                p2up = true;
            }
            if(inByte == 'B'){
                p2down = true;
            }
            specialstage = 0;
        }
        
        if (specialstage == 1){
            if(inByte == '['){
                specialstage = 2;
            }
            else{
                specialstage = 0;
            }
        }
        
        if(inByte == 'w'){
            p1up = true;
        }
        if(inByte == 's'){
            p1down = true;
        }
        if(inByte == '\033'){
            specialstage = 1;
        }
    }
    if (p1up){
        p1paddle_pos -= 0.01;
        p1paddle_pos = ((p1paddle_pos-(paddle_height/2) > 0) ? p1paddle_pos : (0 + (paddle_height/2)));
    }
    if (p1down){
        p1paddle_pos += 0.01;
        p1paddle_pos = ((p1paddle_pos+(paddle_height/2) < 1) ? p1paddle_pos : (1 - (paddle_height/2)));
    }
    if (p2up){
        p2paddle_pos -= 0.01;
        p2paddle_pos = ((p2paddle_pos-(paddle_height/2) > 0) ? p2paddle_pos : (0 + (paddle_height/2)));
    }
    if (p2down){
        p2paddle_pos += 0.01;
        p2paddle_pos = ((p2paddle_pos+(paddle_height/2) < 1) ? p2paddle_pos : (1 - (paddle_height/2)));
    }
}

static volatile bool keepRunning = true;

void gracefulExit(int arg){
    keepRunning = false;
}

int main(){
    framebuffer = (bool*)malloc( sizeof(bool) * 100 * 100);
    fbwidth = 100;
    fbheight = 100;
    
    tcgetattr(STDIN_FILENO, &old_settings);
    tcgetattr(STDIN_FILENO, &new_settings);
    new_settings.c_lflag &= ~ICANON;
    new_settings.c_lflag &= ~ECHO;
    tcsetattr(STDIN_FILENO, TCSANOW, &new_settings);
    
    signal(SIGINT, gracefulExit);
    printf("\x1b[?25l");
    
    last_tick_time = std::chrono::steady_clock::now();
    
    while(keepRunning){
        handleInput();
        calculateball();
        draw();
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
    
    tcsetattr(STDIN_FILENO, TCSANOW, &old_settings);
    printf("\x1b[H");
    printf("\x1b[2J");
    printf("\x1b[?25h");

    return 0;
}
