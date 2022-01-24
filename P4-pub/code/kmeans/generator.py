#!/usr/bin/env python

import copy
import matplotlib.pyplot as plt
import numpy as np


def generate_points():
    """ Generates points according to Normal dists"""
    mu1 = [5., 2.]
    p1 = np.random.normal(mu1, 0.9, size=(10, 2))

    mu2 = [9., 4.]
    p2 = np.random.normal(mu2, 1.2, size=(10, 2))

    mu3 = [0., 2.]
    p3 = np.random.normal(mu3, 1.0, size=(10, 2))

    mu4 = [3., 6.]
    p4 = np.random.normal(mu4, 1.2, size=(10, 2))

    mu5 = [7., 6.]
    p5 = np.random.normal(mu5, 0.75, size=(10, 2))

    plt.plot(list(zip(*p1))[0], list(zip(*p1))[1], 'o')
    plt.plot(list(zip(*p2))[0], list(zip(*p2))[1], 'o')
    plt.plot(list(zip(*p3))[0], list(zip(*p3))[1], 'o')
    plt.plot(list(zip(*p4))[0], list(zip(*p4))[1], 'o')
    plt.plot(list(zip(*p5))[0], list(zip(*p5))[1], 'o')
    plt.show()

    points = np.concatenate((p1, p2, p3, p4, p5))
    np.save('new.npy', points)


if __name__ == '__main__':
    generate_points()
