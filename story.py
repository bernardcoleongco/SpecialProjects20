import csv
import time

prev_choices_dict = {}
next_choices_dict = {}
stories = {}

def read_tsv():
	# read tsv and print rows

	tsv_file = open("story.tsv")
	read_tsv = csv.reader(tsv_file, delimiter="\t")

	for row in read_tsv:
	  prev_choices = row[0]
	  story = row[1]
	  prompt = row[2]
	  next_choices = row[3]
	  for choice in prev_choices.split(','):
	  	if '0' not in choice:
	  		choice = '0.' + choice
	  	prev_choices_dict[choice] = story
	  for choice in next_choices.split(','):
	  	next_choices_dict[story] = choice
	  stories[story] = prompt

	tsv_file.close()

def read_user_input():
	choices = '0'
	prompt = None
	the_end = 'The end.\n'
	ending = "Press any key to exit."
	error_message = "\nInvalid input, please try again.\n"

	while prompt != the_end + ending:
		story = prev_choices_dict[choices]
		prompt = stories[story]+"\n"
		print(story)
		if prompt == the_end:
			prompt += ending
		if prompt == 'n/a\n':
			choices = next_choices_dict[story]
		else:
			user_selection = input(prompt)
			if user_selection.isdigit():
				prev_choice = choices
				choices += "." + user_selection
				if choices not in prev_choices_dict.keys():
					print(error_message)
					choices = prev_choice
					time.sleep(1)
			elif user_selection == 'q':
				print("Thank you for playing!")
				exit()
			else:
				print(error_message)
				time.sleep(1)

def main():
	read_tsv()
	read_user_input()

main()
