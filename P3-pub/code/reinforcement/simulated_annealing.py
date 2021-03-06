import numpy as np
import random
import math


# number of items
N = 100

# weight limit
W = 3000

# weights of items
w = np.array([430, 763, 965, 848, 481, 336, 346, 381, 252, 218, 234, 906, 398,
              749, 343, 281, 773, 589, 896, 342, 640, 935, 876, 456, 629, 296,
              515, 946, 843, 554, 655, 906, 528, 273, 477, 347, 495, 294, 638,
              552, 607, 815, 394, 608, 694, 905, 826, 528, 739, 628, 810, 709,
              822, 296, 657, 654, 653, 892, 410, 812, 780, 469, 837, 450, 417,
              688, 308, 345, 616, 904, 827, 453, 690, 782, 626, 752, 994, 236,
              924, 303, 881, 617, 241, 559, 337, 930, 352, 922, 377, 865, 825,
              536, 499, 729, 359, 897, 959, 293, 658, 983])

# values of items
v = np.array([25, 27, 15, 25, 13, 15, 18, 24, 25, 30, 12, 18, 28, 30, 20, 26,
              24, 30, 14, 20, 15, 30, 18, 26, 16, 24, 11, 16, 14, 13, 13, 14,
              30, 12, 21, 13, 12, 28, 22, 14, 10, 20, 28, 19, 30, 16, 12, 24,
              28, 27, 29, 18, 16, 27, 30, 29, 17, 19, 26, 12, 24, 15, 27, 16,
              15, 15, 19, 14, 22, 30, 19, 30, 19, 24, 27, 16, 12, 27, 24, 17,
              12, 18, 11, 14, 25, 13, 23, 11, 26, 22, 12, 13, 15, 20, 20, 24,
              12, 10, 14, 13])


def neighbor_bag(bag):
    """
    Return a "neighbor" of the current bag.
    """

    next_bag = list(bag)
    weight = 0
    for i in next_bag:
        weight+=w[i]
    for i in range(2):
        x = random.randint(0,N-1)
        while x in next_bag:
            x = random.randint(0,N-1)
        next_bag.append(x)
        weight+= w[x]
    #print(next_bag)
    while weight >W:
        a =random.randrange(len(next_bag))
        weight-=w[next_bag[a]]
        next_bag.pop(a)
        '''
        x = random.randint(0,N-1)
        while x in next_bag:
            x = random.randint(0,N-1)
        next_bag.append(x)
        weight+= w[x]
        '''
        #print(next_bag)
        #print("aa")
        #print(next_bag)
        #print("bb")
    #print(next_bag)
    return next_bag  # TODO


def accept_bag(new_val, old_val, T):
    """
    Return True if we should accept the new bag.  False otherwise.

    You may use any acceptance probability metric you chose, but we
    suggest accepting with probabilities:
    1                            -->  if new_val > old_val
    exp((new_val - old_val) / T) -->  if old_val >= new_val
    """
    if new_val>old_val:
        #print("true")
        return True
    else:
        #print(np.exp((new_val - old_val) / T) > 0.5)
        return math.exp((new_val - old_val) / T) > 0.5



def simulated_annealing():
    """
    Simulated Annealing Algorithm

    Return list of bag values while annealing and final bag: (vals, bag)

    NOTE: Make sure that your algorithm ends up beating the greedy algorithm!
    We will give full credit for any solution that beats the greedy algorithm
    consistently.
    """
    TRIALS = 10000
    T = 1000.0
    DECAY = 0.98

    vals = []
    sim_val = 0
    sim_bag = []

    for trial in range(TRIALS):
        
        # Pick a random neighbor
        next_bag = neighbor_bag(sim_bag)
        next_val = sum([v[i] for i in next_bag])
        #print("aaa")
        # print(next_bag)
        # Accept with some probability
        if accept_bag(next_val, sim_val, T):
            sim_val = next_val
            sim_bag = next_bag
        #print("bbb")
        # Update temperature
        T *= DECAY

        # Update vals
        vals += [sim_val]

    return np.array(vals), sim_bag


def greedy():
    """
    Greedy Algorithm -- maximuze v/w
    """
    vw_ratio = sorted(map(
        lambda x: (x, 1.*v[x]/w[x]), range(N)), key=lambda x: -x[1])
    greedy_val = 0
    greedy_weight = 0
    greedy_bag = []
    index = 0
    while greedy_weight + w[vw_ratio[index][0]] < W:
        greedy_val += v[vw_ratio[index][0]]
        greedy_weight += w[vw_ratio[index][0]]
        greedy_bag += [vw_ratio[index][0]]
        index += 1

    return greedy_val, greedy_weight, greedy_bag


if __name__ == "__main__":

    greedy_val, greedy_weight, greedy_bag = greedy()
    print("Greedy Algorithm:\nValue:{}, Weight:{}\nBag:{}".format(greedy_val,
          greedy_weight, greedy_bag))

    SA_trace, sim_bag = simulated_annealing()
    sim_val = sum([v[i] for i in sim_bag])
    sim_weight = sum([w[i] for i in sim_bag])
    print("Simulated Algorithm:\nValue:{}, Weight:{}\nBag:{}".format(sim_val,
          sim_weight, sim_bag))

    import matplotlib.pyplot as plt
    plt.plot([greedy_val]*len(SA_trace), label="Greedy")
    
    plt.plot(SA_trace, label="SA")

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)

    plt.show()