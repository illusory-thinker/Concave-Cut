import os
import sys
import numpy as np
import scipy.io as scio
from sklearn.metrics import confusion_matrix
from sklearn.metrics import adjusted_rand_score as ari_ori
from sklearn.metrics import normalized_mutual_info_score as nmi_ori
from sklearn.metrics.pairwise import euclidean_distances
from scipy.optimize import linear_sum_assignment

from cppfuns_ import cppcluster

def accuracy(real,pred):#Calculate the accuracy of prediction
    cm = confusion_matrix(y_true = real, y_pred = pred)
    cost_m = np.max(cm) - cm
    indices = linear_sum_assignment(cost_m)
    indices = np.asarray(indices)
    indexes = np.transpose(indices)
    total = 0
    for row, column in indexes:
        value = cm[row][column]
        total += value
    return total * 1. / np.sum(cm) 

#Load data
data = scio.loadmat("FERET.mat")
y_true = data['y_true'].reshape(-1)
clusters = len(np.unique(y_true))
X = data['X']
vnum = len(y_true)
print("Data loaded!")

num_anchor = int(min(1024,vnum))
knn = int(min(int(vnum/clusters*1.2),num_anchor-2))

exptimes = 10
epoches = 10
#Construct the graph
Dis = euclidean_distances(X, X, squared=True)
np.fill_diagonal(Dis, -1)
arrIndex = Dis.argsort() 
Aindex = arrIndex[:,1:knn+1]
np.fill_diagonal(Dis, 0)
Dis.sort()
Asim = Dis[:,1:knn+1]
sigma = np.mean(Asim)
Asim = np.exp(-Asim/(2*sigma**2))
Asim = Asim.astype(np.float64)
Aindex = Aindex.astype(np.int32)

results = np.random.randint(clusters, size = (exptimes,vnum),dtype = np.int32)
times = np.zeros((exptimes,),dtype = np.float64)
cppcluster(results, Aindex, Asim, times, epoches, clusters)
acc = np.array([accuracy(y_true, y) for y in results])
ari = np.array([ari_ori(labels_true=y_true, labels_pred=y_pred) for y_pred in results])
nmi = np.array([nmi_ori(labels_true=y_true, labels_pred=y_pred) for y_pred in results])
print(f"half-cut: {np.mean(acc):.3f},{np.std(acc):.3f},{np.mean(ari):.3f},{np.std(ari):.3f},{np.mean(nmi):.3f},{np.std(nmi):.3f},{np.mean(times):.3f}, {np.std(times):.3f}", flush=True)