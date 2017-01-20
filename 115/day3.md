Events
======


events:
  - customer arrival
  - enter queue
  - exit queue
  - start service
  - end service
  - arrival

- last thing to do at end of customer arrival event is to schedule a enter queue event
  -  Schedule('enter-queue', customer, now+walk_time)

#### Events
- EnterQueue(customer)
  - customer.start_wait_time = now
  - if queue is empty then
    - schedule('exit-queue', customer, now)
- ExitQueue(customer)
  - customer.wait_time = now - start_wait_time
  - schedule('start-service', customer, now+walk_time)
- StartService(customer)
  - generate random variable for service time
  - schedule('end-service', customer, now+service_time)
  - set teller_busy = True
- EndService(customer)
  - schedule('departure', customer, now+walk_time)
  - if there is a next customer in queue then
    - schedule('exit-queue', next_customer, now+walk_time)
  - set teller_busy = False
- Depart(customer)
  - gather statistics about customer
  - time in system = now - start wait time
  - free memory used by customer object
- EndSim()
  - output stats
  - exit back to OS
- InitSim()
  - generate first customer arrival time
  - schedule('arrival', customer, now+interarrival_time)



Reversioning to the mean:
  - you can't expect compensation for probabilities


Exponential distribution
  - f(t) = re^-rt
    - r = rate
    - t = inter-arrival time
    - 1 / r = average inter-arrival time
