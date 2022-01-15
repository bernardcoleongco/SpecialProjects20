import csv

def read_tsv():
	# read tsv and print rows

	tsv_file = open("story.tsv")
	read_tsv = csv.reader(tsv_file, delimiter="\t")

	for row in read_tsv:
	  print(row)

	tsv_file.close()

def main():
	read_tsv()

main()
