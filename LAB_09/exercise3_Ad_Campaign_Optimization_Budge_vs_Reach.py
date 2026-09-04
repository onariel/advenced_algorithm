import random
import time
from unittest import result

costs = [19, 91, 16, 84, 56, 15, 84, 34, 62, 30, 17, 24, 27, 49, 7, 85, 53, 91, 47, 67, 48, 99, 83, 30, 18, 56, 37, 47, 82, 14, 74, 77, 2, 42, 66, 2, 50, 41, 41, 15, 26, 28, 91, 1, 25, 71, 76, 28, 36, 23, 3, 98, 12, 98, 90, 9, 47, 68, 37, 90, 41, 34, 93, 56, 32, 2, 95, 99, 88, 55, 28, 22, 17, 9, 25, 43, 47, 84, 48, 94, 62, 68, 92, 8, 7, 83, 82, 98, 38, 37, 86, 40, 7, 89, 60, 95, 84, 35, 77, 30, 80, 17, 60, 42, 100, 77, 11, 80, 77, 76, 41, 74, 82, 55, 98, 43, 16, 35, 2, 69, 4, 86, 11, 62, 31, 87, 26, 26, 60, 78, 24, 51, 54, 65, 87, 21, 63, 7, 85, 2, 47, 83, 71, 1, 35, 73, 29, 20, 47, 87, 83, 89, 27, 84, 75, 17, 10, 96, 61, 30, 46, 21, 35, 20, 5, 55, 64, 11, 66, 84, 89, 84, 49, 2, 45, 9, 46, 36, 78, 32, 46, 55, 17, 3, 11, 85, 42, 59, 45, 39, 60, 59, 67, 58, 24, 9, 42, 85, 5, 41, 59, 65, 12, 87, 66, 2, 41, 75, 55, 75, 89, 43, 8, 96, 94, 10, 5, 51, 11, 60, 32, 66, 84, 70, 21, 39, 58, 33, 86, 43, 46, 81, 43, 67, 24, 18, 33, 45, 49, 87, 44, 3, 20, 61, 79, 57, 87, 26, 29, 5, 75, 34, 92, 70, 51, 64, 35, 13, 45, 15, 99, 46, 34, 81, 51, 53, 12, 70, 67, 7, 4, 19, 53, 82, 56, 33, 10, 89, 2, 96, 30, 24, 40, 23, 86, 21, 21, 64, 81, 73, 61, 55, 85, 88, 46, 58, 84, 20, 31, 34, 26, 94, 70, 30, 64, 63, 36, 85, 27, 6, 17, 14, 94, 19, 73, 32, 43, 41, 20, 35, 17, 33, 22, 58, 11, 14, 52, 3, 66, 49, 78, 99, 5, 33, 43, 41, 82, 39, 37, 82, 46, 6, 5, 2, 64, 83, 45, 80, 13, 3, 72, 53, 54, 53, 61, 5, 71, 63, 84, 88, 78, 43, 7, 35, 39, 27, 22, 8, 93, 56, 7, 89, 76, 78, 62, 71, 9, 49, 34, 89, 9, 15, 100, 59, 17, 14, 26, 3, 75, 41, 11, 96, 61, 83, 8, 23, 54, 88, 64, 94, 70, 50, 84, 9, 87, 46, 39, 53, 56, 99, 92, 75, 10, 6, 22, 33, 55, 43, 54, 15, 8, 54, 68, 42, 79, 22, 59, 51, 65, 100, 85, 61, 62, 27, 81, 38, 84, 7, 84, 4, 85, 57, 45, 2, 52, 64, 2, 85, 35, 94, 35, 93, 39, 52, 49, 42, 75, 48, 49, 18, 31, 72, 84, 17, 40, 75, 62, 9, 93, 55, 35, 79, 80, 33, 19, 25, 89, 67, 64, 39, 76, 23, 80, 64, 18, 61, 7, 51, 44, 91, 59, 41, 91, 39, 74, 48, 49, 21, 4, 99]
influences = [14, 75, 56, 43, 28, 73, 70, 80, 53, 16, 93, 46, 100, 57, 3, 36, 90, 10, 35, 58, 99, 81, 29, 68, 67, 82, 88, 35, 70, 84, 25, 86, 58, 2, 73, 79, 1, 73, 63, 70, 17, 34, 37, 16, 46, 19, 27, 47, 14, 93, 49, 16, 29, 14, 87, 69, 67, 45, 97, 70, 45, 62, 10, 94, 88, 48, 45, 37, 75, 38, 96, 47, 99, 48, 66, 64, 24, 41, 65, 6, 85, 63, 86, 50, 76, 98, 76, 86, 84, 9, 12, 90, 97, 100, 8, 73, 37, 15, 76, 10, 53, 38, 55, 65, 48, 17, 77, 82, 29, 29, 65, 50, 82, 46, 75, 85, 31, 18, 84, 11, 18, 95, 100, 55, 99, 36, 62, 63, 1, 16, 45, 24, 37, 34, 57, 75, 52, 40, 45, 90, 41, 3, 18, 60, 22, 20, 44, 27, 70, 38, 26, 32, 43, 13, 38, 6, 9, 28, 98, 61, 93, 12, 85, 30, 37, 51, 91, 13, 66, 41, 23, 89, 80, 27, 67, 51, 99, 35, 43, 94, 1, 85, 90, 78, 79, 26, 94, 49, 18, 92, 69, 37, 86, 97, 80, 39, 47, 83, 8, 11, 44, 72, 68, 67, 36, 11, 15, 66, 68, 43, 10, 86, 73, 24, 28, 80, 10, 94, 55, 37, 61, 87, 57, 76, 57, 7, 77, 91, 74, 15, 3, 79, 27, 24, 50, 62, 100, 25, 75, 5, 74, 58, 95, 36, 77, 88, 21, 100, 79, 31, 79, 54, 44, 4, 64, 99, 95, 31, 51, 63, 11, 90, 76, 70, 85, 75, 51, 25, 74, 18, 9, 7, 71, 77, 29, 82, 42, 42, 1, 51, 66, 8, 94, 80, 41, 90, 57, 51, 1, 9, 68, 75, 12, 2, 12, 9, 98, 69, 25, 92, 85, 80, 14, 77, 99, 83, 34, 71, 94, 36, 52, 34, 12, 85, 52, 36, 86, 70, 17, 88, 21, 83, 81, 72, 49, 6, 78, 84, 62, 79, 83, 65, 36, 92, 59, 26, 99, 78, 15, 12, 32, 22, 25, 100, 51, 30, 32, 15, 55, 77, 93, 6, 70, 77, 20, 50, 85, 47, 76, 46, 15, 60, 12, 22, 45, 40, 34, 31, 32, 32, 1, 83, 76, 29, 3, 31, 92, 33, 69, 85, 50, 24, 17, 74, 8, 49, 100, 87, 100, 91, 35, 78, 2, 83, 71, 91, 32, 81, 49, 75, 88, 10, 74, 37, 74, 17, 44, 21, 83, 93, 84, 50, 80, 73, 59, 70, 31, 94, 42, 38, 60, 59, 15, 5, 49, 71, 65, 45, 13, 82, 99, 52, 27, 68, 30, 2, 86, 29, 54, 82, 38, 38, 97, 90, 39, 63, 88, 64, 63, 57, 76, 47, 36, 62, 21, 44, 60, 6, 47, 20, 29, 45, 45, 14, 28, 45, 52, 15, 65, 4, 79, 68, 38, 51, 85, 77, 96, 58, 70, 48, 22, 77, 9, 85, 75, 33, 67, 71, 25, 50, 58, 22, 39, 33, 70, 83, 71, 16, 47, 67]

test_cost = []
test_influences = []
N = 500

for n in range(N):
    test_cost.append(random.randint(1000, 10000))
    test_influences.append(random.randint(1, 100000))


def maximize_reach_slow(budget, costs, influences):
    print("budget: ",budget, "costs: ", costs, "influences:", influences)
    opts = [[]]
    maxvalue = [0]
    N = len(costs)-1
    def test(budget, costs, influences, index, tw, av, S=[]):
        if tw + costs[index] < budget:
            S1 = S + [index]
            if index < N:
                tw1 = tw + costs[index]
                test(budget, costs, influences,index+1, tw1, av, S=S1)
            elif av > maxvalue[0]:
                maxvalue[0] = av
                opts[0] = S1
        av1 = av - influences[index]
        if av1 > maxvalue[0]:
            if index < N:
                test(budget, costs, influences,index+1, tw, av1, S=S)
            else:
                maxvalue[0] = av1
                opts[0] = S
    test(budget, costs, influences,0, 0, sum(influences))
    total_cost = [costs[w] for w in opts[0]]
    return f"the selected influencer: {opts[0]}, for a total of {maxvalue[0]} follower and total of {sum(total_cost)} of cost"


def maximize_reach(budget, costs, influences):
    print("budget: ",budget, "costs: ", costs, "influences:", influences)
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
    return maximum, final_path

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

start = time.time()
reach = maximize_reach(budget, test_cost, test_influences)
end = time.time() - start
print("knabsack problem with dynamic programming:")
print("influence maximum:", reach[0], "with these influencers:", reach[1], "with", N ," influencers and a budget of 10000, with a time of: ", end, "seconds")
start = time.time()
fast = fast_alternative_strategy(budget, test_cost, test_influences)
end = time.time() - start
print("knabsack problem with greedy programming:")
print("selected user: ",fast[0], "for a total of ", fast[2], "influences and ", fast[1], "cost, with a time of:", end, "seconds")

