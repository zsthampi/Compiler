#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int c()
{
    return 1;
}

int b()
{
    return 2;
}

int a()
{
    return 3;
}

int foo(int a, int b, int c)
{
    return (a*3 + b*2 + c);
}

int main() 
{
    int val;
    val = foo(a(), b(), c());

    print("I calculate the answer to be: ");
    write(val);
}
