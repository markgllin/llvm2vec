// clang - emit - llvm - o hello.bc - c hello.c - for *.bc
// clang -S -emit-llvm hello.c - for *.ll
#include <stdio.h>


int main() {
  int test = 5;

  if (test > 10){
    printf("hello world\n");
    return 0;
  } else {
    printf("nah\n");
    
    if (test > 3) {
      printf("i hate c\n");
    }
    return 0;
  }

}