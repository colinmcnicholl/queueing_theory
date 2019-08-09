import random
import math

__DEBUG__ = False

def log(text: str):
    if __DEBUG__:
        print(text)
        
def earlang_B(s, a):
    """Inputs: 's' the number of servers, 'a' the offered load in Earlangs.
    
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
# print(f'probablity that all 15 servers are busy with carried load 9.6 is: {earlang_B(15, 9.6)}')
# # 0.029131042132999503
# print(f'probablity that all 12 servers are busy with carried load 9.6 is: {earlang_B(12, 9.6)}')
# # 0.10464675636104714
# print(f'probablity that all 10 servers are busy with carried load 9.6 is: {earlang_B(10, 9.6)}')
# # 0.19604433570789698 vs Expected 0.1960443357
# print(f'probablity that all 10 servers are busy with carried load 10.08 is: {earlang_B(10, 10.08)}')
# # 0.2182604405754659
# print(f'probablity that all 10 servers are busy with carried load 12.00 is: {earlang_B(10, 12.00)}')
# # 0.30192504028637934
# print(f'probablity that all 7 servers are busy with carried load 9.6 is: {earlang_B(7, 9.6)}')
# # 
# print(f'probablity that all 5 servers are busy with carried load 9.6 is: {earlang_B(5, 9.6)}')
# # 0.5490691302782154 vs expected 0.5490691303
# print(f'probablity that all 4 servers are busy with carried load 9.6 is: {earlang_B(4, 9.6)}')
# # 0.6341848042687279
# print(f'probablity that all 3 servers are busy with carried load 9.6 is: {earlang_B(3, 9.6)}')
# # 0.7223419680996982
# print(f'probablity that all 2 servers are busy with carried load 9.6 is: {earlang_B(2, 9.6)}')
# 


def get_inter_arrival_time(arrival_rate):
    return -(1 / arrival_rate) * math.log(1 - random.random())

    
def get_service_time(avg_service_time):
    return -(avg_service_time) * math.log(1 - random.random())
        
           
def run_simulation(NSTOP=1000000, S=10, arrival_rate=4, avg_service_time=2.4):
    C = [0 * i for i in range(S)]   # completion times servers.
    A = 0                           # current time.
    K = 0                           # number blocked customers.
    AB = 0                          # cumulative time all servers busy.
    
    for d in range(NSTOP):
        log(f'customer: {d}, C: {C}')
        IA = get_inter_arrival_time(arrival_rate)   # Case 1 & 2, otherwise (1/4) for case 3 & 4.
        A += IA                                     # The arrival time for customer d.
        log(f'IA: {IA}, A: {A}')
        J = 0                                       # Next server to be probed.
        log(f'next server to be probed: {J}')
        while A < C[J]:
            log(f'inside if so arrival time: {A} before server {J} is available at time {C[J]}')
            J += 1
            log(f'probe next server in line: {J}')
            if J == S:
                log(f'inside if so server index {J} exceeds max server index {S-1}; K: {K}')
                K += 1
                log(f'number blocked customers now: {K}')
                break
        else:
            log(f'inside else so arrival time {A} after server {J} completion time {C[J]}')
            X = get_service_time(avg_service_time)
            log(f'current time: {A}; service time: {X}; add these gives: {A+X}')
            C[J] = A + X
            log(f'updated service completion times: {C}')
            M = C[0]
            log(f'initialized minimum service completion time as: {M}')
            for i in range(1, S):
                log(f'loop over other service completion times to get minimum, server: {i}')
                if C[i] < M:
                    log(f'inside if so server {i} has completion time {C[i]} < current min: {M}')
                    M = C[i]
                    log(f'new minimum service completion time: {M}')
            log(f'after finish loop minimum service completion time: {M}')
            if M > A:
                log(f'inside if so minimum service completion time: {M} > current time: {A}')
                log(f'before AB: {AB}; (M-A): {M-A}')
                AB += M - A
                log(f'after AB: {AB}')
    print(f'K: {K}; AB: {AB}; A: {A}')    
    print(K/NSTOP, AB/A)  # Fraction of customers blocked, fraction of time all servers simultaneously busy.
    carried_load_simulation = arrival_rate * avg_service_time * (1 - (AB/A))
    server_utilization_simulation = carried_load_simulation / S
    print(f'server utilization from simulation: {server_utilization_simulation}')
  
if __name__ == '__main__':
    random.seed(123)
    print(run_simulation())
        
    
"""
MAP 6264 Homework 1 (Blocked Customers Cleared) 10 Points
Run the BASIC code below for each of the four specified cases,
and fill in the table below. (You may translate into any other
computer language, but don't blame me if you introduce bugs.)
In each case, make the arrival rate to be 4 and the
average service time 2.4 (so that the offered load is 4 x 2.4 = 9.6 erlangs);
set the number of servers to be 10;
and run the simulation for 10,000 arriving customers.
Observe that all the answers in row 1 and row 2 are, in principle, equal.
1. Poisson arrivals, exponential service times.
2. Poisson arrivals, constant service times.
3. Constant interarrival times, exponential service times.
4. Constant interarrival times, constant service times.

homework1_map626g.py
With 10 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)              seed
1   0.19815     0.19949055155314457     0.19604433570789698 1000000 customers: 
2   0.19559     0.1942698070155423      0.19604433570789698 1000000 customers: 
3   0.1371      0.24242003733822218     NA                  1000000 customers: 
4   0.0         0.5999460000013329      NA

server utilization from simulation: 0.7684890705089812
With NSTOP = 1000000:
server utilization from simulation: 0.7710475421055432
K/NSTOP: 0.196073
AB/A: 0.19682547697339245

With 5 servers:
    K/NSTOP     AB/A                    B(s,a)              seed
1   0.54646     0.5427016232534375      0.5490691303        1000000 customers: 
2   0.54787     0.5483069979000874      0.5490691303        1000000 customers: 
3   0.52211     0.6831328673685755      NA                  1000000 customers: 
4   0.5         0.7999760000006664      NA

With 15 servers:
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.03028     0.029930756674027465    0.029131042132999503    1000000 customers: 
2   0.02895     0.02876110342757019     0.029131042132999503    1000000 customers: 
3   0.00364     0.009507612733107598    NA                      1000000 customers: 
4   0.0         0.0                     NA

With 12 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.10521     0.10502751194863676     0.10464675636104714     1000000 customers: 
2   0.10413     0.1047871154377325      0.10464675636104714     1000000 customers: 
3   0.04959     0.09872615875458929     NA                      1000000 customers: 
4   0.0         0.0                     NA


With 10 servers but average arrival time of 4.2 (a = 4.2 * 2.4 = 10.08 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.21954     0.2190467385903617      0.2182604405754659      1000000 customers: 
2   0.21728     0.21716910181209256     0.2182604405754659      1000000 customers: 
3   0.1371      0.24242003733822218     NA                      1000000 customers: 
4   0.0         0.5999460000013329      NA

With 10 servers but average arrival time of 4.0 (a = 4.0 * 3.0 = 12.00 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.30204     0.30151788513648076     0.30192504028637934     1000000 customers: 
2   0.30082     0.29868468826174777     0.30192504028637934     1000000 customers: 
3   0.25791     0.40252202530786235     NA                      1000000 customers: 
4   0.16666     0.99991                 NA

With 7 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.38846     0.388308723940042       0.3907517006187665      1000000 customers: 
2   0.38965     0.3881772380223471      0.3907517006187665      1000000 customers: 
3   0.3485      0.5116404326820196      NA                      1000000 customers: 
4   0.3         0.719964000000933       NA

With 4 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.6347      0.6336504970758445      0.6341848042687279      1000000 customers: 
2   0.6331      0.6333377199598874      0.6341848042687279      1000000 customers: 
3   0.6149      0.7611168411525843      NA                      1000000 customers: 
4   0.6         0.8399820000005331      NA

With 3 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.72428     0.7240327136973354      0.7223419680996982      1000000 customers: 
2   0.72144     0.721574368910532       0.7223419680996982      1000000 customers: 
3   0.70917     0.830946485141977       NA                      1000000 customers: 
4   0.7         0.8799880000003998      NA

With 2 servers, average arrival time of 4.0 (a = 4.0 * 2.4 = 9.6 erlangs):
    K/NSTOP     AB/A                    B(s,a)                  seed
1   0.81358     0.8139251506131809      0.812985179957657       1000000 customers: 
2   0.81218     0.8135479961593075      0.812985179957657       1000000 customers: 
3   0.80481     0.8937422891434076      NA                      1000000 customers: 
4   0.8         0.9199940000002665      NA

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