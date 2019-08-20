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
    

def get_theory_p(num_sources, num_servers=10, intended_offered_load=9.6):
    a_hat = get_offered_load_per_idle_source(num_sources, intended_offered_load)
    p_array = [1]
    for j in range(1, num_servers+1):
        p_array_j = ((num_sources - (j - 1)) * a_hat * p_array[j - 1]) / j
        p_array.append(p_array_j)
    sum_p_array = sum(p_array)
    p_array_final = [el/sum_p_array for el in p_array]
    assert 0.99999 < sum(p_array_final) < 1.00001
    return p_array_final[-1]
    
    
def get_theory_server_utilization_rho(prob_all_servers_busy, num_sources, num_servers=10, intended_offered_load=9.6):
    carried_load = intended_offered_load * (1 - (1 - (num_servers / num_sources)) * prob_all_servers_busy)
    server_utilization = carried_load / num_servers
    return server_utilization
    

def get_best_time_next_source(source_array):
    min_time = min(source_array)
    source_ndx = source_array.index(min_time)
    return min_time, source_ndx
    
    
def get_offered_load_per_idle_source(num_sources, intended_offered_load):
    return intended_offered_load / (num_sources - intended_offered_load)
    
    
def prob_source_busy_no_interaction(offered_load_per_idle_source):
    return offered_load_per_idle_source / (1 + offered_load_per_idle_source)
    
    
def get_rate_for_source_when_idle(offered_load_per_idle_source, avg_service_time):
    return offered_load_per_idle_source / avg_service_time
    
    
def get_think_time(rate_for_source_when_idle):
    return -(1 / rate_for_source_when_idle) * math.log(1 - random.random())

    
def get_service_time(avg_service_time):
    return -(avg_service_time) * math.log(1 - random.random())
        
           
def run_simulation(NSTOP=1000000, num_sources=1000, S=10, intended_offered_load=9.6, avg_service_time=2.4):
    C = [0 * i for i in range(S)]   # completion times servers.
    source_array = [0 * i for i in range(num_sources)] # Holds times at which each source is next going to generate a request for service.
    A = 0                           # current time.
    K = 0                           # number blocked customers.
    AB = 0                          # cumulative time all servers busy.
    
    for d in range(NSTOP):
        IA, ndx = get_best_time_next_source(source_array)   # Case 1 & 2, otherwise (1/4) for case 3 & 4.
        A = IA                                     # The arrival time for customer d.
        log(f'IA: {IA}, A: {A}')
        # Having moved clock to new time, update source_array, S.
        # Need to generate think time, whether or not source is carried.
        a_hat = get_offered_load_per_idle_source(num_sources, intended_offered_load)
        gamma = get_rate_for_source_when_idle(a_hat, avg_service_time)
        think_time = (1/gamma)#get_think_time(gamma)# (1/gamma) case 3
        J = 0                                       # Next server to be probed.
        while A < C[J]:
            J += 1
            if J == S:
                K += 1
                # Because source did not find an idle server add only think time.
                source_array[ndx] += think_time
                break
        else:
            X = get_service_time(avg_service_time) # 2.4 case 2
            C[J] = A + X
            # Add service time plus think time to source array for the source that has been in service.
            source_array[ndx] += (X + think_time)
            M = C[0]
            for i in range(1, S):
                if C[i] < M:
                    M = C[i]
            if M > A:
                AB += M - A
                
    print(f'# servers: {S}, # sources: {num_sources}, K: {K}; AB: {AB}; A: {A}')    
    print(f'fraction of customers blocked: {K/NSTOP}')  # Fraction of customers blocked
    rho = (intended_offered_load * (1 - (1 - (S / num_sources)) * K/NSTOP)) / S
    print(f'from simulation server utilization, rho: {rho}')
    if A != 0:
        print(f'fraction of time all servers simultaneously busy: {AB/A}')
    else:
        print(f'fraction of time all servers simultaneously busy: 0')
    
  
if __name__ == '__main__':
    random.seed(123)
    print(run_simulation())
    
    # test
    # table1_results = []
    # table2_results = [0]
    # table3_results = []
    # for i, num_sources in enumerate([10, 11, 12, 13, 14, 15, 25, 50, 100, 1000, 100000, 1000000, 10000000]):
        # p = get_theory_p(num_sources)
        # table1_results.append(p)
        # if i > 0:
            # pi = get_theory_p(num_sources - 1)
            # table2_results.append(pi)
            
        
        # print(f'for 10 servers probability that 10 sources are busy when we have {num_sources} is..')
        # print(f'... {get_theory_p(num_sources)}')
        # prob_all_servers_busy = table1_results[i]
        # rho = get_theory_server_utilization_rho(prob_all_servers_busy, num_sources)
        # table3_results.append(rho)
    # print(f'table 1 probabilities by theory: {table1_results}')
    # print(f'table 2 probabilities by theory: {table2_results}')
    # print(f'table 3 probabilities by theory: {table3_results}')  
    
    
"""
MAP 6264 Homework 4 (Finite-Source Input, BCC) 30 Points
Adapt the simulation program of Homework 1 (Blocked Customers Cleared) to
account for finite-source input. Consider the three cases:
1. Exponential think times (quasirandom input), exponential service times.
2. Exponential think times, constant service times.
3. Constant think times, exponential service times.
Assume that s = 10 servers; and, for each value of n (number of sources),
calculate (offered load per idle source) so that (intended offered load)
is 9.6 erlangs.
Run each simulation for as many arrivals as necessary to attain statistical
stability. When n = inf (in Case 1 and Case 2) use the simulation of Homework 1.
(Note that for every value of n, the theory values are the same for each case,
because of insensitivity of the equilibrium probabilities to the think times
and the service times). Fill in the tables. Attach code for simulation and
theory; and explain all calculations.

                        Ps[n]
-------------------- simulation ------------------------------
n     theory                    1           2           3
10    0.6648326359915008
11    0.35885046596037773
12    0.28346784153599996
13    0.24674680315057632
14    0.22447326026076037
15    0.20934740209906252
25    0.1590032352301863
50    0.1383991712291617
100   0.1306700041840892
1000  0.12470079531588751
1mil  0.12408646371214853
∞     0.19949055155314457


                        Πs[n]
-------------------- simulation ------------------------------
n       theory                1           2           3
10      0.0
11      0.6648326359915008
12      0.35885046596037773
13      0.28346784153599996
14      0.24674680315057632
15      0.22447326026076037
25      0.20934740209906252
50      0.1590032352301863
100     0.1383991712291617
1000    0.1306700041840892
1 mill  0.12470079531588751
∞       0.19815


                       rho
-------------------- simulation ------------------------------
n     theory                1           2           3
10    0.96
11    0.9286821411525488
12    0.9146451453542401
13    0.9053360928404877
14    0.8984301914713342
15    0.8930088313282999
25    0.8684141365074127
50    0.8537094364960037
100   0.8471011163849468
1000  0.8414843641317805
1 mil 0.840878186066389 
∞     0.7684890705089812                   
"""
