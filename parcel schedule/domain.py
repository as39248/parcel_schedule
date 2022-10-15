"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """parcels to be delivered"""
    parcel_id: int
    volume: int
    city1: str
    city2: str

    def __init__(self, parcel_id: int, volume: int,
                 city1: str, city2: str) -> None:
        """parcel information"""
        self.parcel_id = parcel_id
        self.volume = volume
        self.city1 = city1
        self.city2 = city2


class Truck:
    """Trucks to deliver parcels to destination"""
    truck_id: int
    max_capacity: int
    city: str
    dic: Dict

    def __init__(self, truck_id: int, max_capacity: int, city: str) -> None:
        """create dictionary with truck info parcel info that the truck is
        delivering"""
        self.truck_id = truck_id
        self.max_capacity = max_capacity
        self.city = city
        self.dic = {}

    def pack(self, p: Parcel) -> bool:
        """put the parcel in the truck"""
        info = (self.truck_id, self.max_capacity, self.city)
        parcel = [p.parcel_id, p.volume, p.city1, p.city2]
        if info not in self.dic:
            self.dic[info] = [parcel]
        else:
            self.dic[info].append(parcel)
        return parcel in self.dic[info]

    def fullness(self) -> float:
        """return the percentage of how full the truck is"""
        total_volume = 0
        info = (self.truck_id, self.max_capacity, self.city)
        if self.dic == {}:
            percentage = 0
        else:
            for i in self.dic[info]:
                total_volume += i[1]
            percentage = total_volume / self.max_capacity * 100
        return percentage


# Helper functions for class Fleet

def parcel_allocation_helper(t: Truck, dictionary: Dict, x: Dict) -> None:
    """helper function for parcel_allocation"""
    for lst in t.dic[x]:
        if t.truck_id not in dictionary:
            dictionary[t.truck_id] = [lst[0]]
        else:
            dictionary[t.truck_id].append(lst[0])


def distance_travelled_helper(d_map: DistanceMap, lst1: list, n: int,
                              a: list) -> None:
    """helper function for distance_travelled function"""
    for k in d_map.dictionary:
        if (lst1[2], lst1[3]) in d_map.dictionary:
            n += sum(d_map.dictionary[k])
    a.append(n)


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        n = 0
        for i in self.trucks:
            if i.fullness() > 0:
                n += 1
        return n

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        dic = {}
        for i in self.trucks:
            for info in i.dic:
                parcel_allocation_helper(i, dic, info)
        return dic

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """

        n = 0
        for i in self.trucks:
            for info in i.dic:
                for lst in i.dic[info]:
                    n = i.max_capacity - lst[1]
        return n

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        n = 0
        for i in self.trucks:
            n = i.fullness()
        return n

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        n = 0
        x = 1
        for i in self.trucks:
            n += i.fullness()
        if len(self.trucks) != 0:
            x = len(self.trucks)
        else:
            pass
        return n / x

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        a = []
        d = 0
        for i in self.trucks:
            for info in i.dic:
                for lst in i.dic[info]:
                    distance_travelled_helper(dmap, lst, d, a)
        return sum(a)

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        a = []
        d = 0
        n = 1
        for i in self.trucks:
            for info in i.dic:
                for lst in i.dic[info]:
                    distance_travelled_helper(dmap, lst, d, a)

        if len(self.trucks) != 0:
            n = len(self.trucks)
        else:
            pass
        return sum(a) / n


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
