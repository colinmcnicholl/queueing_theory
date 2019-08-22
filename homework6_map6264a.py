import random
import math

    
def earlang_B_rec(n, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
    Earlang loss formula:
    
    B(n,a) = ( a * B(n-1, a) ) / ( n + a*B(n-1, a) )
    
    B(0, a) = 1.
    
    Output: The probability that all s servers are busy.
    """
    if n == 0: return 1
    
    return a * earlang_B_rec(n-1, a) / (n + a*earlang_B_rec(n-1, a))


def earlang_C(s, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
    Earlang delay formula:
    
    For every integer s > a,
    
    C(s, a) = ( s * B(s, a) ) / ( s - a*(1 - B(s, a)) )
    
    Output: The probability that all s servers are busy.
    """
    assert s > a
    
    return (s * earlang_B_rec(s, a)) / (s - a*(1 - earlang_B_rec(s, a)))
    

def get_inter_arrival_time(arrival_rate):
    return -(1 / arrival_rate) * math.log(1 - random.random())

    
def get_service_time(avg_service_time):
    return -(avg_service_time) * math.log(1 - random.random())
    
def get_available_pos(WP):
    for i, el in enumerate(WP):
        if el[0] == 0:
            return i
    return None
    
def update_wp(IA, A, WP):
    if not WP: return []
    for i, el in enumerate(WP): # loop over each customer in waiting position array.
        if A - el[1] >= el[0]:  # (arrival time newly arrived customer - arrival time waiting customer) >= waiting time for the waiting customer?
            WP[i] = (0, 0)      # Then the waiting customer is no longer waiting.
    return WP
    
           
def run_simulation(buffer_size, offered_load, NSTOP=100000):
    WP = [(0,0)] * buffer_size   # waiting position status.
    A = 0                           # current time.
    W = 0                           # Current waiting time.
    SW = 0                          # Sum of waiting times.
    X = 0                           # Current service time.
    SC = 0                          # Server completion time.
    K = 0                           # number blocked customers.
    SX = 0                          # Cumulative service time.
    CWC = 0                         # Count of number of customers who have to wait.
    for d in range(NSTOP):
        IA = get_inter_arrival_time(offered_load)   # Inter-arrival time.
        A += IA                                     # The arrival time for customer d.
        WP = update_wp(IA, A, WP)
        if A < SC:
            if not WP or all([el[0] > 0 for el in WP]):
                K += 1
            else:
                W = SC - A
                assert W >= 0
                SW += W
                ndx = get_available_pos(WP)
                WP[ndx] = (W, A)
                X = 1 # Constant service times.  HW5 get_service_time(1)
                SC = A + W + X
                SX += X
                CWC += 1
        else:
            assert (all([el == (0, 0) for el in WP]))
            X = 1 # Constant service times.  HW5 get_service_time(1)
            SC = A + X
            SX += X
            CWC += 1
            
    print(f'for n: {buffer_size} and offered load, a: {offered_load}..')
    print(f'server utilization by simulation: {SX/A}')
    print(f'proportion of customers lost: {K/NSTOP}')
    print(f'average waiting time per carried customer by simulation: {SW/CWC}')
    assert ((NSTOP - K) == CWC)
    
    

if __name__ == '__main__':
    random.seed(123)
    print(run_simulation(64, 1.2))
    
"""
MAP 6264 Homework 6 ( M/D/1/n ) 20 Points
Repeat Homework 5, but now assume that the service times are constant:
Consider the M/D/1/n queue (finite waiting room, that is, a buffer with n waiting positions). Write a
simulation program for this model, and compare the simulation results with the predictions of queueing
theory.
Specifically, let W(n) denote the average waiting time (in units of average service time) for those
customers who receive service (that is, those customers who do not overflow the buffer) when the
capacity of the buffer is n; and fill in the tables. In the first case, take a = 0.8 erlangs; in the second case,
take a = 1.2 erlangs. Show the simulation code and output. Explain all theoretical calculations.

                            Case 1
    ρ                               Πn+1                        W(n)
n   theory      simulation          theory      simulation      theory    simulation
0               0.443372407920764               0.44373                   0                                                              
1               0.637963055753247               0.19959                   0.311726449613646                                                                                        
2               0.714981546373599               0.10296                   0.660050295010785 
4               0.769276274522811               0.03484                   1.19592486583925
8               0.792462323287647               0.00575                   1.71747375246176
16              0.796909836251132               0.00017                   1.94081139444109
32              0.797045333957905               0                         1.95189906309966
∞   0.8                             0.0                          2


                            Case 2
    ρ                               Πn+1                            W(n)
n   theory      simulation          theory      simulation          theory      simulation
0               0.543947573386236               0.54503                         0 
1               0.797635147505025               0.33284                         0.417748524368096
2               0.891905684378895               0.25399                         1.00316332935241
4               0.959897636592173               0.19712                         2.38536632548293
8               0.99252468733774                0.16983                         5.68402612515239
16              0.999662228303333               0.16386                         13.3160636900466
32              1.00029587934383                0.16333                         29.2412930636757
∞   1.0                             1.0                             infinity

"""
