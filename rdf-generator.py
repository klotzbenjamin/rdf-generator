# -*- coding: utf-8 -*-
#import pycurl
import json,csv,pickle
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, OWL
from rdflib.namespace import DC, FOAF, Namespace, NamespaceManager,XSD
from optparse import OptionParser



#Parser options
parser = OptionParser()
parser.add_option("-i","--input",help="input file to use for the raw data",action="store", type="string")
parser.add_option("-s","--scheme",help="input ontological scheme to use")
parser.add_option("-m","--mapping",help="input mapping to use")
parser.add_option("-o","--output",help="output file to use")
parser.add_option("-g","--graph",help="base graph file to use")

(options,args) = parser.parse_args()

if not options.input:
    parser.error('Input not given')
if not options.scheme:
    parser.error('Scheme not given')
if not options.mapping:
    parser.error('Mapping not given')

inputFile=options.input
schemeFile=options.scheme
mappingFile=options.mapping
if not options.output:
    outputFile="output.ttl"
else:
    outputFile=options.output
if not options.graph:
    graphFile="input/baseGraph.ttl"
else:
    graphFile=options.output

"""
mappingFlat={
":var1":"latitude",
":var2":"longitude",
":var3":"timestamp",
":var4":"vehicle_speed",
":cst1":"<http://automotive.eurecom.fr/simulator/vehicle>",
":cst2":"xsd:float",
":cst3":"<http://automotive.eurecom.fr/simulator/signal/speed>"}

mappingComplex={
":var1":"location.latitude",
":var2":"location.longitude",
":var3":"timestamp",
":var4":"data.vehicle_speed",
":cst1":"<http://automotive.eurecom.fr/simulator/vehicle>",
":cst2":"xsd:float",
":cst3":"<http://automotive.eurecom.fr/simulator/signal/speed>"}


with open('mapping-flat.pkl','w') as f:
    pickle.dump(mappingFlat,f)
    f.close()

with open('mapping-complex.pkl','w') as f:
    pickle.dump(mappingComplex,f)
    f.close()
"""

#Open mapping as a dictionary
with open(mappingFile,"r") as f:
    mappingComplex=pickle.load(f)
    f.close()



#Find the value in a JSON file from a path
def getValue(data, path):
    y=data
    for x in path.split('.'):
        y=y[x]
    return str(y)

#get dict from JSON or CSV inputs
def getRawData():
    with open(inputFile) as f:
        if inputFile.split(".")[1]=="json":
            data=json.load(f)
        elif inputFile.split(".")[1]=="csv":
            data=dict((row[0],row[1]) for row in csv.reader(f))
        else:
            print "Input file not supported"
        return data

#Replace variable in the scheme with their value
def fillScheme(scheme, mapping):
    data=getRawData()
    for variable in mapping:
        if "cst" in variable:
            scheme=scheme.replace(variable,mapping[variable])
        elif "var" in variable:
            #scheme=scheme.replace(variable,str(data[mapping[variable]]))
            scheme=scheme.replace(variable,getValue(data, mapping[variable]))
        else:
            print "Error in the mapping file"
    return scheme

#Open scheme and replace its variables with the mapped values
with open(schemeFile,"r") as x:
    scheme=x.read().replace('\n', '')
scheme=fillScheme(scheme,mappingComplex)

#Create a graph in RDFlib with the new triples
gScheme=Graph()
gScheme.parse(data=scheme,format='turtle')

#Open base graph and merge it with the new triples
g=Graph()
g.parse("input/baseGraph.ttl",format='turtle')
g=g+gScheme

#Save the output graph
g.serialize(destination=outputFile,format="turtle")

