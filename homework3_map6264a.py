import random
import math
import statistics
import pylab


__DEBUG__ = False

def log(text: str):
    if __DEBUG__:
        print(text)
        
def earlang_B(s, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
    Earlang loss formula:
    
    B(s,a) = (a^s / s!) / sum{k=0 to k=s} (a^k / k!)
    
    Output: The probability that all s servers are busy.
    """
    numerator = a**s / math.factorial(s)
    denominator_elems = []
    for k in range(s+1):
        num = a**k / math.factorial(k)
        denominator_elems.append(num)
    return numerator / sum(denominator_elems)
    
# test
# print(f'probablity that all 2 servers are busy with carried load 9.6 is: {earlang_B(2, 1.8)}')
s = 10
a = 9.6
print(f'For {s} servers and offered load {a} the probability that all servers are busy..')
print(f'by earlang_B formula: {earlang_B(s, a)}')
    
    
def earlang_B_rec(n, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
    Earlang loss formula:
    
    B(n,a) = ( a * B(n-1, a) ) / ( n + a*B(n-1, a) )
    
    B(0, a) = 1.
    
    Output: The probability that all s servers are busy.
    """
    if n == 0: return 1
    
    return a * earlang_B_rec(n-1, a) / (n + a*earlang_B_rec(n-1, a))
    
# test
n = 10
a = 9.6
print(f'For {n} servers and offered load {a} the probability that all servers are busy..')
print(f'by earlang_B recursive formula: {earlang_B_rec(n, a)}')


def earlang_C(s, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
    Earlang delay formula:
    
    For every integer s > a,
    
    C(s, a) = ( s * B(s, a) ) / ( s - a*(1 - B(s, a)) )
    
    Output: The probability that all s servers are busy.
    """
    assert s > a
    
    return (s * earlang_B_rec(s, a)) / (s - a*(1 - earlang_B_rec(s, a)))
    
# test
# s = 2
# a = 1.8
# print(f'For {s} servers and offered load {a} the probability that all servers are busy..')
# print(f' by the Earlang delay formula is: {earlang_C(s, a)}')
s = 10
a = 9.6
print(f'For {s} servers and offered load {a} the probability that all servers are busy..')
print(f'by the Earlang delay formula is: {earlang_C(s, a)}')


def get_inter_arrival_time(arrival_rate):
    return -(1 / arrival_rate) * math.log(1 - random.random())

    
def get_service_time(avg_service_time):
    return -(avg_service_time) * math.log(1 - random.random())
    
def first_available_server_and_time(server_status):
    min_time = min(server_status)
    next_avail_server = server_status.index(min_time)
    return next_avail_server, min_time
    
def prob_wait_greater_than(t, wait_times):
    results = [1 if el/(t*2.4) > 1 else 0 for el in wait_times]
    prob_greater_than_t = sum(results)/len(results)
    return prob_greater_than_t
    
           
def run_simulation(NSTOP=1000000, S=10, arrival_rate=4, avg_service_time=2.4):
    C = [0 * i for i in range(S)]   # completion times servers.
    A = 0                           # current time.
    K = 0                           # number blocked customers.
    AB = 0                          # cumulative time all servers busy.
    SX = 0                          # Cumulative service time.
    wait_times = []                 # Collect waiting times for post analysis.
    data = []
    for d in range(NSTOP):
        log(f'customer: {d}, C: {C}')
        IA = get_inter_arrival_time(arrival_rate)   # Case 1 & 2, otherwise (1/4) for case 3 & 4.
        # interarrival_times.append(IA)
        A += IA                                     # The arrival time for customer d.
        log(f'IA: {IA}, A: {A}')
        J = 0                                       # Next server to be probed.
        log(f'next server to be probed: {J}')
        while A < C[J]:
            log(f'inside if so arrival time: {A} before server {J} is available at time {C[J]}')
            J += 1
            log(f'probe next server in line: {J}')
            if J == S:
                log(f'inside if so server index {J} exceeds max server index {S-1}')
                K += 1
                # Find next server to become available and at what time.
                J, M = first_available_server_and_time(C)
                log(f'next free server {J} at time: {M}')
                W = M - A       # Waiting time.
                log(f'customer {d} has to wait: {W}')
                wait_times.append(W)
                AB += W
                X = get_service_time(avg_service_time)
                log(f'service time: {X}')
                SX += X
                log(f'cumulative service time: {SX}')
                C[J] = M + X
                data.append((d, IA, A, W, J, S))
                log(f'customer {d} arrived at time : {A}, waited until time: {M}, started service with server: {J} for duration: {X}')
                log(f'after update server completion times: {C} about to go to next customer')
                # Next customer
                break
        else:
            log(f'inside else so arrival time {A} after server {J} completion time {C[J]}')
            wait_times.append(0)
            X = get_service_time(avg_service_time)
            SX += X
            log(f'SX: {SX}')
            log(f'current time: {A}; service time: {X}; add these gives: {A+X}')
            C[J] = A + X
            log(f'updated service completion times: {C}')
            data.append((d, IA, A, 0, J, S))
    
    mean_wait_time = statistics.mean(wait_times)
    print(f'statistical mean of wait_times: {mean_wait_time}')
    
    log(f'len(wait_times) : {len(wait_times)} == NSTOP: {NSTOP}')
    average_wait_time_per_unit_time = (1/avg_service_time)*sum(wait_times) / len(wait_times)
    # avg_wait_per_unit_service_time = average_wait_time / avg_service_time
    # print(f'last 10 wait_times: {wait_times[-10:]}')
    # print(f'avg_wait_per_unit_service_time: {avg_wait_per_unit_service_time}')
    num_cust_no_wait = wait_times.count(0)
    # print(f'{num_cust_no_wait} customers have no wait.')
    # print(f'{K} customers have some wait.')
    # print(f'wait times: {wait_times}')
    carried_load = (SX/A)
    print(f'Simulation carried load: {carried_load}')
    theory_loss_system_carried_load = (arrival_rate*avg_service_time) * (1 - earlang_B(S, arrival_rate*avg_service_time))
    print(f'from theory loss system carried load: {theory_loss_system_carried_load}')
    RHO = carried_load/10
    print(f'Simulation Server utilization, RHO: {RHO}')
    theory_delay_system_rho = (arrival_rate*avg_service_time)/S
    print(f'theory delay system rho: {theory_delay_system_rho}')
    assert (len(wait_times) - num_cust_no_wait) == K
    print(f'Simulation E(W) per unit time: {average_wait_time_per_unit_time}') 
    # theory_delay_system_expected_value_wait_time_per_unit_time = ((earlang_C(S, arrival_rate*avg_service_time))/((1-theory_delay_system_rho)*S))
    # print(f'By theory delay system expected value for wait time: {theory_delay_system_expected_value_wait_time_per_unit_time}')
    print(f'AB/A: {AB/A}')
    # print(f'theory delay system earlang_C {S} servers, offered load: {arrival_rate*avg_service_time}, C(s,a): {earlang_C(S, arrival_rate*avg_service_time)}')
    print(f'K/NSTOP: {K/NSTOP}')
    
    sim_probs = [K/NSTOP]
    for t in range(1,9):
        prob = prob_wait_greater_than(t, wait_times)
        sim_probs.append(prob)
        print(f'probability W > {t}: {prob}')
        
    theory_probs = []
    for t in [t*2.4 for t in range(9)]:
        prob_wait_greater_than_t = earlang_C(S, arrival_rate*avg_service_time)*math.exp(-1*(1-theory_delay_system_rho)*S*(1/avg_service_time)*t)
        theory_probs.append(prob_wait_greater_than_t)
        print(f'by theory delay system probablity wait greater than {t} time units is: {prob_wait_greater_than_t}')
        
    log(f'data: {data}')

if __name__ == '__main__':
    random.seed(123)
    print(run_simulation())
    
    x = list(range(9))
    theory_probs = [0.8590803440134663, 0.5758587757474194, 0.38600968106903694, 0.25875002718439916, 0.17344533013396932, 0.11626388168006893, 0.07793401052006589, 0.052240729519552526, 0.035018008216481836]
    sim_case1_probs = [0.85967, 0.574334, 0.38659, 0.265105, 0.178798, 0.119471, 0.081273, 0.056299, 0.03944]
    sim_case2_probs = [0.845178, 0.38427, 0.168627, 0.071811, 0.028784, 0.010539, 0.003378, 0.001134, 0.000469]
    fig = pylab.figure()
    ax = fig.add_subplot()
    ax.plot(x, theory_probs, color='lightblue', linewidth=3)
    ax.scatter(x, sim_case1_probs, color='darkgreen', marker='x')
    ax.scatter(x, sim_case2_probs, color='red', marker='o')
    ax.set(title='Case1: exponential arrivals & service, Case2: const. service time', ylabel='P(W>t)', xlabel='t')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    pylab.show()
    
    
"""
MAP 6264 Homework 3 (Blocked Customers Delayed) 30 Points
Augment your code of Homework 1 (Blocked Customers Cleared) so that
it will now describe the case where the blocked customers wait in an
infinite-capacity queue and are served in FIFO order.
Include code and output.

1. Fill in the table. Cases 1-4 use the same assumptions as Homework 1
    about the input process and the service times. In each "theory" box
    write the theoretical value if you can calculate it; if not, write NA.
    In Case 1, show all formulas used; in every other case, if you give a
    "theory" answer, explain how you arrived at that answer. Run each
    simulation for at least 100,000 arrivals (1,000,000 if feasible).
    Take the unit of measurement to be the average service time
    (2.4 seconds), and take the number of servers to be 10.
2. Draw the graph of P(W > t) versus t (measured in units of average
    service time) for Case 1 when the arrival rate is 4 customers per second,
    and plot the corresponding simulation points given in the table.
    On the same graph, plot the simulation points for Case 2 (to illustrate
    that the probabilities are not insensitive to the distribution of
    service times; for clarity, use different symbols for the simulation
    points for each case).
3. Repeat question (1) with the arrival rate increased to 4.2 arrivals per second.

100 DIM C(50) (50 is max number of servers)
110 INPUT S,NSTOP (S,NSTOP = number of servers, customers to be simulated)
120 FOR D=1 TO NSTOP
130 IA= (IA = interarrival time)
140 A=A+IA (A = arrival time)
150 J=0
160 J=J+1 (J = index of server being probed)
170 IF J=S+1 THEN K=K+1 (K = number of customers that are blocked)
180 IF J=S+1 THEN 270
190 IF A<C(J) THEN 160 (C(J) = completion time for server J)
200 X= (X = service time)
210 C(J)=A+X
220 M=C(1) (M = shortest server-completion time)
230 FOR I=2 TO S
240 IF C(I)<M THEN M=C(I)
250 NEXT I
260 IF M>A THEN AB=AB+M-A (AB = cumulative time during which all servers busy)
270 NEXT D
280 PRINT K/NSTOP,AB/A (fraction of customers blocked, fraction of time all servers are simultaneously busy

B(s,a) = (a^s / s!) / sum{k=0 to k=s} (a^k / k!)
B(5, 9.6) = (9.6^5/5!) / (9.6^0/0! + 9.6^1/1! + 9.6^2/2! + 9.6^3/3! + 9.6^4/4! + 9.6^5/5!)
          = (679.477248) / (1 + 9.6 + 46.08 + 147.456 + 353.8944 + 679.477248)
          = (679.477248) / (1237.507468)
          = 0.5490691303
"""