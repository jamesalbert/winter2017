**performance measure** should be implemented in the environment as opposed to the agent:
  - agents with performance measures built in lead to "sour grapes"


What is **rational** at any given time depends on four things:
  - The performance measure that defines the criterion of success.
  - The agent’s prior knowledge of the environment.
  - The actions that the agent can perform.
  - The agent’s percept sequence to date.

  - this seems to correlate with PEAS (performance, environment, actuators, sensors)
    - actuators -> actions
    - sensors -> devices that build up the percept sequence


**rational agent**:
  - For each possible percept sequence, a rational agent should select an action that is expected to maximize its performance measure, given the evidence provided by the percept sequence and whatever built-in knowledge the agent has


an agent is **rational** under these circumstances (vacuum scenario):
  - performance measure is awarded one point for each clear square
  - environment is known beforehand, but distribution and initial location of agent is not.
  - only available actions are left, right, and suck
  - agent correctly perceives location and whether location contains dirt


an agent should take part in **information gathering** before taking an action in order to modify future percept sequences


**task environments**:
  - "problems" to which rational agents are the "solutions"


chess is a **competitive multiagent environment**

taxi-driving is a **partially cooperative, partially competitive** multiagent environment

**deterministic**
  - the next state of the environment is completely determined by the current state and the action executed by the agent


4 basic types of agents:
  - reflex
    - simple mapping of percept to action
  - model-based
    - maintains internal state to track aspects of the world not evident to the current percept
  - goal
    - act to achieve goal
  - utility
    - maximize own "happiness"
