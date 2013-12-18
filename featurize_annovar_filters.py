from coordfiletools import *
import argparse
import os

parser = argparse.ArgumentParser(description='Convert a set of annovar filter scores into features')
parser.add_argument('inputfilename', type=str, help='The filename with chromosome coordinates')
parser.add_argument('outputfilename', type=str, help='The output filename')
parser.add_argument('filter_dir', type=str, help='The directory containing the annovar filter files')
parser.add_argument('--chrcol', type=int, default=0, help='The chromosome column in the input file')
parser.add_argument('--startcol', type=int, default=1, help='The start coordinate column in the input file')
parser.add_argument('--endcol', type=int, default=2, help='The end coordinate column in the input file')
#parser.add_argument('--regioncol', type=int, default=3, help='The region column in the input file')

args = parser.parse_args()
infile = open(args.inputfilename)
outfile = open(args.outputfilename, 'w')
headerfile = open(args.inputfilename+'.headers', 'w')
filterfiles = [open(args.filter_dir + f) for f in os.listdir(args.filter_dir)]

def featurize(sourcecoords, filterfile, threshold):
    features = []
    def filterfun(line, args):
        if 'Score' in line:
	    score = line.strip().split('\t')[1].split(';')[0].replace('Score=','')
	    score = int(score)
	    if score >= args[0]:
		return 1
	    else:
		return 0
	else:
	    return 1
    lines = filterfile.readlines()
    partial_res = perform_on_find(sourcecoords, lines, filterfun, funargs=[threshold], chrcol=2, startcol=3, endcol=4)
    for coords in sourcecoords:
	if coords in partial_res:
	    features.append(partial_res[coords])
	else:
	    features.append(0)
    header = lines[0].strip().split('\t')[0]
    return header, features

featurelist = []
inlines = [l for l in infile.readlines() if l[0] != '#']
coords = get_coords(inlines, chrcol=args.chrcol, startcol=args.startcol, endcol=args.endcol)
for filterfile in filterfiles:
    header, features = featurize(coords, filterfile, 500)
    headerfile.write('\t%s' % header)
    featurelist.append(features)

for i, line in enumerate(inlines):
    featoutput = ''
    for f in featurelist:
	featoutput += '\t%s' % f[i]
    outfile.write(line.strip() + featoutput + '\n')

outfile.close()
infile.close()
for f in filterfiles:
    f.close()
