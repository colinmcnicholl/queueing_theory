import random
import math

def get_inter_arrival_time(arrival_rate):
    return -(1 / arrival_rate) * math.log(1 - random.random())
    
def get_exponential_service_time(avg_service_time):
    return -(avg_service_time) * math.log(1 - random.random())
    
def get_uniform_service_time():
    return random.random()
    
def get_discrete_service_time():
    X = random.random()
    if X <= 0.9: return (1/3)
    return 2
    
def theory_server_utilization(arrivals_rate, mean_service_time):
    if arrivals_rate * mean_service_time < 1:
        return arrivals_rate * mean_service_time
    return 1
    
# test
arrivals_rate = 1.6
mean_service_time = 0.5
print(theory_server_utilization(arrivals_rate, mean_service_time))
# 0.8
    
def cumulative_waiting_time_distribution_theory(server_utilization, time, mean_service_time):
    if time < 0: return 0
    return 1 - server_utilization * math.exp(-(1-server_utilization)*(time/mean_service_time))
    
# test
server_utilization = 0.8
time = 0.5
mean_service_time = 0.5
print(cumulative_waiting_time_distribution_theory(server_utilization, time, mean_service_time))
# 0.34501539753761445
p_wait_greater_than_half = 1 - cumulative_waiting_time_distribution_theory(server_utilization, time, mean_service_time)
print(f'From theory P(W > 0.5): {p_wait_greater_than_half}')
# From theory P(W > 0.5): 0.6549846024623855

def average_waiting_time_exponential_service_theory(server_utilization, mean_service_time):
    return (server_utilization / (1 - server_utilization)) * mean_service_time
    
# test
server_utilization = 0.8
mean_service_time = 0.5
e_w = average_waiting_time_exponential_service_theory(server_utilization, mean_service_time)
print(f'For M/M/1 queue, E(W) = {e_w}')
# For M/M/1 queue, E(W) = 2.0000000000000004

def average_waiting_time_constant_service_times_theory(server_utilization, service_time):
    return 0.5 * average_waiting_time_exponential_service_theory(server_utilization, service_time)
    
# test
server_utilization = 0.8
service_time = 0.5
e_w = average_waiting_time_constant_service_times_theory(server_utilization, service_time)
print(f'For M/D/1 queue, E(W) = {e_w}')
# For M/D/1 queue, E(W) = 1.0000000000000002

def expected_value_discrete(values, probabilities):
    e_x = 0
    for x, p_x in zip(values, probabilities):
        e_x += x * p_x
    return e_x
    
# test
values = [1/3, 2]
probabilities = [0.9, 0.1]
average_value = expected_value_discrete(values, probabilities)
print(f'For discrete distribution taling values: {values} with probabilities: {probabilities}...')
print(f'The expected value is: {average_value}')
# The expected value is: 0.5
    
def variance_discrete(values, probabilities, expected_value):
    v_x = 0
    for x, p_x in zip(values, probabilities):
        v_x += (x - expected_value)**2 * p_x
    return v_x
    
# test
var_x = variance_discrete(values, probabilities, average_value)
print(f'For discrete distribution taling values: {values} with probabilities: {probabilities}...')
print(f'The variance is: {var_x}')
# The variance is: 0.25    
   
def simulation(service_time_distribution, arrivals_rate=1.6, mean_service_time=0.5):
    T = 0
    W = 0
    SW = 0
    X = 0
    SX = 0
    C = 0
    wait_times = []
    for i in range(100000):
        IA = get_inter_arrival_time(arrivals_rate)
        T += IA
        W += X - IA
        if W < 0: W = 0
        if W > 0: C += 1
        SW += W
        wait_times.append(W)
        if service_time_distribution == 1:
            X = get_exponential_service_time(mean_service_time)
        elif service_time_distribution == 2:
            X = 0.5
        elif service_time_distribution == 3:
            X = get_uniform_service_time()
        elif service_time_distribution == 4:
            X = get_discrete_service_time()
        SX += X
    p_wait_greater_than_half = sum([1 if W>0.5 else 0 for W in wait_times])/100000
    print(f'for service_time_distribution {service_time_distribution}')
    print(f'server utilization: {SX/T}')
    print(f'fraction of customers who must wait in the queue: {C/100000}')
    print(f'P(W>0.5): {p_wait_greater_than_half}')
    print(f'average waiting time: {SW/100000}')
    
    return wait_times
    
    
# if __name__ == '__main__':
    random.seed(123)
    # for service_time_distribution in [1,2,3,4]:
        # simulation(service_time_distribution)
        
    
    arrivals_rate = 1.6
    mean_service_time = 0.5
    rho = theory_server_utilization(arrivals_rate, mean_service_time)
    service_time_distribution = 1
    wait_times = simulation(service_time_distribution)
    probabilities = []
    for time in range(-1, 13):
        theory_prob_wait_less_than_t = cumulative_waiting_time_distribution_theory(rho, time, mean_service_time)
        print(f'With Poisson arrivals by theory Fw(t) = P(W <= {time}): {theory_prob_wait_less_than_t}')
        prob_wait_less_than_t = sum([1 if W <= time else 0 for W in wait_times])/100000
        print(f'From simulation the probability customer must wait <= {time} is: {prob_wait_less_than_t}')
        probabilities.append(prob_wait_less_than_t)
    


"""
STA 4821 Homework 6 (The M/G/1 Queue) 40 Points
The following BASIC code simulates the single-server queue with FIFO service.
It generates the interarrival times and the service times for
100,000 customers; and it produces estimates of
the server utilization,
the fraction of customers who must wait in the queue,
and the average waiting time.


100 FOR i = 1 TO 100000
110 IA = (generate interarrival time)
120 T = T + IA
130 W = W + X – IA
140 IF W < 0 THEN W = 0
150 IF W > 0 THEN c = c + 1
160 SW = SW + W
170 X = (generate service time)
180 SX = SX + X
190 NEXT i
200 PRINT SX/T, c/100000, SW/100000


Adapt the program and run it (using the language of your choice)
for four different service-time
distributions:

(1) exponential service times, with mean service time E(X) = 0.5
(2) constant service time, X = 0.5
(3) X ~ U(0,1)
(4) P(X=1/3) = 0.9, P(X=2)= 0.1

Assume that the interarrival times are exponentially distributed
with mean value 0.625 (that is, Poisson arrivals with rate lambda = 1.6).
Fill in the table.
For case (1), draw the graph of the theoretical distribution function
of waiting times, Fw(t);
and, on the same axes plot the simulation estimates at the values of t
as t goes from –1 to 12 in increments of 1, and fill in the corresponding
table.

Theory for the M/G/1 queue: If lambda is the arrival rate and X is the
service time, then the server utilization is
given by

rho = lambda * E(X)     if lambda * E(X) < 1
      1                 if lambda * E(X) >= 1

The probability that a customer must wait in the queue is

P(W > 0 ) = rho,

and the mean waiting time is given by the famous
Pollaczek-Khintchine formula,

E(W) = rho/(1-rho) * E(X)/2 * (1 + V(X)/E(X^2))

In addition, if the service times are exponentially distributed,
and the service is FIFO, then

Fw(t) = 0               (t<0)
      = 1 - rho * exp(-(1-rho)*t/E(X)) (t>=0)

There is no simple formula for Fw(t) when the service times are
not exponentially distributed. (Therefore, simulation is an important
tool for the analysis of queues whose service times have any
arbitrary specified distribution of service times; and the theoretical
results for the special case of exponential service times are
important because they can be used to check the logic and accuracy
of the simulation.)

    rho                         P(W > 0)                 P(W > 0.5)                         E(W)

X   theory  simulation          theory   simulation      theory             simulation      theory  simulation
1   0.8     0.7942998801384068  0.8      0.79469         0.654984602462385  0.6483          2       1.9397016082464402       
2   0.8     0.799593785266766   0.8      0.79902         NA                 0.55332         1       0.987778580473801
3   0.8     0.804452584152168   0.8      0.80287         NA                 0.62675         1.33    1.35960326098361
4   0.8     0.797830922857923   0.8      0.79928         NA                 0.61635         2       1.96042968144137


            Fw(t)
t   theory              simulation
-1  0                   0
0   0.2                 0.20531
1   0.463743963171489   0.47139
2   0.640536828706223   0.64609
3   0.759044630470238   0.76458
4   0.838482785604275   0.84369
5   0.89173177341071    0.89643
6   0.92742563736847    0.9319
7   0.951351949899826   0.95545
8   0.967390236817307   0.972
9   0.978141022042166   0.98274
10  0.985347488889013   0.98892
11  0.990178128077545   0.99233
12  0.993416202360784   0.99462

"""