Problem Set
===========

###### James Albert, 16004325

##### Problem 4.5

Yes, random variables X and Y are independent. The whole idea of replacement (in this case, with respect to a deck of cards) is that once we randomly pick a card from the deck, we put it back so that there's a chance that we randomly pick it again. Without using replacement, Y would be dependent on X (if X picks a card first) because once X picks its card, that card is out the domain of available cards to pick for Y.


##### Problem 4.26

```
  F(x) = P(X <= x) # cdf
       = 1 - e^(-x/mu) # exponential cdf
  P(X > t) = 1 - F(t)
           = 1 - (1 - e^(-t/mu))
           = 1 - 1 + e^(-t/mu)
           = e^(-t/mu)
  similarly:
    P(X > t + s) = e^( (-t - s) / mu)
    P(X > s) = e^(-s/mu)

  Given P(X > t + s | X > t) = P(X > s)
  P(X > t + s | X > t) = 1 - P(X <= t + s | X > t)
                       = 1 - (P(X <= t + s intersection X > t) / P(X > t))
                       = 1 - (P(t < X <= t + s) / P(X > t))
                       = 1 - (e^(-t/mu) - e^((-t - s)/mu) / e^(-t/mu))
                       = 1 - [ (e^(-t/mu) / e^(-t/mu)) - (e^((-t - s) / mu) / e^(-t/mu)) ]
                       = 1 - [ 1 - (e^(-t/mu - s/mu) / e^(-t/mu)) ]
                       = 1 - 1 + e^(-t/mu - s/mu - (-t/mu))
                       = e^(-s/mu)
                       = P(X > s)

  therefore:
    the exponential distribution has the memoryless property
```

##### Problem 5.2

It might be easier to validate the model of a computer system than that of military combat because we can extract expected/sample output from a computer system with much more ease. We can tell exactly how much memory, cpu, and any other resource processes are using at any time and we can record that data as time progresses. Doing so with a military system would require heavy human interaction to record "output" data, especially over time. The only data collection you might be able to automate would be ammo inventory (how much did we start the battle with, average/std. deviation amount of shots fired, how much did we end battle with, etc), but there's a lot more to combat than ammo use. How good of a leader does a group of soldiers think their commander is? What's the morale of all/subset of the soldiers? How do the answers to these questions change over time?

In a nutshell, it's much easier to obtain credible data with which to validate when it comes to a computer system.
