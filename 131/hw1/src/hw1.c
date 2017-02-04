#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#define max_threads 3

struct Philosopher {
  bool done;
} p1;

struct State {
  struct Philosopher p[max_threads];
  pthread_mutex_t f[max_threads];
  int id;
};

void *PrintHello(struct State *state) {
  printf("Hello World! It's me, thread #%d!\n", state->id);
  pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
  int num_threads = atoi(argv[1]);
  pthread_t threads[num_threads];
  int rc;
  long t;
  struct Philosopher *philos[num_threads];
  pthread_mutex_t *forks[num_threads];
  struct State *states[num_threads];
  for(t = 0; t < num_threads; t++){
    struct Philosopher * p = &(struct Philosopher) {
      .done = false
    };
    philos[t] = p;
    if (pthread_mutex_init(&forks[t], NULL) != 0) {
      printf("\n mutex init failed\n");
      return 1;
    }
    struct State * state = &(struct State) {
      .p = philos,
      .f = forks,
      .id = t
    };
    states[t] = state;
    rc = pthread_create(&threads[t], NULL, PrintHello, &state[t]);
    if (rc){
      printf("ERROR; return code from pthread_create() is %d\n", rc);
      exit(-1);
    }
  }
  pthread_exit(NULL);
  for (t = 0; t < num_threads; t++) {
    pthread_mutex_destroy(forks[t]);
  }
}
