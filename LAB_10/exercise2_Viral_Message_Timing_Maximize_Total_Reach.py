import random
import time

cost = []
reach = []

N = 500

for n in range(N):
    cost.append(random.randint(1000, 10000))
    reach.append(random.randint(1, 100000))

def maximize_reach(budget, costs, influences):
    N = len(costs)
    path = [[] for _ in range(budget+1)]
    path_past = path.copy()
    mat = [[0 for _ in range(budget+1)] for _ in range(N+1)]
    for i in range(N):
        for w in range(budget+1):
            if w >= costs[i]:
                if mat[i][w] < mat[i][w - costs[i]] + influences[i]:
                    mat[i+1][w] = mat[i][w - costs[i]] + influences[i]
                    path[w] = path_past[w - costs[i]] + [i]
                else:
                    mat[i+1][w] = mat[i][w]
            else:
                mat[i+1][w] = mat[i][w]
        path_past = path.copy()
    maximum = 0
    final_path = []
    for m in range(len(mat[-1])):
        if mat[-1][m] > maximum:
            maximum = mat[-1][m]
            final_path = path[m]
    return maximum, final_path, sum(costs[u] for u in final_path)

def is_within_budget(budget, users, costs):
    return sum(costs[u] for u in users) <= budget

def sort_by_efficiency(budget, costs, influences):
    done = []
    result = []
    N = len(costs)-1
    for i in range(N):
        best = 0
        best_index = 0
        for n in range(N):
            if n not in done:
                if influences[n]/costs[n] > best:
                    best = influences[n]/costs[n]
                    best_index = n
                    done.append(n)
        result.append((costs[best_index], influences[best_index], best_index))
    return result

def sort_better(costs, influences, indexes = None):
    if indexes is None:
        indexes = [[i] for i in range(len(influences))]
    pivot = influences[0]/costs[0]
    smaller = []
    bigger = []

def fast_alternative_strategy(budget, costs, influences):
    tw = 0
    sort = sort_by_efficiency(budget,costs, influences)
    result = []
    for i in range(len(costs)):
        if tw > budget:
            break
        result.append(sort[i][2])
        tw += sort[i][0]
    return result[:-1], tw - sort[i-1][0], sum(influences[n] for n in result[:-1])

budget = 10000

print("Here are the different algorithm's result for a budget of: ", budget, " and total number of ", N, " server to choose from")

start_time = time.time()
DP = maximize_reach(budget, cost, reach)
end = ((time.time() - start_time)// 0.0001)/10000
print("The dynamic programming solution is: ", DP[0], "reach for these server selected: ", DP[1] , ", for a total cost of:",DP[2] , "this solution took: ", end, "seconds")

print("is the DP solution is within budget: ", is_within_budget(budget, DP[1], cost))

start_time = time.time()
Greedy = fast_alternative_strategy(budget, cost, reach)
end = ((time.time() - start_time)// 0.0001)/10000

print("The greedy solution is: ", Greedy[2], " reach for these server selected: ", Greedy[0], ", for a total of: ", Greedy[1] ,"this solution took: ", end, "seconds")

print("is the greedy solution is within budget: ", is_within_budget(budget, Greedy[0], cost))
