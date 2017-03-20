#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

/*Global variables */
int num_threads;
pthread_mutex_t *mutexes;

/* For representing the status of each philosopher */
typedef enum{
  none,   // No forks
  one,    // One fork
  two     // Both forks to consume
} utensil;

/* Representation of a philosopher */
typedef struct phil_data{
  int phil_num;
  int course;
  utensil forks;
}phil_data;

void eat(struct phil_data * p, int offset) {
  p->forks = two;
  sleep(1);
  p->course++;
  printf("philosopher %d just ate course %d\n", p->phil_num, p->course);
  pthread_mutex_unlock(&(mutexes[offset]));
  p->forks = one;
}

/* ****************Change function below ***************** */
void *eat_meal(struct phil_data * p){
/* 3 course meal: Each need to acquire both forks 3 times.
 *  First try for fork in front.
 * Then for the one on the right, if not fetched, put the first one back.
 * If both acquired, eat one course.
 */
  int id = p->phil_num;
  while (p->course < 3) {
    if (pthread_mutex_trylock(&(mutexes[id])) != 0) {
      continue;
    }
    p->forks = one;
    int next, prev;
    int n = id - 1;
    int m = num_threads;
    prev  = ((n % m) + m) % m;
    next  = (id + 1) % num_threads;
    if (pthread_mutex_trylock(&(mutexes[next])) != 0) {
      eat(p, next);
    }
    else if (pthread_mutex_trylock(&(mutexes[prev])) != 0) {
      eat(p, prev);
    }
    pthread_mutex_unlock(&(mutexes[id]));
    p->forks = none;
  }
  return NULL;
}

/* ****************Add the support for pthreads in function below ***************** */
int main( int argc, char **argv ){
  int num_philosophers, error;

  if (argc < 2) {
          fprintf(stderr, "Format: %s <Number of philosophers>\n", argv[0]);
          return 0;
     }

  num_philosophers = num_threads = atoi(argv[1]);
  pthread_t threads[num_threads];
  phil_data philosophers[num_philosophers]; //Struct for each philosopher
  mutexes = malloc(sizeof(pthread_mutex_t)*num_philosophers); //Each mutex element represent a fork

  /* Initialize structs */
  for( int i = 0; i < num_philosophers; i++ ){
    philosophers[i].phil_num = i;
    philosophers[i].course   = 0;
    philosophers[i].forks    = none;
  }
/* Each thread will represent a philosopher */

/* Initialize Mutex, Create threads, Join threads and Destroy mutex */
  for (int i = 0; i < num_threads; i++) {
    if (pthread_mutex_init(&mutexes[i], NULL) != 0) {
      printf("\n mutex init failed\n");
      return 1;
    }
  }
  for (int i = 0; i < num_threads; i++) {
    int rc = pthread_create(&threads[i], NULL, eat_meal, &philosophers[i]);
    if (rc) {
      printf("ERROR; return code from pthread_create() is %d\n", rc);
      exit(-1);
    }
  }
  for (int i = 0; i < num_threads; i++) {
    pthread_join(threads[i], NULL);
  }
  for (int i = 0; i < num_threads; i++) {
    pthread_mutex_destroy(&mutexes[i]);
  }

  return 0;
}
