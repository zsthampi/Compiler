#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)

int add(int a, int b) {
  return a+b;
}

int times_eight(int a) {
  return add(add(add(a,a),add(a,a)), add(add(a,a),add(a,a)));
}

int main() {
    int a, b;
    read(a);
    write(times_eight(a));
}
