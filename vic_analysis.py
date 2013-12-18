import sys
import pdb
from numpy import *
import math
import argparse

parser = argparse.ArgumentParser(description='Analysis and assessment of variant information content (vic)')
parser.add_argument('inputfile', metavar='INPUTFILE', type=str, help='The input file')
parser.add_argument('--fcol', type=int, default=4, help='The column number where the features start')
parser.add_argument('--regcol', type=int, default=3, help='The column specifying the region')
args = parser.parse_args()
ifile = open(args.inputfile)
freqfile = open(args.inputfile+'.freq', 'w')
vicfile = open(args.inputfile+'.vic', 'w')

header = True
region_values = {}

convert = {'str':lambda x:str(x), 'int':lambda x:int(x), 'float':lambda x:float(x)}
lines = ifile.readlines()
for nl, line in enumerate(lines):
    line = line.strip()
    if line[0] != '#' and len(line) > 0:
	fields = line.split('\t')
	if header:
	    numfeatures = len(fields[args.fcol:])
	    types = ['str']*numfeatures
	    values = []
	    freqs = {}
	    vic_fields = []
	    values = []
	    for i, feature in enumerate(fields[args.fcol:]):
		if ':' in feature:
		    types[i] = feature.split(':')[-1]
	    header = False
        else:
            region = fields[args.regcol]
	    if region in region_values:
		for i, feature in enumerate(fields[args.fcol:]):
		    region_values[region][1][i].append(convert[types[i]](feature))
		    region_values[region][0].append(fields[:3])
	    else:
		region_values[region] = [[fields[:3]], []]
		for i, feature in enumerate(fields[args.fcol:]):
		    region_values[region][1].append([convert[types[i]](feature)]) 
		    
for region in region_values:
    vic_fields = region_values[region][0]
    values = region_values[region][1]
    bin_edges = []
    tuples = []
    freqs = {}
    for i in range(numfeatures):
	bin_edges.append([])
    for i in range(numfeatures):
	if types[i] == 'int' or types[i] == 'float':
	    hist, bin_edges[i] = histogram(values[i])
    for i in range(len(values[0])):
	tuplist = []
	for j in range(numfeatures):
	    if types[j] == 'int' or types[j] == 'float':
		idx = -1
		for k in range(len(bin_edges[j])):
		    if values[j][i] > bin_edges[j][k]:
			idx = k-1
			break
		tuplist.append(bin_edges[j][idx])
	    else:
		tuplist.append(values[j][i])
	tuples.append(tuple(tuplist))
    for t in tuples:
	if t not in freqs:
	    count = 0.
	    for t2 in tuples:
		if t == t2:
		    count += 1
	    freqs[t] = count/len(tuples)
    for i,t in enumerate(tuples):
	p = freqs[t]
	vicfile.write('%s\t%s\t%s\t' % (vic_fields[i][0], vic_fields[i][1], vic_fields[i][2]))
	vicfile.write('%s\t%s\n' % (region, -p*math.log(p, 2)))
    freq_output = region + '\t'
    for tup in freqs:
	freq = freqs[tup]
	freq_output += ' %s:%s' % (str(tup).strip('()'), freq)
    freqfile.write(freq_output + '\n')
		

vicfile.close()
freqfile.close()
ifile.close()
