#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <SDL.h>
#include <SDL_image.h>

void Slock(SDL_Surface *screen)
{
  if ( SDL_MUSTLOCK(screen) )
    if ( SDL_LockSurface(screen) < 0 )
      return;
}

void Sulock(SDL_Surface *screen)
{
  if ( SDL_MUSTLOCK(screen) )
    SDL_UnlockSurface(screen);
}


void fade_code(SDL_Surface *im1, SDL_Surface *im2, Uint8 alpha, SDL_Surface* imOut)
{
    int pixelsCount = imOut->w * im1->h;
    int byteCount = imOut->format->BytesPerPixel * pixelsCount;
    
    Uint8 *A = (Uint8*) im1->pixels;
    Uint8 *B = (Uint8*) im2->pixels;
    Uint8 *out = (Uint8*) imOut->pixels;
    Uint8 *end = out + byteCount;
    
    for(; out != end; out++,A++,B++)
        *out = (Uint8)(( (*A) * alpha + (*B) * (128 - alpha))/128) ;
}


void fade_mmx(SDL_Surface* im1,SDL_Surface* im2,Uint8 alpha, SDL_Surface* imOut)
{
    int pixelsCount = imOut->w * im1->h;
    
    Uint32 *A = (Uint32*) im1->pixels;
    Uint32 *B = (Uint32*) im2->pixels;
    Uint32 *out = (Uint32*) imOut->pixels;
    Uint32 *end = out + pixelsCount;



    Uint64 pA = (long long)(alpha) * 2;
    Uint64 pB = (long long)(128 - alpha) * 2;
    Uint64 preparedAlpha = pA | (pA << 16) | (pA << 32) | (pA << 48);
    Uint64 preparedBeta = pB | (pB << 16) | (pB << 32) | (pB << 48);
    /* TUTAJ WPISZ KOD WYKORZYSTUJACY MMX !!! */
    __asm__ volatile(  "movq mm0, %[pAl] \n"
    			"movq mm1, %[pBt] \n"
    			"mloop: \n"
    			"cmp %[out], %[end] \n"
    			"je enddraw \n"
    			"pxor mm2, mm2 \n" //Nie trzeba ich zerowac, ale tak dziala duzo szybciej
    			"punpcklbw mm2, dword [ %[im1] ] \n"
    			"psrlw mm2, 8 \n"
    			"pxor mm3, mm3 \n" //
    			"punpcklbw mm3, dword [ %[im2] ] \n"
    			"psrlw mm3, 8 \n"
    			"pmullw mm2, mm0 \n"
    			"pmullw mm3, mm1 \n"
    			"psrlw mm2, 8 \n"
    			"psrlw mm3, 8 \n"
    			"paddw mm2, mm3 \n"
    			"packuswb mm2, mm2 \n"
    			"movd dword [ %[out] ] , mm2 \n"
    			"add %[im1], 4 \n"
    			"add %[im2], 4 \n"
    			"add %[out], 4 \n"
    			"jmp mloop \n"
    			"enddraw: \n"
    			
    			 : [im1] "+r" (A), [im2] "+r" (B), [out] "+r" (out) : [end] "rm" (end), [pAl] "m" (preparedAlpha), [pBt] "m" (preparedBeta) : "mm0", "mm1", "mm2", "mm3", "memory");
    
    __asm__("emms" : : ); // koniec
}


int main(int argc, char *argv[])
{
    char *file1 = "image1.jpg",*file2 = "image2.jpg";
    
    if(argc == 3){
        file1 = argv[1];
        file2 = argv[2];
    }
    
    if ( SDL_Init(SDL_INIT_AUDIO|SDL_INIT_VIDEO) < 0 ){
        printf("Unable to init SDL: %s\n", SDL_GetError());
        exit(1);
    }
    atexit(SDL_Quit);
    
    SDL_Surface *screen;
    screen = SDL_SetVideoMode( 800, 600,32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    
    if ( screen == NULL ){
        printf("Unable to set %dx%d video: %s\n",800, 600, SDL_GetError());
        exit(1);
    }
  
    SDL_Surface *image1,*image2,*output;
    SDL_Surface *temp;
     
    temp = IMG_Load(file1);
    if (temp == NULL) 
    {
        printf("Unable to load bitmap: %s\n", SDL_GetError());
        return 1;
    }
    image1 = SDL_DisplayFormat(temp);
    SDL_FreeSurface(temp);

    temp = IMG_Load(file2);
    if (temp == NULL) 
    {
        printf("Unable to load bitmap: %s\n", SDL_GetError());
        return 1;
    }
    image2 = SDL_DisplayFormat(temp);
    SDL_FreeSurface(temp);
    
    if( image1->w != image2->w || image1->h != image2->h )
    {
        printf("Bad bitmaps sizes\n");
        return 1;
    }
    
    temp = SDL_CreateRGBSurface(
        SDL_SWSURFACE, image1->w, image1->h,
        image1->format->BitsPerPixel,
        image1->format->Rmask, image1->format->Gmask, 
        image1->format->Bmask, image1->format->Amask 
    );
    
    output = SDL_DisplayFormat(temp);
    SDL_FreeSurface(temp);
    
    SDL_Rect src, dest;
    
    src.x = 0;
    src.y = 0;
    src.w = output->w;
    src.h = output->h;
     
    dest.x = 0;
    dest.y = 0;
    dest.w = output->w;
    dest.h = output->h;
    
    int maxFPS = 0;
    int FPS = 0;
    int lastTimeFPS = 0;
    
    int done = false;
    int mode = 1, lastMode = 0;
    int alpha;
    Uint8 f = 0;
    char buffer[64];
    
    while(!done)
    {
        SDL_Event event;
        
        while ( SDL_PollEvent(&event) )
        {
            if ( event.type == SDL_QUIT )
                done = true;
        
            if ( event.type == SDL_KEYDOWN )
            {
                if ( event.key.keysym.sym == SDLK_ESCAPE )
                    done = true;
                if ( event.key.keysym.sym == SDLK_1 )
                    mode = 1;
                if ( event.key.keysym.sym == SDLK_2 )
                    mode = 2;
            }
        }
     
        alpha = f<0x80 ? (f&0x7f) : 0x80-(f&0x7f);
        f++;

        switch(mode)
        {
            case 1:
                fade_code(image1, image2, alpha, output);
                break;
            default:
                fade_mmx(image1, image2, alpha, output);
                break;
        }
        
        int currentTime = SDL_GetTicks();
        
        Slock(screen);
        SDL_BlitSurface(output, &src, screen, &dest);
        Sulock(screen);
        
        SDL_Flip(screen);
        FPS++;
        
        if ( currentTime - lastTimeFPS >= 1000 )
        {
            if (FPS > maxFPS)
                maxFPS = FPS;
            
            if (lastMode != mode)
                maxFPS = 0;
            
            snprintf( buffer, sizeof(buffer), "%d FPS (max:%d) [%d]", FPS, maxFPS, mode );
            SDL_WM_SetCaption( buffer,0 );
            FPS = 0;
            lastTimeFPS = currentTime;
            lastMode = mode;
        } 
    }
    
    SDL_Quit();
    
    return 0;
}

