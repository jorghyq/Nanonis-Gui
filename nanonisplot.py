# files that hold nanonis plotting

f = open("Follow Me_Bias Spectroscopy238.dat","r")
header = {}

s1 = f.readline()
if s1.split("\t")[0] == 'Experiment':
	header['type'] = s1.split("\t")[1]
    print header['type']
else:
	print 'Not a correct type!'
# read the header
skip = 1
skip = skip + 1
print skip
line  = f.readline()
items = line.split("\t")
# if this line is not a void line
if len(items) == 3:
    header[items[0]] = items[1]
    print items[0]+items[1]
elif items[0] == '[DATA]':
    print items[0]
else:
	pass
