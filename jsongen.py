import json
import sys

from random import *
from time import time
from string import ascii_letters

HELP = """Usage: python3 jsongen.py (options) <template-file> <repeat> <output-file>

Options can be:
	-h, --help              Show help and exit
	--version               Show version and exit
	--verbose               Show advanced output

	-t                      Output elapsed time

	-o <str>                Change the function operator (Default is '~')
	--hashlen <int>         Change length of hash (Default is 40)
	--now <float>           Change current timestamt (Default is current time)
	--min-pw <int>          Change minimum password length (Default is 8)
	--max-pw <int>          Change maximum password length (Default is 16)
	--min-int <int>         Change minimum integer (Default is 0)
	--max-int <int>         Change maximum integer (Default is 65535)
	--min-float <float>     Change minimum float (Default is 0.0)
	--max-float <float>     Change maximum float (Default is 65535.0)"""

VERSION = "JSONGen - Version 0.2"

t0 = time()

def checkArgOption(arg, desc, type_, default):
	if arg in options:  # Change function operator
		try:
			return type_(options[options.index(arg) + 1])

		except (IndexError, ValueError):
			print("Usage of '"+arg+"' ("+str(default)+"): "+arg+" <"+desc+" ("+str(type_)[8:-2]+")>")
			sys.exit()

	else:
		return type_(default)

try:
	# Removing 'jsongen.py'
	sys.argv = sys.argv[1:]

	if "--help" in sys.argv or "-h" in sys.argv:
		print(HELP)
		sys.exit()

	elif "--version" in sys.argv:
		print(VERSION)
		sys.exit()

	options = sys.argv[:-3]
	tempFilePath = sys.argv[-3]
	repeat = int(sys.argv[-2])
	outputFilePath = sys.argv[-1]

	# variable = checkArgOption(argument, description, type, defaultValue)
	funcOp = checkArgOption("-o", "function-operator", str, "~")
	hashLength = checkArgOption("--hashlen", "hash-length", int, 40)
	nowTime = checkArgOption("--now", "timestamp-now", float, time())

	minPW = checkArgOption("--min-pw", "min-password-length", int, 8)
	maxPW = checkArgOption("--max-pw", "max-password-length", int, 16)
	minInt = checkArgOption("--min-int", "min-int", int, 0)
	maxInt = checkArgOption("--max-int", "max-int", int, 65535)
	minFloat = checkArgOption("--min-float", "min-float", float, 0.0)
	maxFloat = checkArgOption("--max-float", "max-float", float, 65535.0)

	if "--verbose" in sys.argv:
		verbose = True
	else:
		verbose = False

	if "-t" in sys.argv:
		showElapsedTime = True
	else:
		showElapsedTime = False

except (IndexError, ValueError):
	print("Usage: python3 jsongen.py (options) <template-file> <repeat> <output-file>")
	sys.exit()

def printVerbose(text):
	if verbose:
		print("[Verbose]    " + text)

printVerbose("Defining gen-functions.")
class gen:
	def hash():
		h = ""
		for a in range(hashLength):
			h += choice("0123456789abcdef")

		return h

	def password():
		p = ""
		for a in range(randint(minPW, maxPW)):
			p += choice(ascii_letters)

		return p

	def username():
		names = [
			"rick", "morty",
			"homer", "marge", "lisa", "bart", "maggi",
			"bob", "linda", "louise", "tina", "gene",
			"cartman", "kenny", "kyle", "stan", "butters"
		]

		r = randint(0, 1)

		# Create basic name
		if r == 0:
			u = choice(names)
		elif r == 1:
			u = choice(names) + choice([".", "-", "_"]) + choice(names)

		# Add "x"
		if randint(0, 3) == 3:
			u = list(u)
			u[randint(0, len(u)-1)] = "x"
			u = "".join(u)

		# Add prefix
		if randint(0, 4) == 4:
			u = choice(["iam", "the", "nice", "bad"]) + choice([".", "-", "_", ""]) + u

		# Add underscores
		if randint(0, 3) == 3:
			u = "_" + u + "_"

		# Add numbers
		if randint(0, 1) == 1:
			for a in range(randint(1, 4)):
				u += str(randint(0, 9))

		return u

	def int_():
		return str(randint(minInt, maxInt))

	def float_():
		return str(uniform(minFloat, maxFloat))

	def now():
		return str(int(nowTime))

	def fnow():
		return str(nowTime)

	def timestamp():
		return str(randint(0, int(nowTime)))

	def ftimestamp():
		return str(uniform(0, nowTime))


def readTemplate(path):
	try:
		with open(path) as templateFile:
			tj = json.loads(templateFile.read())

	except json.decoder.JSONDecodeError:
		print("Error: Can't read template-file. Check syntax.")
		sys.exit()

	return tj

printVerbose("Connecting functions.")

functions = {
	"username": gen.username,
	"password": gen.password,
	"hash": gen.hash,
	"int": gen.int_,
	"float": gen.float_,
	"now": gen.now,
	"fnow": gen.fnow,
	"timestamp": gen.timestamp,
	"ftimestamp": gen.ftimestamp,
}

jsonObject = []

printVerbose("Reading template.")
singleObject = readTemplate(tempFilePath)

printVerbose("Creating object.")
printVerbose("  => Length: " + str(repeat))

printVerbose("Using functions.")
for a in range(repeat):
	soString = json.dumps(singleObject)
	for func in functions:
		while funcOp + func + funcOp in soString:
			soString = soString.replace(funcOp + func + funcOp, functions[func](), 1)

	jsonObject.append(json.loads(soString))

printVerbose("Writing.")
with open(outputFilePath, "w+") as of:
	jsonString = json.dumps(jsonObject, indent=4, sort_keys=True)
	of.write(jsonString)

elapsedTime = round(time() - t0, 5)
if showElapsedTime:
	print("Generating", str(repeat), "object" if repeat == 1 else "objects", "took", elapsedTime, "second" if elapsedTime == 1 else "seconds")
