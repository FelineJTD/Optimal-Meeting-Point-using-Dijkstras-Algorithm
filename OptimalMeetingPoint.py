class Vertex:
  def __init__(self, name):
    self.name = name
    self.edges = {}
  def addEdge(self, destination, distance):
    self.edges[destination] = distance
  
def readVertices(filename):
  vertices = []
  possible_meeting_points = []

  with open(filename, "r") as f:
    data = f.read()

  data = data.replace(" ", "")
  data = data.split("\n")
  
  i = 0
  while(i < len(data) and data[i] != "end."):
    if (data[i] != "" and data[i][0] != "#"):
      data[i] = data[i].split(":")
      vertex = Vertex(data[i][0])
      data[i][1] = data[i][1].split(";")
      for j in range (len(data[i][1])):
        data[i][1][j] = data[i][1][j].split(",")
        vertex.addEdge(data[i][1][j][0], data[i][1][j][1])
      vertices.append(vertex)
    i += 1
  
  i += 1

  while(i < len(data) and data[i] != "end."):
    if (data[i] != "" and data[i][0] != "#"):
      possible_meeting_points.append(data[i])
    i += 1

  return(vertices, possible_meeting_points)
    
readVertices("vertices.txt")