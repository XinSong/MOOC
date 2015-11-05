#include <cstdio>
#include <limits.h>
#include <stack>
#include <algorithm>

struct Point{
    int x,y;
    Point(){;}
    Point(int x, int y)
    {
        this->x = x;
        this->y = y;
    }
};

Point ltl(Point * points, int n)
{
    Point * left_lowest = new Point(INT_MAX, INT_MAX);
    for(int idx = 0; idx < n; ++idx)
    {
        if(points[idx].x < left_lowest->x || (points[idx].x == left_lowest->x && points[idx].y < left_lowest->y))
            left_lowest = points + idx;
    }
    return *left_lowest;
}

int Area2(Point p, Point q, Point s)
{
    /**
     * 利用如下行列式值求三角形面积的二倍
     *        | p.x    p.y    1|
     * 2 * S= | q.x    q.y    1|
     *        | s.x    s.y    1|
     */
    return p.x * q.y - p.y * q.x + q.x * s.y - q.y * s.x + s.x * p.y - s.y * p.x;
}

bool ToLeft(Point p, Point q, Point s)
{
    //Area2函数所求的三角形面积是有方向的
    //利用面积的符号来求点s在有向线段pq的左侧还是右侧
    return Area2(p, q, s) > 0;
}

int main(void){
    int n;
    scanf("%d", &n);
    printf("n=%d\n", n);
    Point * points = new Point[n];
    for(int idx = 0; idx < n; ++idx)
    {
        scanf("%d %d", &points[idx].x, &points[idx].y);
    }
    Point t = ltl(points, n);
    return 0;
}
