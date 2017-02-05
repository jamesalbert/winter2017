#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#define max_threads 3

struct Philosopher {
  int courses_left;
};

struct State {
  struct Philosopher *philo;
  pthread_mutex_t locks[max_threads];
  pthread_cond_t conds[max_threads];
  bool *forks;
  int id;
  int num;
};

void *PrintHello(struct State *state) {
  int id;
  id = state->id;
  while (state->philo->courses_left > 0) {
    printf("philo %d is trying to get his fork\n", id);
    if (!state->forks[id]) {
      continue;
    }
    pthread_mutex_lock(&(state->locks[id]));
    state->forks[id] = false;
    printf("philo %d got his fork\n", id);
    int here, next, prev;
    bool right, left;
    pthread_mutex_t *lock, *rlock, *llock;
    pthread_cond_t *cond, *rcond, *lcond;
    next  = (id + 1) % state->num;
    prev  = (id - 1) % state->num;
    printf("%d, %d, %d\n", state->forks[prev], state->forks[id], state->forks[next]);
    if (state->forks[next]) {
      state->forks[next] = false;
      pthread_mutex_lock(&(state->locks[next]));
      state->philo->courses_left -= 1;
      printf("philo %d has %d courses_left\n", id, state->philo->courses_left);
      pthread_mutex_unlock(&(state->locks[next]));
      state->forks[next] = true;
    }
    else if (state->forks[prev]) {
      state->forks[prev] = false;
      pthread_mutex_lock(&(state->locks[prev]));
      state->philo->courses_left -= 1;
      printf("philo %d has %d courses_left\n", id, state->philo->courses_left);
      pthread_mutex_unlock(&(state->locks[prev]));
      state->forks[prev] = true;
    }
    pthread_mutex_unlock(&(state->locks[id]));
    state->forks[id] = true;
  }
  return NULL;
}

int main(int argc, char *argv[]) {
  int num_threads = atoi(argv[1]);
  pthread_t threads[num_threads];
  int rc;
  long t;
  struct Philosopher *philos;
  pthread_mutex_t *locks;
  pthread_cond_t *conds;
  bool *forks;
  struct State *states;
  philos = (struct Philosopher*)malloc(num_threads*sizeof(*philos));
  locks  = (pthread_mutex_t *)malloc(num_threads*sizeof(*locks));
  conds  = (pthread_cond_t *)malloc(num_threads*sizeof(*conds));
  forks = (bool *)malloc(num_threads*sizeof(*forks));
  states = (struct State *)malloc(num_threads*sizeof(*states));
  for(t = 0; t < num_threads; t++){
    if (pthread_mutex_init(&locks[t], NULL) != 0) {
      printf("\n mutex init failed\n");
      return 1;
    }
    if (pthread_cond_init(&conds[t], NULL) != 0) {
      printf("\n cond init failed\n");
      return 1;
    }
    forks[t] = true;
    philos[t] = (struct Philosopher) {
      .courses_left = 3
    };
    struct State * state = &(struct State) {
      .philo = &(philos[t]),
      .locks = locks,
      .forks = forks,
      .id = t,
      .num = num_threads
    };
    states[t] = *state;
    rc = pthread_create(&threads[t], NULL, PrintHello, &states[t]);
    if (rc) {
      printf("ERROR; return code from pthread_create() is %d\n", rc);
      exit(-1);
    }
  }
  for (t = 0; t < num_threads; t++) {
    pthread_join(threads[t], NULL);
  }
  for (t = 0; t < num_threads; t++) {
    pthread_mutex_destroy(&locks[t]);
  }
  free(locks);
  free(conds);
  free(forks);
  free(states);
}
