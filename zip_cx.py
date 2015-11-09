import sys
import os
import zipfile

# modified from http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
def write_zipdir(path, ziph):
    # ziph is zipfile handle
    path_len = len( os.path.dirname(path) )

    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(root[path_len:], file))
def write_zipfile(path, filename, ziph):
    ziph.write(path, filename)

def zip_create(frm, to=None):
    head, tail = os.path.split(frm)
    dst = to if to is not None else tail+'.zip'
    print tail
	
    ziph = zipfile.ZipFile(dst, 'w')
	
    if os.path.isdir(frm):
    	write_zipdir(frm, ziph)
    elif os.path.isfile(frm):
    	write_zipfile(frm, tail, ziph)
    else:
        raise ValueError
    ziph.close()

def zip_extract(frm, to=None, pwd=None):
    with zipfile.ZipFile(frm, "r") as ziph:
        ziph.extractall(path=to, pwd=pwd)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('need a argument')
		exit(0)

	ch = raw_input("(z)ip or (u)nzip: ")
	if ch == 'z':
		zip_create(sys.argv[1])
	elif ch == 'u':
		zip_extract(sys.argv[1])
	else:
		print('bad choice')