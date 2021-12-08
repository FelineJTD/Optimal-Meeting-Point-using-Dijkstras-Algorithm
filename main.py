from OptimalMeetingPoint import printRoutes, readVertices, completeDijkstra, minTotalCost, minMaxCost, printRoutes
import sys

file_name = sys.argv[1]

vertices, unreachables, count = readVertices(file_name)
if (len(unreachables) > 1):
  print("There is no suitable meeting point.")
else:
  if (len(unreachables) == 1):
    # use the unreachable node as a starting point
    start_node = unreachables[0]
  else:
    # use the first node as a starting point
    start_node = next(iter(vertices))
  cheapest, prev_node = completeDijkstra(vertices, start_node)

  try:
    method = int(sys.argv[2])
  except:
    print("Which method would you like to use to determine the most suitable meeting point?")
    print("1. Minimize the total cost (= minimize the average cost) of travel")
    print("2. Minimize the maximum individual cost of travel")
    print("3. Both")
    method = int(input("> "))

  if (method == 1 or method == 3):
    print("\n----- MINIMIZING TOTAL COST -----")
    place, min = minTotalCost(cheapest, prev_node, count)
    print(f"The most suitable meeting point is {place} with the total cost of {min}.")
    printRoutes(vertices, prev_node, place)
  if (method == 2 or method == 3):
    print("\n----- MINIMIZING MAXIMUM COST -----")
    place, min = minMaxCost(cheapest, prev_node, count)
    print(f"The most suitable meeting point is {place} with the maximum cost of {min}.")
    printRoutes(vertices, prev_node, place)