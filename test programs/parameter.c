#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

void foo(int m,int n) {
    m = m + n;
    n = n + m;
}

int main() {
    int a;
    read(a);
    foo(a,a);
    write(a);
}


