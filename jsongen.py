import json
import sys

from random import *
from time import time
from string import ascii_letters

HELP = """Usage: python3 jsongen.py (options) <template-file> <repeat> <output-file>

Options can be:
	-h, --help			Show help and exit
	--version			Show version and exit

	-o '...'			Change the function operator (Default is '~')
	--verbose			Show advanced output"""

VERSION = "JSONGen - Version 0.1"

try:
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

	if "-o" in options:  # Change function operator
		try:
			funcOp = options[options.index("-o") + 1]
		except IndexError:
			print("Usage of '-o': -o <function-operator>")
	else:
		funcOp = "~"

	if "--verbose" in sys.argv:
		verbose = True
	else:
		verbose = False

except (IndexError, ValueError):
	print("Usage: python3 jsongen.py (options) <template-file> <repeat> <output-file>")
	sys.exit()

def printVerbose(text):
	if verbose:
		print("[Verbose]    " + text)

printVerbose("Defining gen-functions.")
class gen:
	def hash(length=40):
		h = ""
		for a in range(length):
			h += choice("0123456789abcdef")

		return h

	def password():
		p = ""
		for a in range(randint(8, 16)):
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

	def int_(min=0, max=65535):
		return str(randint(min, max))

	def float_(min=0, max=65535):
		return str(uniform(min, max))

	def now():
		return str(int(time()))

	def fnow():
		return str(time())

	def timestamp():
		return str(randint(0, int(time())))

	def ftimestamp():
		return str(uniform(0, time()))


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
for a in range(repeat):
	jsonObject.append(singleObject)

printVerbose("Writing.")

with open(outputFilePath, "w+") as of:
	jsonString = json.dumps(jsonObject, indent=4, sort_keys=True)
	for func in functions:
		while funcOp + func + funcOp in jsonString:
			jsonString = jsonString.replace(funcOp + func + funcOp, functions[func](), 1)

	of.write(jsonString)
