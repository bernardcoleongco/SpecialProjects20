import csv

def read_tsv():
	# read tsv and print rows

	tsv_file = open("story.tsv")
	read_tsv = csv.reader(tsv_file, delimiter="\t")

	for row in read_tsv:
	  print(row)

	tsv_file.close()

def read_user_input():
	user_input = input()

def main():
	read_tsv()
	read_user_input()

main()
