import random
import math
import statistics
import pylab


__DEBUG__ = False

def log(text: str):
    if __DEBUG__:
        print(text)
        

def get_theory_p_0_p_1(num_wait_pos, offered_load, num_servers=1):
    p_array = [1]
    for j in range(1, num_servers+1):
        p_array_j = (offered_load**j / math.factorial(j)) * p_array[j - 1]
        p_array.append(p_array_j)
    sum_p_array = sum(p_array)
    p_array_final = [el/sum_p_array for el in p_array]
    assert 0.99999 < sum(p_array_final) < 1.00001
    return p_array_final
    
# test
# offered_load = 0.8
# print(get_theory_p_0_p_1(0,0.8))
    

def arriving_customers_distribution(num_wait_pos, offered_load):
    # follow exercise 21 p238
    p_array = [1]
    pass
    

def mean_busy_period(num_wait_pos, offered_load, p_0, p_1):
    """Inputs: n the number of waiting positions as an integer and the
    offered load, denoted a, as a float.
    
    Output: The mean busy period as a float in units of average service time.
    """    
    if n == 1: return (1 / p_0) * 1 # tau = 1, as working in units of average service time.

def prob_cust_lost(num_wait_pos, offered_load):
    """Inputs: n the number of waiting positions as an integer and the
    offered load, denoted a, as a float.
    
    Output: The probability that an arriving customer is lost, i.e., 
    not carried by the single server in the M/M/1/n model with
    Poisson arrivals, exponential service times, a single server and
    a finite number, n, waiting positions.  The probability is a float
    in the range (0, 1).
    """
    n = num_wait_pos
    a = offered_load
    p_0 = 1 / ( 1 + a * sum([a**i for i in range(n+1)]) )
    p_n_plus_one = a**(n+1) * p_0
    return p_n_plus_one
    
# test
# a = 0.8
# wait_positions = [0,1,2,4,8,16,32]
# for num_wait_pos in wait_positions:
    # print(f'for {num_wait_pos} waiting positions and offered load {a} the loss probability is: {prob_cust_lost(num_wait_pos, a)}') 
# a = 1.2
# for num_wait_pos in wait_positions:
    # print(f'for {num_wait_pos} waiting positions and offered load {a} the loss probability is: {prob_cust_lost(num_wait_pos, a)}') 

 
def get_theory_server_utilization(num_wait_pos, offered_load):
    loss_prob = prob_cust_lost(num_wait_pos, offered_load)
    return offered_load * (1 - loss_prob)
    
# test
# a = 0.8
# wait_positions = [0,1,2,4,8,16,32]
# for num_wait_pos in wait_positions:
    # print(f'for offered load {a} and {num_wait_pos} the theoretical server utilization is {get_theory_server_utilization(num_wait_pos, a)}')
    
# a = 1.2
# for num_wait_pos in wait_positions:
    # print(f'for offered load {a} and {num_wait_pos} the theoretical server utilization is {get_theory_server_utilization(num_wait_pos, a)}')
    
    
def get_average_wait_time_carried_customers(num_wait_pos, offered_load):
    n = num_wait_pos
    a = offered_load
    p_0 = 1 / (1 + a * sum([a**i for i in range(n + 1)]))
    p_array = [p_0]
    for j in range(1, n + 2):
        prob_j = a**j * p_0
        p_array.append(prob_j)
    average_queue_length = sum([j * prob for j, prob in enumerate(p_array[2:], start=1)])
    average_waiting_time = average_queue_length / offered_load
    return average_waiting_time
    
# test
# a = 0.8
# wait_positions = [0,1,2,4,8,16,32]
# for num_wait_pos in wait_positions:
    # print(f'for offered load {a} and {num_wait_pos} the theoretical average waiting time for carried customers is {get_average_wait_time_carried_customers(num_wait_pos, a)}')
    
# a = 1.2
# for num_wait_pos in wait_positions:
    # print(f'for offered load {a} and {num_wait_pos} the theoretical average waiting time for carried customers is {get_average_wait_time_carried_customers(num_wait_pos, a)}')

    
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
        
           
def run_simulation(num_wait_pos, offered_load, NSTOP=100000, S=1):
    wait_pos_status = [0 * i for i in range(num_wait_pos)]    # Array to hold state of the n waiting positions.  Let 0 denote waiting position unoccupied and 1 denote waiting position occupied.
    SCT = 0                         # completion time server.
    T = 0                           # current time.
    K = 0                           # number blocked customers.
    W = 0                           # Initialize waiting time.
    SW = 0                          # Initialize cumulative waiting time.
    CW = 0                          # count of customers who had to wait for service.
    SX = 0                          # Cumulative service time.
    wait_times = []
    for d in range(NSTOP):
        log(f'customer: {d}, SCT: {SCT}')
        IA = get_inter_arrival_time(offered_load)   # Take mu = 1 by convention.  a = lambda/mu, i.e., a = lambda or offered load = arrival rate.
        T += IA                                     # The arrival time for customer d.
        log(f'IA: {IA}, T: {T}')
        if T < SCT:                                 # Has customer interrupted service / Is the server busy?
            log(f'customer has interrupted service, T: {T} < SCT: {SCT}')
            if len(wait_pos_status) > 0 and any([el == 0 for el in wait_pos_status]):  # Any available positions in queue?
                log(f'There is a queue and it has available positions, wait_pos_status: {wait_pos_status}')
                W = SCT - T                      # waiting time = waiting time previous customer + service time previous customer - time I arrived?
                log(f'wait time = SCT: {SCT} - T: {T} == {W}')
                if W < 0:                           # Is waiting time negative?
                    log('wait time negative')
                    W = 0                           # Set waiting time as zero.
                    X = get_service_time(1)         # Generate my service time.
                    log(f'service time: {X}')
                    SCT = T + X                     # Service completion time is current time + service time.
                    log(f'server completion time == T: {T} + X: {X}: {SCT}')
                    SX += X                         # Increment cumulative service time.
                    log(f'cumulative service time: {SX}')
                if W > 0:                           # Customer had to wait?
                    log(f'wait time W: {W} is positive')
                    CW += 1                          # If waiting time positive increment count of customers who had to wait.
                    log(f'after increment count of number of customers who have had to wait: {CW}')
                    ndx = wait_pos_status[::-1].index(0)  # Get index of smallest value in waiting postion array from end.
                    log(f'index from right end of first available waiting position: {ndx}')
                    wait_pos_status[-ndx-1] = 1           # Change status to 1, to denote waiting position is occupied.
                    log(f'new waiting position status: {wait_pos_status}')
                    log(f'waiting time: {W}, before cumulative waiting time: {SW}')
                    SW += W                             # Increment cumulative waiting time.
                    log(f'after increment cumulative waiting time: {SW}')
                    wait_times.append(W)
                    log(f'cumulative waiting time: {SW}')
                    X = get_service_time(1)             # Generate my service time.
                    log(f'service time: {X}')
                    SCT += X                            # Increment server completion time.
                    log(f'server completion time == old SCT + X: {X}, i.e., {SCT}')
                    SX += X                             # Increment cumulative service time.
                    log(f'cumulative service time: {SX}')
            else:                                   # There are waiting positions but all are occupied.
                K += 1                              # Increment count of customers lost.
                log(f'no queue or there is a queue but it was full.  # customers lost: {K}')
        else:                                       # When customer arrives server is idle.
            log(f'customer has NOT interrupted service, T: {T} > SCT: {SCT}')
            wait_times.append(0)
            X = get_service_time(1)                 # Straight to service for time X.
            log(f'service time: {X}')
            SCT = T + X                                # Increment server completion time.
            log(f'server completion time == T: {T} + X: {X}: {SCT}')
            SX += X                                 # Increment cumulative service time.
            log(f'cumulative service time: {SX}')
            if len(wait_pos_status) > 0:            # Is there a queue?
                # log('there is a queue about to reset waiting positions')
                # wait_pos_status.clear()               # First customer into queue is first customer out of queue to get service.
                # wait_pos_status = [0 * i for i in range(num_wait_pos)]        # Enter an available space at the back of the queue to re-establish the number of waiting positions.
                # log(f'new waiting position status: {wait_pos_status}')
                for i, el in enumerate(wait_pos_status):
                    if el > 0:
                        ndx = i
                        wait_pos_status[ndx] = 0
                        break
            
    
    print(f'for n: {num_wait_pos} and offered load, a: {offered_load}..')
    # print(f'T: {T}, K: {K}, SW: {SW}, SX: {SX}, CW: {CW}, (NSTOP - K): {NSTOP - K}')
    print(f'server utilization by simulation: {SX/T}')
    # print(f'proportion of carried customers who have to wait: {CW/(NSTOP - K)}')
    # print(f'average service time per carried customer: {SX/(NSTOP - K)}')
    print(f'average waiting time per carried customer by simulation: {SW/(NSTOP - K)}')
    # print(f'mean wait time: {statistics.mean(wait_times)}')
    # print(f'number of customers lost: {K}')
    print(f'proportion of customers lost: {K/NSTOP}')
    

if __name__ == '__main__':
    random.seed(123)
    print(run_simulation(0, 0.8))
    
    
    
"""
MAP 6264 Homework 5 ( M/M/1/n ) 20 Points
Consider the M/M/1/n queue (finite waiting room, that is, a buffer
with n waiting positions). Write a simulation program for this model,
and compare the simulation results with the predictions of queueing
theory.
Specifically, let W(n) denote the average waiting time (in units of
average service time) for those customers who receive service (that is,
those customers who do not overflow the buffer) when the capacity of
the buffer is n; and fill in the tables.
In the first case, take a = 0.8 erlangs;
in the second case, take a = 1.2 erlangs.
Show the simulation code and output. Explain all theoretical calculations.


"""