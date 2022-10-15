"""Assignment 1 - Distance map (Task 1)

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

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """Stores and looks up the distance between any two cities"""
    dictionary: Dict

    def __init__(self) -> None:
        """Create dictionary of distances between two cities.
        >>> m = DistanceMap()
        >>> m.dictionary
        {}
        """
        self.dictionary = {}

    def distance(self, c1: str, c2: str) -> int:
        """Return the distance from the first city to the second, or -1 if the
         distance is no stored in the distance map.
         >>> m = DistanceMap()
         >>> m.add_distance('Montreal', 'Toronto', 4)
         >>> m.distance('Montreal', 'Toronto')
         4
         """

        result = -1
        if (c1, c2) in self.dictionary.keys():
            result = self.dictionary[c1, c2][0]
        return result

    def add_distance(self, c1: str, c2: str, distance1: int,
                     distance2: int = -1) -> None:
        """Add the distance between two cities into the dictionary
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m.dictionary
        {('Toronto', 'Hamilton'): [9, 9]}
        """
        if distance2 == -1:
            distance2 = distance1
        self.dictionary[c1, c2] = [distance1]
        self.dictionary[c1, c2].append(distance2)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
