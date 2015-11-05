#include <cstdio>
struct Point{
    int x,y;
};

int main(void){
    int n;
    Point * points = new Point[n];
    for(int idx=0; idx < n; ++idx)
    {
        scnaf("%d %d", &points[idx].x, &points[idx].y);
    }

    return 0;
}
