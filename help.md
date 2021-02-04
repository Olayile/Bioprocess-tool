
# Curve Fitting
---
Curve fitting is done using a polynomial objective function. Using scipy.optimize curve fit using least-squares to minimize the sum of squares of the non-linear function.

# Kinetic models
---

## Cell growth models
---

*Monod*: This is a model formed by  [Jacques Monod](https://en.wikipedia.org/wiki/Jacques_Monod)

*

## Parameter fitting 
---

> **Levenberg-Marquardt**: By default, the Levenberg-Marquardt algorithm is used for fitting. While often criticized, including the fact it finds a local minima, this approach has some distinct advantages. These include being fast, and well-behaved for most curve-fitting needs, and making it easy to estimate uncertainties for and correlations between pairs of fit variables, 

> **Differential evolution**: The inspiration of Differential (DE) comes from the the Darwanian principal of evolution where the fittest individual moves on to the next generation. DE adds the weighted adds the weighted difference of two individuals in a population which are randomly selected to a third individual. New candidate solutions are created by the combination of the parent as well as several other individuals of the same population. The candidate replaces the parent if the fitness is better. DE consist of three key parameters, namely: population size, crossover probability constant and scaling imilar to other evolutionary algorithms, DE starts with an initial set of possible solutions which evolve by mutation, crossover and selection until a stop criteria is reached DE. is different from other evolutionary algorithms in their motivation, roles and applications as well as consisting of parameter encoding. DE encodes all parameters using a floating point which can be manipulated using arithmetic operators compared to GA which uses binary encoding scheme. This difference gives several advantages to using DE, such as decreased memory complexity, decreased computational cost and complexity as well as ease of use.  Differential evolution has undergone a large number of modifications since it was discovered. These have been used to further enhance its performance on complex optimization problems. The modifications are implemented on the parameters involved and the basic steps(population alignment, mutation, crossover, selection) \cite{dragoi_optimization_2013}

## Frequently asked Questions 
---
