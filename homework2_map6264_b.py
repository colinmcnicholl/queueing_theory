"""
Homework 2 (Reliable Intuition?)
Consider a renewal process.  Let X be the interrenewal times; and let I and R
be the length of the interval interrupted at random and its remainder,
respectively.  The following BASIC simulation calculates the average values
of X, I and R (based on 10,000 replications of I and R, where T is a random
interruption point).

100 FOR j=1 TO 10000
110 S=0
120 T = -1000*LOG(1-RND)
130 X=
140 c=c+1
150 SX=SX+X
160 S=S+X
170 IF S<T THEN 130
180 R=S-T: I=X
190 SR=SR+R: SI=SI+I
200 NEXT j
210 PRINT SX/c,SI/10000,SR/10000

a. Run the simulation for the case when X is exponentially distributed
(that is, the renewal process is a Poisson process) with E(X) = 1.
Fill in the following table.

        E(X)                E(I)                    E(R)
theory  simulation      theory  simulation      theory  simulation


Comment on the assertion: 'It is intuitively obvious that
E(I) = e(x) and E(R) = E(X) / 2.'
"""

# import random
# from math import log


# def renewal_process():
    # c = 0
    # SX = 0
    # SR = 0
    # SI = 0
    # for j in range(10000):
        # # print(f'for loop, j: {j}')
        # S = 0
        # T = -1000 * log(1 - random.random())        # A random interruption point.
        # # print(f'A: {S}, random variable T: {T}')
        # while S < T:
            # # print(f'while loop, S: {S} < T: {T}')
            # X = random.expovariate(1)               # X interrenewal time (exponentially distributed).
            # # print(f'random variable X: {X}')
            # c += 1
            # SX += X
            # S += X
            # # print(f'c: {c}, SX: {SX}, S: {S}')
        # R = S - T                                   # Remainder of interval interrupted at random.
        # I = X                                       # length of interval interrupted at random.
        # SR += R
        # SI += I
    # print(f'SX: {SX}, SI: {SI}, SR: {SR}')
    # return SX/c, SI/10000, SR/10000                 # Average values of X, I and R based on 10,000 simulations.
    
    
# if __name__ == '__main__':
    # print(renewal_process())
    
# (0.9999828904343558, 2.0230036304379935, 1.0199996675935978) # CORRECT - agrees with theory.

    
"""
b.
Let X = Y + u, where u is a constant (to be treated as a parameter),
and Y is a random variable with probability distribution:
P(Y=1) = 0.9, P(Y=11) = 0.1.  Run the simulation and fill in the values
indicated in the table.  Calculate the theoretical values of E(I)
and E(R) according to the formulas (to be derived later):
E(I) = E(X) + V(X) / E(X) and E(R) = E(I) / 2.

Draw the theoretical graph of E(R) versus u.  On the same graph, plot the
points produced by the simulation.

Comment on the assertion: 'It is intuitively obvious that as the average
length of the random interval X increases (that is, as u increases), the
average lengths of the interrupted interval I and its remainder will also
increase.'

          E(X)                E(I)                    E(R)
u     theory  simulation      theory  simulation      theory  simulation
0.0   2.0     1.99938604      6.5     6.508           3.25    3.24256775
0.5   2.5     2.50048478      6.1     6.068           3.05    3.04055360
1.0   3.0     3.00011326      6.0     5.897           3.0     2.96294847
1.5   3.5     3.49909029      6.0714  5.966           3.0357  2.98278437
2.0   4.0     4.00051863      6.25    6.141           3.125   3.06123192
2.5   4.5     4.5008065       6.5     6.604           3.25    3.33348773
3.0   5.0     4.99976821      6.8     6.803           3.4     3.42920619
3.5   5.5     5.49976971      7.1364  7.053           3.5682  3.58323867
4.0   6.0     5.99887192      7.5     7.45            3.75    3.75796387
4.5   6.5     6.50355987      7.8846  7.841           3.9423  3.92157733
5.0   7.0     6.9996382       8.2857  8.309           4.1429  4.12271624
       
"""

import pylab
import random
from math import log

theory_interrenewal_times = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
theory_length_of_interval_interrupted = [6.5, 6.1, 6.0, 6.0714, 6.25, 6.5, 6.8, 7.1364, 7.5, 7.8846, 8.2857]
theory_length_of_remainder_of_interval_interrupted = [3.25, 3.05, 3.0, 3.0357, 3.125, 3.25, 3.4, 3.5682, 3.75, 3.9423, 4.1429]


def renewal_process(nsims, u):
    c = 0
    SX = 0
    SR = 0
    SI = 0
    for j in range(nsims):
        # print(f'for loop, j: {j}')
        S = 0
        T = -1000 * log(1 - random.random())        # A random interruption point.
        # print(f'A: {S}, random variable T: {T}')
        while S < T:
            # print(f'while loop, S: {S} < T: {T}')
            Z = random.random()
            if Z < 0.9:
                Y = 1
            else:
                Y = 11
            X = Y + u               # X interrenewal time (exponentially distributed).
            # print(f'random variable X: {X}')
            c += 1
            SX += X
            S += X
            # print(f'c: {c}, SX: {SX}, S: {S}')
        R = S - T                                   # Remainder of interval interrupted at random.
        I = X                                       # length of interval interrupted at random.
        SR += R
        SI += I
    # print(f'SX: {SX}, SI: {SI}, SR: {SR}')
    return round(SX/c, 8), round(SI/nsims, 8), round(SR/nsims, 8) # Average values of X, I and R based on 10,000 simulations.
    
    
if __name__ == '__main__':
    width0 = 4
    precision0 = 2
    width1 = 7
    precision1 = 2
    width2 = 11
    precision2 = 9
    width3 = 8
    precision3 = 5
    width4 = 11
    precision4 = 4
    width5 = 8
    precision5 = 5
    width6 = 11
    precision6 = 9
    results = []
    averages_of_length_of_interrenewal_time = []
    averages_of_length_interval_interrupted = []
    averages_of_length_of_remainder_of_interval_interrupted = []
    nsims = 10000
    constants = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    print('           E(X)                 E(I)                 E(R)')
    print('   u  theory  simulation   theory  simulation   theory  simulation')
    for i, u in enumerate(constants):
        result = renewal_process(nsims, u)
        X, I, R = result
        averages_of_length_of_interrenewal_time.append(X)
        averages_of_length_interval_interrupted.append(I)
        averages_of_length_of_remainder_of_interval_interrupted.append(R)
        
        print(f'{u:{width0}.{precision0}} {theory_interrenewal_times[i]:{width1}.{precision1}} {X:{width2}.{precision2}} {theory_length_of_interval_interrupted[i]:{width3}.{precision3}} {I:{width4}.{precision4}} {theory_length_of_remainder_of_interval_interrupted[i]:{width5}.{precision5}} {R:{width6}.{precision6}}')

# u: 0.0, result: (1.99870383, 6.503, 3.27958138)
# u: 0.5, result: (2.50177274, 6.136, 3.09685038)
# u: 1.0, result: (2.99976102, 5.959, 3.00963514)
# u: 1.5, result: (3.49998894, 6.089, 3.07296771)
# u: 2.0, result: (4.00038766, 6.221, 3.14572415)
# u: 2.5, result: (4.49960179, 6.502, 3.2728427)
# u: 3.0, result: (4.99755035, 6.802, 3.45841496)
# u: 3.5, result: (5.50412325, 7.151, 3.54764502)
# u: 4.0, result: (5.99803391, 7.451, 3.70664365)
# u: 4.5, result: (6.49939995, 7.861, 3.95283525)
# u: 5.0, result: (7.00241141, 8.309, 4.16110608)

pylab.figure(1)
pylab.plot(averages_of_length_of_interrenewal_time, averages_of_length_of_remainder_of_interval_interrupted)
pylab.title('Average wait time for taxi')
pylab.xlabel('Expected value of time between taxis')
pylab.ylabel('Expected value for wait time')
pylab.show()   