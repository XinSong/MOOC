#include <cstdio>
#include <limits.h>
#include <stack>
#include <algorithm>
using namespace std;

struct Point{
    int x,y;
    Point(){;}
    Point(int x, int y)
    {
        this->x = x;
        this->y = y;
    }
};

class CmpPointFunc{
    private:
        const Point & ltl;
    public:
        CmpPointFunc(Point & p):ltl(p){}
        bool operator()(const Point & p, const Point & q)
        {
            if(p.x - ltl.x == 0)
            {
                if(p.y - ltl.y > 0)
                    return false;
                else
                    return true;
            }
            if(q.x - ltl.x == 0)
            {
                if(q.y - ltl.y > 0)
                    return true;
                else
                    return false;
            }
            return ((p.y - ltl.y) * 1.0 / (p.x - ltl.x)) <= ((q.y - ltl.y) * 1.0 / (q.x - ltl.x));
        }
};

Point findLTL(Point * points, int n)
{
    Point * left_lowest = new Point(INT_MAX, INT_MAX);
    for(int idx = 0; idx < n; ++idx)
    {
        if(points[idx].x < left_lowest->x || (points[idx].x == left_lowest->x && points[idx].y < left_lowest->y))
            left_lowest = points + idx;
    }
    return *left_lowest;
}

int Area2(const Point & p, const Point & q, const Point & s)
{
    /**
     * 利用如下行列式值求三角形面积的二倍
     *        | p.x    p.y    1|
     * 2 * S= | q.x    q.y    1|
     *        | s.x    s.y    1|
     */
    return p.x * q.y - p.y * q.x + q.x * s.y - q.y * s.x + s.x * p.y - s.y * p.x;
}

bool ToLeft(const Point & p, const Point & q, const Point & s)
{
    //Area2函数所求的三角形面积是有方向的
    //利用面积的符号来求点s在有向线段pq的左侧还是右侧
    return Area2(p, q, s) > 0;
}

void sort_points(Point * points, int n)
{
    Point ltl = findLTL(points, n);
    sort(points, points + n,  CmpPointFunc(ltl));
}

void _sort_points(Point * points, int n)
{
    Point ltl = findLTL(points, n);
    sort(points, points + n,  CmpPointFunc(ltl));
}


stack<Point*> get_convex_hull(Point * points, int n)
{
    stack<Point*> point_set;
    stack<Point*> convex_hull;
    convex_hull.push(&points[0]);
    convex_hull.push(&points[1]);
    Point * e_start = &points[0];
    Point * e_end = &points[1];

    for(int idx=n-1; idx >=2; --idx)
        point_set.push(points + idx);
    while(!point_set.empty())
    {
        Point * new_p = point_set.top();
        printf("new Point: %d %d\n", new_p->x, new_p->y);
        point_set.pop();
        if(ToLeft(*e_start, *e_end, *new_p))
        {
            printf("Bingo!!!\n");
            convex_hull.push(new_p);
            e_start = e_end;
            e_end = new_p;
        }else{
            printf("Oooooops!!!\n");
            e_end = new_p;
            convex_hull.pop();
            convex_hull.push(e_end);
        }
    }
    return convex_hull;
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
    sort_points(points, n);
    for(int idx = 0; idx < n; ++idx)
    {
        printf("%d %d\n", points[idx].x, points[idx].y);
    }
    stack<Point*> convex_hull = get_convex_hull(points, n);
    while(!convex_hull.empty())
    {
        Point * t = convex_hull.top();
        convex_hull.pop();
        printf("%d %d\n", t->x, t->y);
    }
    return 0;
}
