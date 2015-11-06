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
        Point * points;
    public:
        CmpPointFunc(Point * p, Point & ltl):points(p), ltl(ltl){}
        bool operator()(const int p, const int q)
        {
            if(points[p].x - ltl.x == 0)
            {
                if (points[q].x - ltl.x == 0)
                    return (points[p].y - ltl.y) <= (points[q].y - ltl.y);
                else
                    return false;
            }
            else if(points[q].x - ltl.x == 0)
            {
                    return true;
            }
            return ((points[p].y - ltl.y) * 1.0 / (points[p].x - ltl.x)) <= ((points[q].y - ltl.y) * 1.0 / (points[q].x - ltl.x));
        }
};

Point & findLTL(Point * points, int n)
{
    Point * left_lowest = new Point(INT_MAX, INT_MAX);
    for(int idx = 0; idx < n; ++idx)
    {
        if(points[idx].x < left_lowest->x || (points[idx].x == left_lowest->x && points[idx].y < left_lowest->y)){
            left_lowest = points + idx;
        }
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
    return Area2(p, q, s) >= 0;
}

void sort_points(Point * points, int * result, int n)
{
    Point ltl = findLTL(points, n);
    int * point_index = new int[n];
    sort(result, result + n,  CmpPointFunc(points, ltl));
}

stack<int>  get_convex_hull(Point * points, int * point_index, int n)
{
    stack<int> point_set;
    stack<int> convex_hull;
    //convex_hull.push(point_index[0]);
    //convex_hull.push(point_index[1]);
    int e_start = point_index[0];
    int e_end = point_index[1];
    for(int idx=n-1; idx >=2; --idx)
        point_set.push(point_index[idx]);
    while(!point_set.empty())
    {
        int new_p = point_set.top();
        point_set.pop();
        while(!ToLeft(points[e_start], points[e_end], points[new_p]))
        {
            printf("list %d\n", convex_hull.size());
            printf("%d", convex_hull.size());
            e_end = e_start;
            e_start = convex_hull.top();
            printf("pop start:%d\n", e_start);
            convex_hull.pop();
            printf("pop end:%d\n", e_end);
        }
        printf("102\n");
        convex_hull.push(e_start);
        e_start = e_end;
        e_end = new_p;
    }
    convex_hull.push(e_start);
    convex_hull.push(e_end);
    return convex_hull;
}

int main(void){
    int n;
    scanf("%d", &n);
    Point * points = new Point[n];
    int * point_index = new int[n];

    for(int idx = 0; idx < n; ++idx)
        point_index[idx] = idx;

    for(int idx = 0; idx < n; ++idx)
    {
        scanf("%d %d", &points[idx].x, &points[idx].y);
    }

    sort_points(points, point_index, n);
    for(int i=0;i<n;++i)
        printf("%d\n",point_index[i]);
    stack<int> convex_hull = get_convex_hull(points, point_index, n);
    printf("le");
    long int product = convex_hull.size();
    while(!convex_hull.empty())
    {
        product *= (convex_hull.top() + 1);
        convex_hull.pop();
    }
    printf("%d\n",product);
    return 0;
}
