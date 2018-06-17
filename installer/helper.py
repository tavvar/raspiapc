import sys, json

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

filename = sys.argv[1]
url = sys.argv[2]
id = sys.argv[3]
im = sys.argv[4]

fo = open(filename, 'w+')
fo.write(json.dumps({'id':id,'intervall':im,'url':url}))