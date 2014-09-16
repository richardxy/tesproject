__author__ = 'rxie'
__author__ = 'rxie'
#!/usr/bin/env python

# based on:
# http://rajmak.wordpress.com/2013/04/27/clustering-text-map-reduce-in-python/

#from helper import lev_dist as distance
from Levenshtein import distance
from pprint import pprint

DISTANCE = 10

class Cluster(object):
    """
    Clustering a list of (sorted!) strings.

    I use it for clustering URLs. After extracting all the links (or images)
    from a web page, I use this class to group together similar URLs. It also
    identifies the largest cluster.
    """
    def __init__(self):
        self.clusters = {'clusters': {}}

    def clustering(self, elems):
        """
        Clusterize the input elements.

        Input: list of words (e.g. list of URLs). It MUST be sorted!

        Process: build a dictionary where keys are cluster IDs (int) and
                 values are lists (elements in the given cluster)
        """
        clusters = {}
        cid = 0

        for i, line in enumerate(elems):
            if i == 0:
                clusters[cid] = []
                clusters[cid].append(line)
            else:
                last = clusters[cid][-1]
                if distance(last, line) <= DISTANCE:
                    clusters[cid].append(line)
                else:
                    cid += 1
                    clusters[cid] = []
                    clusters[cid].append(line)
        #
        self.clusters['clusters'] = clusters
        self.clusters['clusters']['largest'] = self.get_largest_cluster()
        self.clusters['clusters']['number_of_clusters'] = cid + 1

    def get_largest_cluster(self):
        clusters = self.clusters['clusters']

        maxi_k = None
        maxi_v = None
        first = True
        for k,v in clusters.iteritems():
            if first:
                maxi_k = k
                maxi_v = len(v)
                first = False
            else:
                if len(v) > maxi_v:
                    maxi_v = len(v)
                    maxi_k = k
        #
        return clusters[maxi_k]

    def show(self):
        pprint(self.clusters)

def get_clusters(elems):
    elems = sorted(elems)
    cl = Cluster()
    cl.clustering(elems)
    return cl.clusters['clusters']

#############################################################################

if __name__ == "__main__":
    import numpy as np
    #%pylab inline
    from pylab import *
    import pandas as pd
    import json
    import matplotlib.pyplot as plt
    import re


    json_local_1 = 'url_sample_1.json'
    #uri_sample_2.json and uri_sample_3.json are in the directory too
    #these are the files in the links from http://nara.endgames.local/crawl/

    json_list = []
    with open(json_local_1) as f:
        for line in f:
            json_list.append(json.loads(line))
    i=0
    li=[]
    for item in json_list:
        if(i<100000):
            i=i+1

            if(len(item)>1):
                for type in item:
                    li = li+ item[type]
        else:
            break
    cl = Cluster()
    cl.clustering(li)
    cl.show()