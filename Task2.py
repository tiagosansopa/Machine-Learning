#Santiago Solórzano
#Proyecto 2 task 2

class Cluster(object):
  def __init__(self, numero, pi, mu, zigma,n):
    self.numero = numero
    self.pi = pi
    self.mu = mu
    self.zigma = zigma
    self.det = np.linalg.det(self.zigma)
    self.eij = np.zeros(n)

  def saludar(self):
    return "hola cluster " + str(self.numero)


import matplotlib.pyplot as pt
import random as r
import numpy as np
import math

with open("coordenadas.txt") as f:
    content = f.read().splitlines()

points = [s[1:-1].split(",") for s in content ]
points = [[float(p) for p in i] for i in points]
k = int(input("Cantidad de clusters?\n"))

clusters =[]
for i in range(k):
  mu = [r.randint(-10,10),r.randint(-10,10)]
  while True:
    zigma = np.random.random_integers(-10,10,(2,2))
    if(np.linalg.det(zigma) > 0):
      break
  clusters.append(Cluster(i,1/k,mu,zigma,len(points)))

for i in range(1):
  for index, p in enumerate(points):
    R = 0.0
    for c in clusters:
      eij = c.pi * math.pow(2*math.pi,-(2)/2) * math.pow(c.det,-1/2) * math.exp(np.matmul(np.matmul(-0.5 * np.transpose(np.array(p)-np.array(c.mu)), np.linalg.inv(c.zigma)), (np.array(p)-np.array(c.mu))) )
	  #eij = c.pi * math.pow(2*math.pi,-(2)/2) * math.pow(c.det,-1/2) * math.exp(-0.5 * np.transpose(np.array(p)-np.array(c.mu)) * np.linalg.inv(c.zigma) * (np.array(p)-np.array(c.mu)) )
      c.eij[index] = eij
      R+=eij
    for c in clusters:
      c.eij[index] = c.eij[index] /R  

for c in clusters:
  util = np.sum(c.eij)
  c.pi = util/len(c.eij)
  
  tmp = 0
  for index, p in enumerate(points):
    tmp += np.array(p) * c.eij[index]
  c.mu = tmp/util
  
  tmp = 0
  for index, p in enumerate(points):
    tmp += np.matmul(c.eij[index] * (np.array(p)-np.array(c.mu)), np.transpose(np.array(p)-np.array(c.mu)))
  np.zigma = tmp/util
  
  print(c.eij)	  
for p in points:
  pt.plot(p[0],p[1],'ro')

for c in clusters:
  pt.plot(c.mu[0],c.mu[1],'bs')	
pt.axis([-10,10,-10,10])

pt.show()








