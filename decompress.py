#! user/bin/env python
# -*- encoding: utf-8 -*-

import zipfile, rarfile
import sys

def extract_zip(zFile, password):
	try:
		zFile.extractall(pwd=password.encode('cp850','replace'))
		return password
	except:
		return None

def extract_rar(rFile, password):
	try:
		rFile.setpassword(password)
		rFile.extractall(pwd=password)
		return password
	except:
		return None

def error(argv):
	print("Error: fichero {0} no encontrado".format(argv))

def extention(file):
	f = file.split(".")
	return f[len(f)-1]

def main(argv):

	is_zip = False
	success_full = False

	if len(argv) <= 1:
		print("usage: <python> decompress.py <name.(zip or rar)> <name_dic.txt>")
		sys.exit(1)
	try:
		file = argv[1]
		if extention(file) == "zip":
			compressed_file = zipfile.ZipFile(file)
			is_zip = True
		else:
			compressed_file = rarfile.RarFile(file)
	except:
		error(argv[1])
		sys.exit(1)

	try:
		pwdFile = open(argv[2])
	except:
		error(argv[2])
		compressed_file.close()
		sys.exit(1)

	linea = "NULL"

	while linea != "":
		linea = pwdFile.readline()
		pwd = linea.strip("\n")

		if is_zip:
			if extract_zip(compressed_file, pwd):
				print("\n\nPassword encontrado: {0}".format(pwd))
				success_full = True
		else:
			if extract_rar(compressed_file, pwd):
				print("\n\nPassword encontrado: {0}\n\n".format(pwd))
				success_full = True

		if success_full:
			compressed_file.close()
			pwdFile.close()

			sys.exit(0)

		print("comprobando: {0}".format(pwd))


if __name__ == '__main__':
	main(sys.argv)
