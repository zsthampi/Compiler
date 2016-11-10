#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int g()
{
    return 1;
}

int f()
{
    return g() + 1;
}

int e()
{
    return f() + 1;
}

int d()
{
    return e() + 1;
}

int c()
{
    return d() + 1;
}

int b()
{
    return c() + 1;
}

int a()
{
    return b() + 1;
}

int main() 
{
    int val;
    val = a();

    print("I calculate the answer to be: ");
    write(val);
}
