#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int max(int a, int b) {
    if (a>b) {
        return a;
    }
    return b;
}

int main() {
    int a,b;
    read(a);
    read(b);

    write(max(a,b));
}

