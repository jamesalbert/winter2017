---
author:
- jalbert1
date: March 2017
title: hw5
---

8.8 {#section .unnumbered}
===

$
Jim \ne George\newline
Spouse(Jim, Laura)\newline
\forall X: X \ne Jim \land ~Spouse(X, Laura)\newline
therefore ~Spouse(George, Laura)\newline
$

8.10 {#section-1 .unnumbered}
====

$
a) Occupation(Emily, Surgeon) \lor Occupation(Emily, Lawyer)\newline
b) Occupation(Joe, Actor) \land \exists! X: X \ne Actor \land Occupation(Joe, X)\newline
c) \forall X: Occupation(X, Surgeon) \Rightarrow Occupation(X, Doctor)\newline
d) \forall X: Occupation(X, Lawyer) \Rightarrow Customer(Joe, X)\newline
e) \exists! X: Boss(X, Emily) \Rightarrow Occupation(X, Lawyer)\newline
f) \exists X, \forall Y(Occupation(X, Lawyer) \Rightarrow (Customer(Y, X) \Rightarrow Occupation(Y, Doctor)))\newline
g) \forall X, \exists Y: Occupation(X, Surgeon) \Rightarrow Customer(X, Y)\newline
$

8.28 {#section-2 .unnumbered}
====

$
b) \neg Wrote(Gershwin, "Eleanor Rigby.")\newline
d) \exists X: Wrote(Joe, X)\newline
g) \forall X, \exists Y: Sings(Y, X, Revolver) \Rightarrow Y \ne Gershwin\newline
h) \forall X, \exists Y: Wrote(Gershwin, X) \Rightarrow Sings(Gershwin, X, Y)
k) \forall X, \exists Y, \exists Z: Sings(McCartney, X, Y) \Rightarrow (CopyOf(Z, Y) \land Owns(Joe, Z))\newline
$
