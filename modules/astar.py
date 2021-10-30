# -*- coding: utf-8 -*-
"""
This file contains the A* algorithm in use for the pathfinding module. The code is a modified version from
https://github.com/jrialland/python-astar
"""

from abc import abstractmethod
from heapq import heappush, heappop

Infinite = float('inf')


class AStar:
    class SearchNode:
        __slots__ = ('data', 'gscore', 'fscore',
                     'closed', 'came_from', 'out_openset')

        def __init__(self, data, gscore=Infinite, fscore=Infinite):
            self.data = data
            self.gscore = gscore
            self.fscore = fscore
            self.closed = False
            self.out_openset = True
            self.came_from = None

        def __lt__(self, b):
            return self.fscore < b.fscore

        def __str__(self):
            return f"{self.data=}"

        def __repr__(self):
            return f"{self.data=}"

    @abstractmethod
    def heuristic_cost_estimate(self, current, goal):
        """Computes the estimated (rough) distance between a node and the goal. The second parameter is always the
        goal."""
        raise NotImplementedError

    @abstractmethod
    def distance_between(self, n1, n2):
        """Gives the real distance between two adjacent nodes n1 and n2 (i.e n2 belongs to the list of n1's neighbors).
           n2 is guaranteed to belong to the list returned by the call to neighbors(n1)."""
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node):
        """For a given node, returns (or yields) the list of its neighbors"""
        raise NotImplementedError

    def is_goal_reached(self, current, goal):
        """ returns true when we can consider that 'current' is the goal"""
        return current == goal

    def reconstruct_path(self, last, reversePath=False):
        """Reconstructs the found path as a list."""
        def _gen():
            current = last
            while current:
                yield current.data
                current = current.came_from

        if reversePath:
            return _gen()
        else:
            return list(reversed(list(_gen())))

    def astar(self, start, goal, reversePath=False):
        """Find a path"""
        if self.is_goal_reached(start, goal):
            return [start]
        search_nodes = {}
        start_node = search_nodes[start['i']] = AStar.SearchNode(
            start, gscore=.0, fscore=self.heuristic_cost_estimate(start, goal))
        open_set = []
        heappush(open_set, start_node)
        while open_set:
            current = heappop(open_set)
            print(f"openSet length={len([n for n in open_set])}, searchNodes length={len(search_nodes)}, {current=}")
            if self.is_goal_reached(current.data, goal):
                return self.reconstruct_path(current, reversePath)
            current.out_openset = True
            current.closed = True
            for neighbor in self.neighbors(current.data):
                neighbour_node = search_nodes.setdefault(neighbor['i'], AStar.SearchNode(neighbor))
                if neighbour_node.closed:
                    continue
                tentative_gscore = current.gscore + self.distance_between(current.data, neighbour_node.data)
                if tentative_gscore >= neighbour_node.gscore:
                    continue
                neighbour_node.came_from = current
                neighbour_node.gscore = tentative_gscore
                neighbour_node.fscore = tentative_gscore + self.heuristic_cost_estimate(neighbour_node.data, goal)
                if neighbour_node.out_openset:
                    neighbour_node.out_openset = False
                    heappush(open_set, neighbour_node)
                else:
                    # re-add the node in order to re-sort the heap
                    open_set.remove(neighbour_node)
                    heappush(open_set, neighbour_node)
        return []


def find_path(start, goal, neighbors_fnct, reversePath=False, heuristic_cost_estimate_fnct=lambda a, b: Infinite,
              distance_between_fnct=lambda a, b: 1.0, is_goal_reached_fnct=lambda a, b: a == b):
    """A non-class version of the path finding algorithm"""

    class FindPath(AStar):

        def heuristic_cost_estimate(self, current, goal):
            return heuristic_cost_estimate_fnct(current, goal)

        def distance_between(self, n1, n2):
            return distance_between_fnct(n1, n2)

        def neighbors(self, node):
            return neighbors_fnct(node)

        def is_goal_reached(self, current, goal):
            return is_goal_reached_fnct(current, goal)

    return FindPath().astar(start, goal, reversePath)
