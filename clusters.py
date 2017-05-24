from math import sqrt
from cluster import bicluster
import pdb

def readfile(filename):
    lines = [line for line in file(filename)]

    '''First line is the column titles'''
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        '''First column in each row is the row name'''
        rownames.append(p[0])
        '''The data for this row is the remainder of the row'''
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

def pearson(v1, v2):
    '''Simple sum'''
    sum1 = sum(v1)
    sum2 = sum(v2)

    '''Sum of the square'''
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    '''Sum if the products'''
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    '''Calculate r (Pearson score)'''
    num = pSum - (sum1*sum2/len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2)/len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))

    if den == 0: return 0

    return 1.0 - num/den

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    '''Clusters are initially just the rows'''
    clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        '''Loop through every pair looking for the smallest distance'''
        for i in range(i + 1, len(clust)):
            for j in range(i+1, len(clust)):
                '''distances is the cache of distance calculations'''
                if(clust[i].id, clust(j).id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i,j)

        '''calculate the average of the two clusters'''
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        '''create the new cluster'''
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest, id=currentclustid)

        '''cluster ids that weren't in the original set are negative'''
        currentclustid = -1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    '''Indent to make a hierarchy layout'''
    for i in range(n): print ' ',
    if clust.id < 0:
        '''Negative id means that this is branch'''
        print '-'
    else:
        '''positive id means that this is an endpoint'''
        if labels == None: print clust.id
        else: print labels[clust.id]

    '''Now print the right and left branches'''
    if clust.left != None: printclust(clust.left, labels=labels, n=n+1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n+1)
