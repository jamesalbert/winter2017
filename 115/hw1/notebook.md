Train Simulation
================

###### James Albert, 16004325

```python
from lib import *

Simulator(mu=10, limit=7200, verbose=False) \
  .start() \
  .analyze()
```

Running the simulator, we can observe a lot about what happened in 7200 hours. A total of 701 trains were served by the time it finished. As time progresses (figuratively), we can see trains on average receive 5 to 6 hours of service time. The dock is busy, idle, and hogged out .53%, 38.89%, and 0.21% of 7200 hours respectively. These add up to 39.63% (not 100%) because the 'busy', 'idle', and 'hogged-out' states for the dock are not mutually exclusive. As for the queue, there were at most 4 trains in the queue at once, averaging up to 1.58h hours per train wait time.

![](static/output_0_0.png)

#### Stats

    trains served: 701
    average time train is in system: 5.84h
    max time train is in system: 24.53h
    total dock idle: 0.53%
    total dock busy: 38.89%
    total dock hogged-out: 0.21%
    maximum # trains in queue: 4 trains
    average time in queue: 1.58h
