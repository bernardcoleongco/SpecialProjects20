import csv
import time

prev_choices_dict = {}
next_choices_dict = {}
stories = {}

def clean_data(choice):
	# clean up/standardize tsv data
	if '0' not in choice:
		choice = '0.' + choice

	return choice

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
			choice = clean_data(choice)
			prev_choices_dict[choice] = story

		for choice in next_choices.split(','):
			choice = clean_data(choice)
			next_choices_dict[story] = choice

		stories[story] = prompt
	
	tsv_file.close()

def error_state(msg):
	print(msg)
	
	# delay so that the user has time to digest the situation
	# before returning to the story flow so they can try again
	time.sleep(1)

def validation(user_selection, choices):
	prev_choice = choices
	choices += "." + user_selection
	if choices not in prev_choices_dict.keys():
		error_state(user_selection + " is an invalid number, please try again.\n")
		choices = prev_choice

	return choices

def read_user_input():
	choices = '0'
	prompt = None
	the_end = 'The end.\n'
	ending = "Press any key to exit."

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
				choices = validation(user_selection, choices)
			elif user_selection == 'q' or prompt == the_end + ending:
				print("Thank you for playing!")
				exit()
			else:
				error_state(user_selection + " is an invalid choice, please try again.\n")

def display_instructions():
	print("Your adventure begins! Select the number that represents your choice, but choose wisely if you hope to survive... Press 'q' to quit at any time.\n")
	
	# delay so that the user has time to digest the situation
	# before launching into the story flow
	time.sleep(1)

def main():
	read_tsv()
	display_instructions()
	read_user_input()

main()
