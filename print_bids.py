'''
PRECONDITION:	YEAR is an integer - the current year.
PRECONDITION:	{YEAR}/silent.csv is a csv file where each row is an item,
				with information about the donor and donation. The order of the
				columns is specified in HEADER. Feel free to change it.
POSTCONDITION:	{YEAR}/servsheets.tex is a Tex file that can be compiled and
				printed into the bid sheets for the Silent Auction.
WARNING:		This script ignores special characters, as there is no easy way
				to convert them to the proper LaTeX commands.
WARNING:		"\^\^" is not valid Latex (needs to not be escaped), but "^" must
				be escaped everywhere else. Odd edge case.
NOTE:			This script should be run once, when all donations are in right
				before the silent auction starts. This script arranges the items
				such that they are easy to print and does NOT make PDFs to be
				viewed digitally. All items should be shared digitally via Google Sheets.
'''

import csv
from helpers import *

ALUMNI_FILTER = False
YEAR = 'SENIOR_2018'
HEADER = ['name', 'title', 'description', 'category', 'starting_bid']
NUM_LINES = 26

with open('{}/senior_auction.csv'.format(YEAR), 'r') as sample:
	readSample = csv.reader(sample, delimiter=',', quotechar='"')

	f = open('{}/servsheets.tex'.format(YEAR),'w')

	f.write('''\
			\\documentclass[11pt]{{article}}
			\\pagestyle{{plain}}
				\\topmargin -.5in \\oddsidemargin 0in \\evensidemargin 0in \\textwidth 6.5in \\textheight 9.5in
			\\setlength{{\\parindent}}{{0in}}
			\\begin{{document}}
		\n'''.format())

	categories = [[],[],[],[],[],[],[]]
	categoryNames = ["Events", "Arts & Crafts", "Lessons & Instruction", "Services", "Food & Drink", "Objects ", "Miscellaneous"]

	header = True # I can't for the life of me figure out a better way to skip the header
	for item in readSample:
		if header:
			header = False
			continue
		idx = categoryNames.index(item[3]) # ** FOR FUTURE DEVELOPERS: Change this index to reflect which column "categories" are in
		categories[idx].append(item)

	for i, category in enumerate(categories):

		category = sorted(category, key=lambda item:item[3].lower()) # sort by title, alphabetically
		for j, row in enumerate(category):
			item = {key:handleLatexChars(val.strip()) for key,val in zip(HEADER,row)} # unpack the row

			# if not item['email']:
			# 	item['email'] = parse_email(item['name'], item['affiliation']) # make sure all the email addresses are present
			# item['starting_bid'] = addDollarSign(item['starting_bid'])
			# if item['num_winners'] in ['', '1']: # specify what the number of winners means
			# 	item['winners'] = "Top bidder"
			# else:
			# 	item['winners'] = "Top {num_winners} bids".format(**item)

			# # Enable Alumni only filter.
			# if ALUMNI_FILTER:
			# 	if 'Alumni' not in interest_for and 'anyone' not in interest_for:
			# 		continue

			# write the important information to the file
			f.write('''\
					\\section*{{{0}.{1} {title}}}
					{name} \\\\
					Starting Bid: {starting_bid} \\\\
					{description} \\\\
					[6ex]
					\\begin{{tabular}}{{c c c}}
						~~~~~~~~~~~~~Name~~~~~~~~~~~~~ & ~~~~~~~~~Bid (\\$)~~~~~~~~~ & ~~~Email Address (if not standard olin.edu)~~~ \\\\
				\n'''.format(i+1, j+1, **item))
			for a in range(NUM_LINES): # print lines for bids
				f.write(' & & \\\\\n\\hline\n')
			f.write('''\
					\\end{{tabular}}
					\\clearpage
				\n'''.format())
			# print >>f, "\\section*{{{0}.{1} {title}}}".format(i+1, j+1, **item) # title
			# print >>f, "{name} ({email}) \\".format(**item) # name
			# print >>f, "Starting Bid: {} \\".format(starting_bid)
			# print >>f, "Winner(s): "
			# if num_winners == 1: 	print >>f, r"Top bidder \\"
			# else: 					print >>f, r"Top {} bids \\".format(num_winners)
			# print >>f, r"{} \\[6ex]".format(description) # description
			# print >>f, r"\begin{tabular}{c c c}"
			# print >>f, r"~~~~~~~~~~~~~Name~~~~~~~~~~~~~ & ~~~~~~~~~Bid (\$)~~~~~~~~~ & ~~~Email Address (if not standard olin.edu)~~~ \\"
			# for a in range(NUM_LINES): # print lines for bids
			# 	print >>f, r" & & \\"
			# 	print >>f, r"\hline"
			# print >>f, r"\end{tabular}"
			# print >>f, r"\clearpage"
	f.write('\\end{document}')
	f.close()
