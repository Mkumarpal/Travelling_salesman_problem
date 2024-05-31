import gurobipy as gp
from gurobipy import *

# data = {}
locations = [
        # fmt:off
      (4, 4),  # depot
      (2, 0), (8, 0),  # locations to visit
      (0, 1), (1, 1),
      (5, 2), (7, 2),
      (3, 3), (6, 3),
      (5, 5), (8, 5),
      (1, 6), (2, 6),
      (3, 7), (6, 7),
      (0, 8), (7, 8)
        # fmt:on
    ]

# distance = [
#        [0, 29, 20, 21],
#        [29, 0, 15, 17],
#        [20, 15, 0, 28],
#        [21, 17, 28, 0]
#    ]
# define the no of cities
n = len(locations)
print(n)

I = n
J = n
# find the data of the distance for the i in I and j in J
# data is [(1,2), (2,2), (3,2)........]
data = [(l[0]*114, l[1]*80) for l in locations]
print(data)
distance = [[0 for j in range(J)] for i in range(J)]
print(distance)
# define the distance matrix
for i in range(I):
      print("iii",i)
      for j in range(J):
            print("jjj", j)
            if i == j:
                  distance[i][j] = 0
            else:
                  distance[i][j] = abs(data[i][0]-data[j][0]) + abs(data[i][1]-data[j][1])

print(distance)

#define the model
model = gp.Model("Travellling sales man problems")

#define the decision  variables x[i,j] is the xij for i in I for j in J
x = model.addVars(I,J, vtype =  GRB.BINARY, name = "x_i_j")

# create variable u[i] for subtour elimination
u = model.addVars(I, vtype =  GRB.CONTINUOUS, name = "ui")

# set the objective functions (dij*xij for i in I for j in J)
# minimize the distance of the travelling distance
model.setObjective(quicksum(distance[i][j]*x[i,j] for i in range(I) for j in range(J)), GRB.MINIMIZE)

# add the constraints
for i in range(I):
       model.addConstr(quicksum(x[i,j] for j in range(J) if i !=j) ==1, "sum of x[i,j] fix i and j is varying ")

for j in range(J):
      model.addConstr(quicksum(x[i,j] for i in range(I) if i!=j ) ==1, "sum of x[i,j] fix j and i is varying")

# subtour elimination constraints

for i in range(1,n):
      for j in range(1,n):
            if i != j:
                  model.addConstr(u[i]-u[j] + n*x[i,j] <= n -1,  "subtour_[i]_[j]" )

# optimize the model
model.optimize()


# display the results
print("optimal tour")
print(model.ObjVal)
# tour = []
# for i in range(n):
#       for j in range



if model.Status == GRB.OPTIMAL:
      print("optimal soltuion", model.ObjVal)
      print("dual of the solution", model.getAttr("x"))
      tour_tuple = []
      for i in range(n):
          for j in range(n):
              if x[i,j].X >0.5:
                  print(f"value of x[i,j]={x[i,j].X} where {i}and {j}")
                  print(f"the city{i}, to city{j}, distance {distance[i][j]}")
                  tour_tuple.append((i,j))
      print(f"The total optimal distance is {model.ObjVal}")
      print(tour_tuple)
      # print("X* =", each for each in x"")
# if model.Status == GRB.OPTIMAL:
#     print("Optimal solution", model.ObjVal)
#     print("dual of the solution", model.getAttr("x"))
#     constr= model.getConstrs()
#     # for d in model.getConstrs():
#     #     print("hello",d.getAttr("Pi"))
#     # print("dual of the constraint", model.getAttr("L1"))
#     print("x*= ", x.X)
#     print("y*= ", y.X)
#     print("y*= ", z.X)
#     print("a*= ", a.X)
#     print("c*= ", c.X)
#
import networkx as nx
import matplotlib.pyplot as plt


g = nx.Graph()


for i, each in enumerate(locations):
    g.add_node(i,pos = each )

pos = nx.get_node_attributes(g,'pos')

print(pos)

for each in tour_tuple:
    g.add_edge(each[0], each[1])


nx.draw(g,pos, with_labels=True)

plt.show()
