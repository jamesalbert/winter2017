Analysis
========


#### Timing table

| num threads | chunk size | lab 1      | lab 3     |
|-------------|------------|------------|-----------|
| 2           | 25         | 0.00527241 | 0.0217012 |
| 4           | 25         | 0.00538522 | 0.021568  |
| 8           | 25         | 0.00388256 | 0.021908  |
| 2           | 70         | 0.00360094 | 0.022511  |
| 4           | 70         | 0.00314327 | 0.0215688 |
| 8           | 70         | 0.00315208 | 0.0258088 |


#### Conclusion

There seems to be a ~10-fold increase in run time in lab 3 part A2 compared to lab 1 part b. I researched why this would happen and the most I can derive, from a general perspective (algorithm not considered), is that there is a substantial overhead in using OpenMP's dynamic scheduler. This makes sense. OpenMP's dynamic scheduler does a lot of the stuff that I did by hand in Lab 1. The only difference is that I was able to do the same thing (and quite more than likely do a lot more in regards to handling the threads) with a simple pragma. There is naturally overhead in simplifying heavy tasks.
