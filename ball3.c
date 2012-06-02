#import <math.h>

float dist(int p1x, int p1y, int p2x, int p2y);
bool * make_ball(int r, int sh, int bgx, int bgy, int cx, int cy);

int main()
{
    bool arr[500][500];
    for (i = 0; i<500; i++){
        for (j = 0; j<500; j++){
            arr[i][j] = false;
        }
    }
        
    arr = make_ball(50,51,500,500,230,340);
    return 0;
    
}

bool [] make_ball(int r, int sh, int bgx, int bgy, int cx, int cy)
{
    bool ball[bgx][bgy];
    
    

    return ball;
}
