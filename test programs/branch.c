#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int main() {
    int a, b;
    read(a);
    read(b);
    if (a>=b) {
        write(a);
    }
    if (b>a) {
        write(b);
    }
}

