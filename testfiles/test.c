#include <stdio.h>
#include <math.h>

typedef int (*foo)(int, int);

int add(int a, int b) {
  return a + b;
}

foo foo_constructor(int x) {
  return &add;
}
void clearstack(){
  int a[10000];
  int i = 0;
  for (; i < 10000; ++i){
    a[i] = 10;
  }
}

int main() {

  foo f;
  f = add;
  clearstack();
  int res = f(5, 6);
  printf("%d\n", res);

  foo g = foo_constructor(3);
  int res1 = g(10, 4);
  printf("%d\n", res1);
  return 0;
}
