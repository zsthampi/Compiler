#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int recursionsum(int n) {
    if (n==0) {
        return 0;
    }
    return n + recursionsum(n-1);
}

int main() {
    int a;
    read(a);
    write(recursionsum(a));
}


