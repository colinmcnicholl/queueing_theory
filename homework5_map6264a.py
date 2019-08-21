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
                X = get_service_time(1)
                SC = A + W + X
                SX += X
                CWC += 1
        else:
            assert (all([el == (0, 0) for el in WP]))
            X = get_service_time(1)
            SC = A + X
            SX += X
            CWC += 1
            
    print(f'for n: {buffer_size} and offered load, a: {offered_load}..')
    print(f'server utilization by simulation: {SX/A}')
    print(f'proportion of customers lost: {K/NSTOP}')
    print(f'average waiting time per carried customer by simulation: {SW/CWC}')
    print(f'A/NSTOP: {A/NSTOP}')
    assert ((NSTOP - K) == CWC)
    
if __name__ == '__main__':
    random.seed(123)
    print(run_simulation(2, 0.8))
    
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

                            Case 1
                ρ                                               Πn+1                                   W(n)
n   theory                  simulation              theory                  simulation          theory                  simulation
0   0.4444444444444445      0.44452213471194785     0.4444444444444445      0.44461             0.0                     0.0
1   0.5901639344262295      0.5887282238183281      0.26229508196721313     0.2612              0.32786885245901637     0.4457431030123395
2   0.6612466124661247      0.6581555890835649      0.1734417344173442      0.17317             0.7046070460704608      0.8516817584312503
4   0.7289444010755486      0.7282888480653664      0.08881949865556424     0.08962             1.4242345389886373      1.567585604438412     
8   0.7759419500796657      0.7744750008776795      0.03007256240041786     0.03128             2.526444442379526       2.6224316346544425
16  0.7963310259372157      0.8007682248130787      0.004586217578480438    0.00429             3.591826635515242       3.7715671316553983
32  0.7998985365038771      0.8018415509683205      0.0001268293701537039   0.00016             3.978565836444025       4.138040575607979
∞


                            Case 2
                ρ                                       Πn+1                                            W(n)
n   theory                  simulation              theory                  simulation          theory                  simulation
0   0.5454545454545455      0.5430735123149999      0.5454545454545454      0.54133             0.0                     0.0
1   0.7252747252747254      0.7251686998249892      0.39560439560439553     0.39709             0.3296703296703296      0.5497540034312383
2   0.8137108792846497      0.8123973071185027      0.32190760059612517     0.32112             0.760059612518629       1.1219161711070293
4   0.8992942541329639      0.9003456814294474      0.25058812155586346     0.25254             1.768231768231768       2.382712481008391
8   0.9614772431171408      0.9589251527256454      0.19876896406904926     0.19809             4.137217167521513       5.14582037940748
16  0.9921946142678791      0.9915536155092198      0.17317115477676737     0.1698              9.758575084685834       11.684301705789991
32  0.9995928533750761      0.9999363686415371      0.16700595552076986     0.16661             22.558018394051654      27.05288191507914
∞

"""
