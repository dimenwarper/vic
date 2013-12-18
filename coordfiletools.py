
def get_coord_tuple(line, chrcol, startcol, endcol, delim):
    fields = line.strip().split(delim)
    return (fields[chrcol].replace('chr', ''), int(fields[startcol]), int(fields[endcol]))

def get_coords(lines, chrcol=0, startcol=1, endcol=2, delim='\t'):
    res = []
    for line in lines:
	res.append(get_coord_tuple(line, chrcol, startcol, endcol, delim))
    return res

def index_coords(lines, chrcol=0, startcol=1, endcol=2, delim='\t'):
    res = {}
    for line in lines:
	res[get_coord_tuple(line, chrcol, startcol, endcol, delim)] = line
    return res
    
def perform_on_find(sourcecoords, targetlines, function, funargs=[], chrcol=0, startcol=1, endcol=2, delim='\t'):
    res = {}
    index = index_coords(targetlines, chrcol=chrcol, startcol=startcol, endcol=endcol,  delim=delim)
    for coords in sourcecoords:
	if coords in index:
	    if len(funargs) > 0:
		res[coords] = function(index[coords], funargs)
	    else:
		res[coords] = function(index[coords])
    return res

