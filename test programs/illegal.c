#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int array_1[4];
int array_2[4];

void populate_arrays(void)
{
    array_1[0] = 0;
    array_1[1] = 1;
    array_1[2] = 1;
    array_1[3] = 2;

    array_2[0] = 3;
    array_2[1] = 5;
    array_2[2] = 8;
    array_2[3] = 13;
}

int main(void)
{
    int idx, bound;

    populate_arrays();
    
    idx = 0;
    bound = 8;

    print("The first few digits of the Fibonacci sequence are:\n");
    while (idx < bound)
    {
	write(array_1[idx]);
	idx = idx + 1;
    }
}
