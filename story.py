import csv

prev_choices_dict = {}
next_choices_dict = {}
stories = {}

def read_tsv():
	# read tsv and store rows

	tsv_file = open("story.tsv")
	read_tsv = csv.reader(tsv_file, delimiter="\t")

	for row in read_tsv:
	  prev_choices = row[0]
	  story = row[1]
	  prompt = row[2]
	  next_choices = row[3]

	  for choice in prev_choices.split(','):
	  	# clean up/standardize tsv data
		if '0' not in choice:
	  		choice = '0.' + choice
	  	
		prev_choices_dict[choice] = story
	  
	  for choice in next_choices.split(','):
	  	next_choices_dict[story] = choice

	  stories[story] = prompt
	
	tsv_file.close()

def read_user_input():
	user_input = input()

def main():
	read_tsv()
	read_user_input()

main()
