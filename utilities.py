import random
import numpy
from itertools import islice


def one_hot_encode(enum_value):
    enum_members = list(enum_value.__class__)
    one_hot = [0] * len(enum_members)
    index = enum_members.index(enum_value)
    one_hot[index] = 1
    return one_hot


def one_hot_decode(enum_class, one_hot_iterator):
    enum_members = list(enum_class)
    one_hot_list = [next(one_hot_iterator) for _ in range(len(enum_members))]
    index = one_hot_list.index(1)
    return enum_members[index]


def random_sum(size):
    array = numpy.random.dirichlet(numpy.ones(size))
    scale_factor = numpy.random.rand()
    array *= scale_factor
    return array.tolist()


def partition_iterator(iterator, size):
    return islice(iterator, size)


def transpose(matrix):
    return list(zip(*matrix))
