#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

void bar@(void)
{
    int x, y;
    if (x > y)
    {
	return;
    }

    x = y;
    return;
}

void foo(void)
{
    bar@();
}

int main(void)
{
    foo();
}
