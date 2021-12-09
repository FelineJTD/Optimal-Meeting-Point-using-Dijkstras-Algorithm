#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Felicia Sutandijo
# @Date   : 2021-12-09

'''
This python code determines the optimal meeting point of a group of connected people represented by a weighted graph
'''

from OptimalMeetingPoint import printRoutes, readVertices, completeDijkstra, minTotalCost, minMaxCost, printRoutes
import sys

file_name = sys.argv[1]

vertices, unreachables, count = readVertices(file_name)
if (len(unreachables) > 1): # there are more than one place that only has inbound edges
  print("There is no suitable meeting point.")
else:
  if (len(unreachables) == 1): # there is one place that only has inbound edges, meaning the suitable meeting point is there
    # use the unreachable vertex as a starting point
    start_vertex = unreachables[0]
  else: # no constraints, everyone can travel
    # use the first vertex as a starting point
    start_vertex = next(iter(vertices))
  cheapest, prev_vertex = completeDijkstra(vertices, start_vertex)

  # minimizing cost method
  try:
    method = int(sys.argv[2])
  except:
    print("Which method would you like to use to determine the most suitable meeting point?")
    print("1. Minimize the total cost (= minimize the average cost) of travel")
    print("2. Minimize the maximum individual cost of travel")
    print("3. Both")
    method = int(input("> "))

  # output
  if (method == 1 or method == 3):
    print("\n----- MINIMIZING TOTAL COST -----")
    place, min = minTotalCost(cheapest, count)
    print(f"The most suitable meeting point is {place} with the total cost of {min}.")
    printRoutes(vertices, prev_vertex, place)
  if (method == 2 or method == 3):
    print("\n----- MINIMIZING MAXIMUM COST -----")
    place, min = minMaxCost(cheapest, count)
    print(f"The most suitable meeting point is {place} with the maximum cost of {min}.")
    printRoutes(vertices, prev_vertex, place)