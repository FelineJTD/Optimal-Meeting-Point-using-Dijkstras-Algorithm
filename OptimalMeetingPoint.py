def readVertices(filename):
  vertices = {}

  with open(filename, "r") as f:
    data = f.read()

  data = data.replace(" ", "")
  data = data.split("\n")
  
  for i in range(len(data)):
    if (data[i] != "" and data[i][0] != "#"):
      data[i] = data[i].split(":")
      name = data[i][0]
      vertices[name] = {}
      data[i][1] = data[i][1].split(";")
      for j in range (len(data[i][1])):
        data[i][1][j] = data[i][1][j].split(",")
        vertices[name][data[i][1][j][0]] = int(data[i][1][j][1])
  
  return(vertices)
    

def completeDijkstra(vertices):
  cheapest_prices = {}
  previous_stopover_city = {}
  unvisited_cities = []
  rev_cities = []
  visited_cities = {}

  for i in vertices.keys():
    visited_cities[i] = False

  start_city = i
  unvisited_cities.append(start_city)
  rev_cities.append(start_city)

  # initial loop
  while (unvisited_cities!=[]):
    # initiation
    print(unvisited_cities)
    curr_city = unvisited_cities[0]
    print("\ncurr_city =", curr_city)
    cheapest_prices[curr_city] = {}
    previous_stopover_city[curr_city] = {}
    cheapest_prices[curr_city][curr_city] = 0
    unvisited_cities.pop(0)
    visited_cities[curr_city] = True
    print(cheapest_prices)
    print(previous_stopover_city)

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
  
  print(cheapest_prices)
  return(cheapest_prices, previous_stopover_city)
  


  
a = readVertices("Atlanta.txt")
completeDijkstra(a)