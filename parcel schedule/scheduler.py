"""Assignment 1 - Scheduling algorithms (Task 4)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """A Random scheduler, capable of deciding what parcels go onto which
    trucks, and what route each truck will take. """
    unscheduled: List

    def __init__(self) -> None:

        self.unscheduled = []

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:

        shuffle(parcels)
        for p in parcels:
            lst = []
            for t in trucks:
                if p.volume <= t.max_capacity - \
                        (t.fullness() / 100 * t.max_capacity):
                    lst.append(t)
            if len(lst) != 0:
                choice(lst).pack(p)
            else:
                self.unscheduled.append(p)
        return self.unscheduled


class GreedyScheduler(Scheduler):
    """A Greedy scheduler, capable of deciding what parcels go onto which
    trucks, andwhat route each truck will take."""
    unscheduled: List

    def __init__(self) -> None:

        self.unscheduled = []

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        truck = Truck
        for p in parcels:
            for t in trucks:
                if p.city2 != truck.city and \
                        p.volume <= t.max_capacity - \
                        (t.fullness() / 100 * t.max_capacity):
                    truck = PriorityQueue(empty_truck)
                    truck.add(t)
                elif p.city2 == truck.city and \
                        p.volume <= t.max_capacity - \
                        (t.fullness() / 100 * t.max_capacity):
                    truck = PriorityQueue(truck_with_parcel)
                    truck.add(t)
                else:
                    self.unscheduled.append(p)
            truck.queue[0].pack(p)
        return self.unscheduled


def empty_truck(t1: Truck, t2: Truck) -> bool:
    """helper function to set the priority for GreedyScheduler"""
    return (t1.max_capacity - (t1.fullness() / 100 * t1.max_capacity)) > \
           (t2.max_capacity - (t2.fullness() / 100 * t2.max_capacity))


def truck_with_parcel(t1: Truck, t2: Truck, p: Parcel) -> bool:
    """helper function to set the priority for GreedyScheduler"""
    return (t1.max_capacity - (t1.fullness() / 100 * t1.max_capacity)) > \
           (t2.max_capacity
            - (t2.fullness() / 100 * t2.max_capacity)) and t1.city == p.city2


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
