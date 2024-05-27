import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
from sklearn.metrics import confusion_matrix
from sklearn.metrics.pairwise import euclidean_distances
from scipy.optimize import linear_sum_assignment

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

data = scio.loadmat("FERET.mat")
y_true = data['y_true'].reshape(-1)
clusters = len(np.unique(y_true))
X = data['X']
vnum = len(y_true)
print("Data loaded!")

num_anchor = int(min(1024,vnum))
knn = int(min(int(vnum/clusters*1.2),num_anchor-2))

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
for i in range(vnum):
    for j in range(knn):
        tindex = Aindex[i][j]
        if i not in Aindex[tindex]:
            Aindex[i][j] = -1
results = [0]*vnum
for i in range(clusters):
    results[i] = i
for i in range(clusters,vnum):
    results[i] = np.random.randint(clusters)

epoches = 20
isum = np.zeros(clusters)
for i in range(vnum):
    tindex = results[i]
    for j,k in zip(Aindex[i],Asim[i]):
        if j != -1 and results[j] == tindex:
            isum[tindex] += k
tisum = dict()
acc = []
for epoch in range(epoches):
    for i in range(vnum):
        old_index = results[i]
        tisum.clear()
        if isum[old_index] != 0:
            tisum[results[i]] = 0
            for j in Aindex[i]:
                if j!=-1 and results[j] not in tisum:
                    tisum[results[j]] = 0
            tifunc = dict()
            for j, k in zip(Aindex[i],Asim[i]):
                if j != -1:
                    tisum[results[j]] += k
            for key1 in tisum.keys():
                if key1 == old_index:
                    tifunc[key1] = np.sqrt(isum[key1]) - np.sqrt(isum[key1] - 2*tisum[key1])
                else:
                    tifunc[key1] = np.sqrt(isum[key1] + 2 * tisum[key1]) - np.sqrt(isum[key1])
            maxindex = max(tifunc, key=lambda x: tifunc[x])
            if maxindex != old_index:
                isum[maxindex] += 2*tisum[maxindex]
                isum[old_index] -= 2*tisum[old_index]
                results[i] = maxindex  
    fsum = 0
    for i in range(clusters):
        fsum += np.sqrt(isum[i])
    acc.append(fsum)

x = [int(i+1) for i in range(len(acc))]  
plt.rcParams['font.size'] = '22'
plt.figure(figsize=(6.4, 4.8))
plt.title("FERET",fontsize = 30)
plt.xticks(np.arange(1, epoches+1, 2))
plt.margins(0.05, 0.05)
plt.xlabel('Iteration')
plt.ylabel('Obj.',y=1.02,labelpad=-40,fontsize = 30,rotation = 0)
plt.scatter(np.arange(1, epoches+1, 1), acc,color = "red")
plt.plot(np.arange(1, epoches+1, 1),acc,color = "red")
plt.savefig("FERET.pdf",bbox_inches=mt.Bbox([[-0.1, -0.5], [6.5, 4.9]]))