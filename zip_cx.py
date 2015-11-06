import sys
import os
import zipfile

# modified from http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
def zipdir(path, ziph):
    # ziph is zipfile handle
    path_len = len( os.path.dirname(path) )

    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(root[path_len:], file))

def zip_create(frm, to):
    ziph = zipfile.ZipFile(to, 'w')
    if os.path.isdir(frm):
    	zipdir(frm, ziph)
    elif os.path.isfile(frm):
    	head, tail = os.path.split(frm)
    	ziph.write(frm, tail)
    ziph.close()

def zip_extract(frm):
    with zipfile.ZipFile(frm, "r") as ziph:
        ziph.extractall()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('need a argument')
		exit(0)

	ch = raw_input("(z)ip or (u)nzip: ")
	if ch == 'z':
		zip_create(sys.argv[1], 'test.zip')
	elif ch == 'u':
		zip_extract(sys.argv[1])
	else:
		print('bad choice')