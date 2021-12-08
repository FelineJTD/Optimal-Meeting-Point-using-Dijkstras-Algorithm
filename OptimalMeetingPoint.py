

def readVertices(filename):
  # a function that reads a file containing vertices data and returns
  # 1. vertices: dictionary of dictionary
  # 2. unreachables: array
  # 3. count: integer

  '''
  Accepted file format:
  
  # comments
  node: adjacent node, weight; another adjacent node, weight
  another node: adjacent node, weight

  # spaces and newlines do not matter
  # just remember not to put a semicolon (;) after the last adjacent node of each node
  '''

  vertices = {} # a dictionary of all the vertices and their corresponding dictionary of edges
  unreachables = [] # an array of unreachable nodes
  count = 0 # count of nodes

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
      # initiate dictionary of edges using node name as key
      vertices[name] = {}
      data[i][1] = data[i][1].split(";")
      # iteration to append edges data to dictionary
      for j in range (len(data[i][1])):
        data[i][1][j] = data[i][1][j].split(",")
        vertices[name][data[i][1][j][0]] = int(data[i][1][j][1])
  
  # check if there are any nodes which are unreachable
  for node in vertices.keys():
    found = False
    for edges in vertices.values():
      if node in edges:
        found = True
        break
    if not found:
      unreachables.append(node)    
  
  return (vertices, unreachables, count)
    

def completeDijkstra(vertices, start_city):
  cheapest_prices = {}
  previous_stopover_city = {}
  unvisited_cities = []
  rev_cities = []
  visited_cities = {}

  for i in vertices.keys():
    visited_cities[i] = False

  unvisited_cities.append(start_city)
  rev_cities.append(start_city)

  # initial loop
  while (unvisited_cities!=[]):
    # initiation
    curr_city = unvisited_cities[0]
    cheapest_prices[curr_city] = {}
    previous_stopover_city[curr_city] = {}
    cheapest_prices[curr_city][curr_city] = 0
    unvisited_cities.pop(0)
    visited_cities[curr_city] = True

    for adj_city, price in vertices[curr_city].items(): # iterate each adj cities
      if (not visited_cities[adj_city]):
        unvisited_cities.append(adj_city)
        rev_cities.append(adj_city)

      for vc, visited in visited_cities.items():
        if visited:
          try:
            price_through_current_city = cheapest_prices[vc][curr_city] + price
            try:
              if(cheapest_prices[vc][adj_city] > price_through_current_city):
                cheapest_prices[vc][adj_city] = price_through_current_city
                previous_stopover_city[vc][adj_city] = curr_city
            except:
              cheapest_prices[vc][adj_city] = price_through_current_city
              previous_stopover_city[vc][adj_city] = curr_city
          except:
            pass
    
  # revisiting cities
  for p in range(len(rev_cities)):
    curr_city = rev_cities[p]
    for q in range(p+1,len(rev_cities)):
      vc = rev_cities[q]
      for adj_city, price in vertices[rev_cities[p]].items(): # iterate each adj cities
        try:
          price_through_current_city = cheapest_prices[vc][curr_city] + price
          try:
            if(cheapest_prices[vc][adj_city] > price_through_current_city):
              cheapest_prices[vc][adj_city] = price_through_current_city
              previous_stopover_city[vc][adj_city] = curr_city
          except:
            cheapest_prices[vc][adj_city] = price_through_current_city
            previous_stopover_city[vc][adj_city] = curr_city
        except:
          pass
  
  return(cheapest_prices, previous_stopover_city)


def printRoutes(vertices, previous_stopover_node, destination):
  print("Here are everybody's routes:")
  for start_city in vertices.keys():
    curr_city = destination
    cheapest_route = []
    while (curr_city != start_city):
      cheapest_route.append(curr_city)
      curr_city = previous_stopover_node[start_city][curr_city]
    cheapest_route.append(start_city)
    cheapest_route.reverse()
    for i in range(len(cheapest_route)-1):
      print(f"{cheapest_route[i]} -> ", end="")
    print(cheapest_route[len(cheapest_route)-1])


def minTotalCost(cheapest_costs, previous_stopover_node, node_count):
  min = -1
  for node, costs_from_other_nodes in cheapest_costs.items(): # these are the possible meeting points
    total_cost = 0
    # check if everyone could reach the node
    if (len(costs_from_other_nodes) == node_count):
      for i in costs_from_other_nodes.values():
        total_cost += i
      if (min == -1 or total_cost < min):
        min = total_cost
        place = node

  return (place, min)


def minMaxCost(cheapest_costs, previous_stopover_node, node_count):
  min = -1
  for node, costs_from_other_nodes in cheapest_costs.items(): # these are the possible meeting points
    # check if everyone could reach the node
    if (len(costs_from_other_nodes) == node_count):
      cost = max(costs_from_other_nodes.values())
      if (min == -1 or cost < min):
        min = cost
        place = node
  
  return (place, min)