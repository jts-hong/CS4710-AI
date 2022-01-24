"""
Q-learning Functions
"""

import sys
import numpy as np
import pandas as pd

def pick_strategies(game, s, t):
    """
    Pick strategies by exploration vs exploitation
    """
    a = np.zeros(game.n).astype(int)
    pr_explore = np.exp(- t * game.beta)
    e = (pr_explore > np.random.rand(game.n))
    for n in range(game.n):
        if e[n]:
            a[n] = np.random.randint(0, game.k)
        else:
            a[n] = np.argmax(game.Q[(n,) + tuple(s)])
    return a


def update_q(game, s, a, s1, pi, stable):
    """
    Update Q matrix
    """
    for n in range(game.n):
        subj_state = (n,) + tuple(s) + (a[n],)
        old_value = game.Q[subj_state]
        max_q1 = np.max(game.Q[(n,) + tuple(s1)])
        new_value = pi[n] + game.delta * max_q1
        old_argmax = np.argmax(game.Q[(n,) + tuple(s)])
        game.Q[subj_state] = (1 - game.alpha) * old_value + game.alpha * new_value
        # Check stability
        new_argmax = np.argmax(game.Q[(n,) + tuple(s)])
        same_argmax = (old_argmax == new_argmax)
        stable = (stable + same_argmax) * same_argmax
    return game.Q, stable


def check_convergence(game, t, stable):
    """
    Check if game converged
    """
    if (t % game.tstable == 0) & (t > 0):
        sys.stdout.write("\rt=%i" % t)
        sys.stdout.flush()

        #print(game.PI)
    if stable > game.tstable:
        print('Converged!')
        return True
    if t == game.tmax:
        print('ERROR! Not Converged!')
        return True
    return False


def simulate_game(game):
    """
    Simulate game
    """
    s = game.s0
    stable = 0
    data={}
    columns=('A_Price','B_Price','A_PI','B_PI','CONS_1','CONS_2')
    # Iterate until convergence
    for t in range(int(game.tmax)):
        a = pick_strategies(game, s, t)
        pi = game.PI[tuple(a)]
        s1 = a
        game.Q, stable = update_q(game, s, a, s1, pi, stable)
        s = s1
        if t%1000==0:
            data[t]={'A_Price':game.init_actions()[a[0]],'B_Price':\
                game.init_actions()[a[1]],'A_PI':pi[0],'B_PI':pi[1],\
                    'CONS_1':game.compute_p_competitive_monopoly()[0][0],\
                        'CONS_2':game.compute_p_competitive_monopoly()[1][0]}
        if check_convergence(game, t, stable):
            df = pd.DataFrame(data=data, index=columns).T
            df.to_csv('data_Final.csv')
            df.plot()
            break
    return game 