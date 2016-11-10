#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int main() {
    int a, sum;
    read(a);
    sum = 0;
    while (a>0) {
        sum = sum + a;
        a = a - 1;
    }
    write(sum);
}

