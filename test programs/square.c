#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int square(int x)
{
    int x;
    x = 10;

    return x * x;
}

int main(void)
{
    int val;
    print("Give me a number: ");
    read(val);

    print("Your number squared is: ");
    write(square(val));
}
