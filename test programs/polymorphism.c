#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define binary int
#define decimal int

void print_two(int a, int b) {  
    write(a);
    write(b);
}

int main() {
    binary b;
    decimal a;
    read(a);
    read(b);  
    print_two(a, b);
    print_two(b, a);
}

