import sys
#import math as m
#import os.path 
#import timeit

class readInput(object):
  'this class reads a piped input'
  def __init__(self):
    pass
  def getInput(self):
    lines = []
    Done = 0;
    while not Done:
      myline = input()
      lines.append(myline)
      if myline == "0 0":
        Done = 1
    return lines


class GetMaps(object):
  'this class reads the input file'

  def __init__(self):
    pass

  def build(self):
    lines = readInput().getInput()
    assert len(lines) > 0, 'the file is empty!'
    nline = 0
    Done = False
    mapObjs = []
    while not Done:
      firstLine = lines[nline].split()
      nline += 1
      N = int(firstLine[0])
      M = int(firstLine[1])
      if (M == 0 and N == 0):
        break
      assert (M>0 and N>0),'file format is wrong!'
      block_i = []
      block_j = []
      S_i, S_j, T_i, T_j = 0 , 0 , 0 , 0
      for j in range(N-1,-1,-1):
        for i in range(M):
          char = lines[nline][i]
          if (char == '.'):
            pass
          elif (char == '#'):
            block_i.append(i)
            block_j.append(j)
          elif (char == 'S'):
            S_i = i
            S_j = j
          elif (char == 'T'):
            T_i = i
            T_j = j
          else:
            print("char: ", char)
            assert 0,'Character %c NOT recognized!' % char
        nline += 1
      mapObjs.append(Map(M,N,block_i,block_j,Vertex(S_i,S_j,0,0),Vertex(T_i,T_j,0,0)))
      del block_i
      del block_j
    return mapObjs

class FileParser(object):
  'this class reads the input file'

  def __init__(self,inFile):
    #assert os.path.isfile(inFile),'The file does not exist!'
    self.file = inFile

  def Parse(self):
    lines = [line.strip() for line in open(self.file,'r')]
    assert len(lines) > 0, 'the file is empty!'
    nline = 0
    Done = False
    mapObjs = []
    while not Done:
      firstLine = lines[nline].split()
      nline += 1
      N = int(firstLine[0])
      M = int(firstLine[1])
      if (M == 0 and N == 0):
        break
      assert (M>0 and N>0),'file format is wrong!'
      block_i = []
      block_j = []
      S_i, S_j, T_i, T_j = 0 , 0 , 0 , 0
      for j in range(N-1,-1,-1):
        for i in range(M):
          char = lines[nline][i]
          if (char == '.'):
            pass
          elif (char == '#'):
            block_i.append(i)
            block_j.append(j)
          elif (char == 'S'):
            S_i = i
            S_j = j
          elif (char == 'T'):
            T_i = i
            T_j = j
          else:
            print("char: ", char)
            assert 0,'Character %c NOT recognized!' % char
        nline += 1
      mapObjs.append(Map(M,N,block_i,block_j,Vertex(S_i,S_j,0,0),Vertex(T_i,T_j,0,0)))
      del block_i
      del block_j
    return mapObjs

class Vertex(object):
  'this is a vertex structure \
  it has: \
  positions: ip, jp \
  direction: dir \
  color: col'

  def __init__(self,ip,jp,dir,col):
    self.ip = ip
    self.jp = jp
    self.dir = dir
    self.col = col

  def printVer(self):
    print("(ip:" , self.ip , ", jp:" , self.jp , ", dir:" , self.dir , ", col:" , self.col,")")

class Map(object):
  'this is the map class \
  reads a map from a file'

  def __init__(self,M,N,block_i,block_j,V_S,V_T):
    self.M = M # number of columns
    self.N = N # number of rows
    self.SV = V_S
    self.TV = V_T
    self.Block_i = block_i
    self.Block_j = block_j
    self.Inside_mat = [True for i in range(self.M) for j in range(self.N)]
    for i in range(len(self.Block_i)):
      ind_i = block_i[i]
      ind_j = block_j[i]
      ind_mat = ind_i*self.N + ind_j
      self.Inside_mat[ind_mat] = False
      

  def isInside(self,ip,jp):
    inside = True
    inside = inside and ip>=0 and jp>=0 and ip<self.M and jp<self.N and self.Inside_mat[ip*self.N+jp]
    return inside
    
  def isBlock(self,ip,jp):
    return (not self.Inside_mat[ip*self.N+jp])

  def printMap(self):
    for j in range(self.N-1,-1,-1):
      for i in range(self.M):
        if (self.isInside(i,j)):
          if (i==self.SV.ip and j==self.SV.jp):
            sys.stdout.write( " S " )
          elif (i==self.TV.ip and j==self.TV.jp):
            sys.stdout.write( " T " )
          else:
            sys.stdout.write( " - " )
        elif (self.isBlock(i,j)):
          sys.stdout.write( " # " )
      print() 
    
class Graph(object):
  'this is a graph structure'

  def __init__(self,mapObj):
    self.map = mapObj
    self.buildGraph(mapObj)

  def buildGraph(self,mapObj):
    self.M = mapObj.M
    self.N = mapObj.N
    self.SV    = mapObj.SV
    self.TV = mapObj.TV
    self.dirSize = 4
    self.colSize = 5
    # all the posible verticies
    self.V = [Vertex(i,j,dir,col) for i in range(self.M) for j in range(self.N) for dir in range(self.dirSize) for col in range(self.colSize)]
    # Linked list of the verticies (connectivity) start with the id of the vertex (shouldn't have any duplicates in V)
    self.LL = [[self.getInd(v)] for v in self.V]

    # build the LL
    setInd = self.getInd2
    checkInside = mapObj.isInside
    ipMove = [0, -1, 0, 1]
    jpMove = [1, 0, -1, 0]
    for v in self.V:
      vip = v.ip
      vjp = v.jp
      vdir = v.dir
      vcol = v.col
      ind = setInd(vip,vjp,vdir,vcol)
      # change it to a for loop
      self.LL[ind].append( setInd(vip,vjp,(vdir+1)%self.dirSize,vcol) )
      self.LL[ind].append( setInd(vip,vjp,(vdir-1)%self.dirSize,vcol) )
      if (checkInside(vip+ipMove[vdir],vjp+jpMove[vdir])):
        self.LL[ind].append( setInd(vip+ipMove[vdir],vjp+jpMove[vdir],vdir,(vcol+1)%self.colSize) )
      
  def getInd(self,v):
    return self.colSize*(self.dirSize*(v.ip*self.N + v.jp) + v.dir) + v.col
    
  def getInd2(self,ip,jp,dir,col):
    return ip*self.N*self.dirSize*self.colSize + jp*self.dirSize*self.colSize + dir*self.colSize + col

  def getVert(self,ind):
    return self.V[ind]

  def check(self):
    for v in self.LL:
      self.map.printMap()
      for vv in v:
        self.V[vv].printVer()
      print(" ")

class BFS(object):
  'the structure for Breadth First Search graphs'

  def __init__(self,G):
    self.Graph = G         # Graph object
    self.LL    = G.LL # Link List
    self.V     = G.V  # Verticies

  def BFS_ShortDist(self,v,w):
    V_visit = [0 for i in range(len(self.V))]
    vInd = self.Graph.getInd(v)
    wInd = self.Graph.getInd(w)
    Lev_list = [[vInd]]
    V_visit[vInd] = 1
    cur_lev = 0
    Done = False
    while (not Done):
      Lev_list.append([])
      for vInd in Lev_list[cur_lev]:
        for nInd in self.LL[vInd][1:]:
          if (V_visit[nInd] == 0):
            if (nInd == wInd):
              return cur_lev+1
            Lev_list[cur_lev+1].append(nInd)
            V_visit[nInd] = 1
      #print "Lev_list: " , Lev_list[cur_lev+1]
      if (len(Lev_list[cur_lev+1]) == 0):
        return -1
      cur_lev+=1

def main():
  # I'm keeping unnecessary things around
  #myMaps = FileParser('inFile.txt').Parse()
  myMaps = GetMaps().build()
  for maps in myMaps:
    maps.printMap()
    print()
    G = Graph(maps)
    prob = BFS(G)
    short_dist = 1e20
    for dir in range(4):
      short_dist = min(short_dist,prob.BFS_ShortDist(G.SV,Vertex(G.TV.ip,G.TV.jp,dir,0)))
    if (short_dist != -1):
      print("Case #"+str(myMaps.index(maps)+1))
      print("minimum time = " + str(short_dist) + " sec")
      print()
    else:
      print("Case #"+str(myMaps.index(maps)+1))
      print("destination not reachable")
      print()

if __name__ == "__main__":
  main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
