#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Felicia Sutandijo
# @Date   : 2021-12-09

'''
This python code contains the functions needed to determine
the optimal meeting point of a group of connected people
represented by a weighted graph
'''
from PriorityQueue import PriorityQueue

def readVertices(filename):
  # a function that reads a file named filename (string) containing vertices data and returns
  # 1. vertices: dictionary of dictionary
  # 2. unreachables: array
  # 3. count: integer

  '''
  Accepted file format:
  
  # comments
  vertex: adjacent vertex, weight; another adjacent vertex, weight
  another vertex: adjacent vertex, weight

  # spaces and newlines do not matter
  # just remember not to put a semicolon (;) after the last adjacent vertex of each vertex
  '''

  vertices = {} # a dictionary of all the vertices and their corresponding dictionary of edges
  unreachables = [] # an array of unreachable vertices
  count = 0 # count of vertices

  # open file
  with open(filename, "r") as f:
    data = f.read()

  # clean file
  data = data.replace(" ", "")
  data = data.split("\n")
  
  # iteration
  for i in range(len(data)):
    if (data[i] != "" and data[i][0] != "#"): # aka if the line contains data
      count += 1
      data[i] = data[i].split(":")
      name = data[i][0]
      # initiate dictionary of edges using vertex name as key
      vertices[name] = {}
      data[i][1] = data[i][1].split(";")
      # iteration to append edges data to dictionary
      for j in range (len(data[i][1])):
        data[i][1][j] = data[i][1][j].split(",")
        vertices[name][data[i][1][j][0]] = int(data[i][1][j][1])
  
  # check if there are any vertices which are unreachable
  for vertex in vertices.keys():
    found = False
    for edges in vertices.values():
      if vertex in edges:
        found = True
        break
    if not found:
      unreachables.append(vertex)    
  
  return (vertices, unreachables, count)
    

def completeDijkstra(vertices, start_vertex):
  # a function that requires a vertices (dictionary) and a start_vertex (string)
  # and returns cheapest_costs (dictionary) and previous_stopover_vertex (dictionary)
  # through complete Dijkstra method which calculates all cheapest routes
  # to every city from every city (or vice versa, depending on the vertices data)

  # variables to be returned
  cheapest_costs = {}
  previous_stopover_vertex = {}
  # variables to hold temporary states while Dijkstra runs
  unvisited_vertices = PriorityQueue() # a priority queue, to be used in initial loop
  revisit_vertices = [] # a queue, containing the same elements with the same order, to be used in secondary loop
  visited_vertices = {}

  # enqueue
  unvisited_vertices.insert(start_vertex)

  # initial loop
  while (not unvisited_vertices.isEmpty()):
    # initiation
    # dequeue
    curr_vertex = unvisited_vertices.delete()
    revisit_vertices.append(curr_vertex)

    cheapest_costs[curr_vertex] = {}
    previous_stopover_vertex[curr_vertex] = {}
    cheapest_costs[curr_vertex][curr_vertex] = 0
    visited_vertices[curr_vertex] = True

    for adj_vertex, price in vertices[curr_vertex].items(): # iterate each adj vertices
      # add vertex to queues if not yet visited
      if (adj_vertex not in visited_vertices):
        unvisited_vertices.insert(adj_vertex)

      for vv in visited_vertices.keys():
        try:
          # if there is a cheapest cost through curr_vertex
          price_through_current_vertex = cheapest_costs[vv][curr_vertex] + price
          try:
            # compare the prices if there is an existing one
            if(cheapest_costs[vv][adj_vertex] > price_through_current_vertex):
              cheapest_costs[vv][adj_vertex] = price_through_current_vertex
              previous_stopover_vertex[vv][adj_vertex] = curr_vertex
          except:
            # price not yet initialized
            cheapest_costs[vv][adj_vertex] = price_through_current_vertex
            previous_stopover_vertex[vv][adj_vertex] = curr_vertex
        except:
          pass
    
  # revisiting vertices
  # this secondary loop is important so that all vertices 'visits' all vertices, currently only the start_vertex has done so
  for p in range(len(revisit_vertices)):
    curr_vertex = revisit_vertices[p]
    for q in range(p+1,len(revisit_vertices)):
      vv = revisit_vertices[q]
      for adj_vertex, price in vertices[revisit_vertices[p]].items(): # iterate each adj vertices
        try:
          price_through_current_vertex = cheapest_costs[vv][curr_vertex] + price
          try:
            if(cheapest_costs[vv][adj_vertex] > price_through_current_vertex):
              cheapest_costs[vv][adj_vertex] = price_through_current_vertex
              previous_stopover_vertex[vv][adj_vertex] = curr_vertex
          except:
            cheapest_costs[vv][adj_vertex] = price_through_current_vertex
            previous_stopover_vertex[vv][adj_vertex] = curr_vertex
        except:
          pass

  return(cheapest_costs, previous_stopover_vertex)


def printRoutes(vertices, previous_stopover_vertex, destination):
  # a procedure to output all routes
  # from each vertex to the destination
  print("Here are everybody's routes:")
  for start_vertex in vertices.keys():
    curr_vertex = start_vertex
    cheapest_route = []
    while (curr_vertex != destination):
      cheapest_route.append(curr_vertex)
      curr_vertex = previous_stopover_vertex[destination][curr_vertex]
    cheapest_route.append(destination)
    print("•", end=" ")
    for i in range(len(cheapest_route)-1):
      print(f"{cheapest_route[i]} -> ", end="")
    print(cheapest_route[len(cheapest_route)-1])


def minTotalCost(cheapest_costs, vertex_count):
  # a function that accepts cheapest_costs (dictionary) and vertex_count (integer)
  # and returns the suitable meeting point place (string) and minimum TOTAL COST min (integer) spent accumulatively by everyone
  min = -1
  for vertex, costs_from_other_vertices in cheapest_costs.items(): # these are the possible meeting points
    total_cost = 0
    # check if everyone could reach the vertex
    if (len(costs_from_other_vertices) == vertex_count):
      for i in costs_from_other_vertices.values():
        total_cost += i
      if (min == -1 or total_cost < min):
        min = total_cost
        place = vertex

  return (place, min)


def minMaxCost(cheapest_costs, vertex_count):
  # a function that accepts cheapest_costs (dictionary) and vertex_count (integer)
  # and returns the suitable meeting point place (string) and minimum MAXIMUM COST min (integer) spent by an individual
  min = -1
  for vertex, costs_from_other_vertices in cheapest_costs.items(): # these are the possible meeting points
    # check if everyone could reach the vertex
    if (len(costs_from_other_vertices) == vertex_count):
      cost = max(costs_from_other_vertices.values())
      if (min == -1 or cost < min):
        min = cost
        place = vertex
  
  return (place, min)