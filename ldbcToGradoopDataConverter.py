''' This script is used to convert a graph dataset from LDBC format to a Gradoop friendly json file.

    To run this script you need:
        - <path_to_vertices_dir>: a directory containing vertices files in csv format.
        - <path_to_relations_dir>: a directory containing relations files in a csv format.

    To run from terminal:
        $ "ldbcToGradoopDataConverter <path_to_vertices_dir> <path_to_edges_dir>"

    Output:
        - vertices.json
        - edges.json
'''

from os import walk
import glob
import json
import os
import random
import re
import sys
import uuid

class LDBCToGradoopDataConverter:

    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def write_to_dir(self, dataList, outpath):
        with open(os.path.abspath(outpath), "w") as outfile:
            for data in dataList:
                json.dump(data, outfile)
                outfile.write("\n")

    def read_from_dir(self, inpath):
        kvStore = {}

        files = []
        for (dirpath, dirnames, filenames) in walk(os.path.abspath(inpath)):
            files.extend(filenames)
        print files
        assert(len(files) > 1)
        for fle in files:
            with open(os.path.abspath(inpath)+'/'+fle, "r") as f:
                contents = f.read().split("\n")
                labels = contents[0].split('|')
                #print labels
                labels = labels[1:]

                for l in  contents:
                    line = l.split("|")
                    attr = {}
                    k = line[0]
                    data = line[1:]
                    #print labels
                    #print data
                    for i in range(len(labels)-1):
                        if not len(data) < len(labels)-1:
                            attr[labels[i]] = data[i]
                    kvStore[k] = attr
                    #print k, attr
        return kvStore

    def read_ldbc_vertices(self, inputFile):
        self.verticesDict = self.read_from_dir(inputFile)
        #print verticesDict

    def read_ldbc_relations(self, inputFile):
        self.relationsDict = self.read_from_dir(inputFile)
        '''
        for l in open(os.path.abspath(inputFile), "r"):
            line = l.strip().split("|")
            edgesDict[line[0]] = line[1:]
        '''
        #print relationsDict

    def create_json_vertices(self, outputPath):
        print "creating JSON vertices"
        vertices = []
        #vId = 0
        # TODO: generate hexadeximal id that works for gradoop.
        for k,v in self.verticesDict.iteritems():
            if not k:
                continue
            if k is  "" or re.match('^[a-zA-Z]+', k) is not None:
                continue
            ldbcVertex = {}
            #print k,v
            #print v
            ldbcVertex["id"] = "{:024x}".format(int(k))
            ldbcVertex["data"] = v
            meta = {}
            meta["label"] = "test"
            ldbcVertex["meta"] = meta
            vertices.append(ldbcVertex)
        self.write_to_dir(vertices, outputPath + "/" + "vertices.json")
        #print jsonVertices
        print "done."

    def create_json_edges(self, outputPath):
        print "creating JSON edges"
        eId = 0
        edges = []
        # TODO: generate hexadeximal id that works for gradoop.
        for k, v in self.relationsDict.iteritems():
            if k is "" or re.match('^[a-zA-Z]+', k) is not None:
                continue
            if len(v.values()) > 0:
                values = v.values()[0]
            if not len(v.values()) > 0 or re.match('^[a-zA-Z]+', values) is not None:
                continue
            ldbcEdge = {}
            #print k, v
            #print eId
            ldbcEdge["id"] = "{:024x}".format(eId)
            ldbcEdge["source"] = "{:024x}".format(int(k))
            meta = {}
            meta["label"] = "test"
            ldbcEdge["meta"] = meta
            ldbcEdge["target"] = "{:024x}".format(int(v.values()[0]))
            ldbcEdge["data"] = {"type":"edge"}
            if len(v.values()) > 1:
                ldbcEdge["data"] = v.values()[1:]
            edges.append(ldbcEdge)
            eId += 1

        self.write_to_dir(edges, outputPath + "/" + "edges.json")
        print "done."

    def create_json_graphs(self, outputPath):
        print "creating JSON graphs"
        graphs = []
        graph = {}
        # TODO: generate hex id that works for gradoop.
        graph["id"] = "{:024x}".format(random.randint(1, 10000))
        meta = {}
        meta["label"] = "test"
        graph["meta"] = meta
        graph["data"] = {"type": "test"}
        graphs.append(graph)
        self.write_to_dir(graphs, outputPath + "/" + "graphs.json")
        print "done."

def main(argv):
    if(len(argv) < 3):
        print "ldbcToGradoopDataConverter <path/to/vertices> <path/to/edges> <output dir>"
        sys.exit()

    verticesFile = argv[0]
    relationsFile = argv[1]
    outputDir = argv[2]
    dc = LDBCToGradoopDataConverter()
    dc.read_ldbc_vertices(verticesFile)
    #print dc.verticesDict
    dc.read_ldbc_relations(relationsFile)
    #print dc.relationsDict
    dc.create_json_vertices(outputDir)
    dc.create_json_edges(outputDir)
    dc.create_json_graphs(outputDir)
    print "done."

if __name__ == "__main__":
    main(sys.argv[1:])
