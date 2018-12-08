# Created by: Elias Mote, Ryan Moeller

def main():

	import json
	import sys

	# The total length of the self-avoiding walk we are checking
	length = 1

	# The four directions (the language of the DFA) are: right, up, left, down
	directions = ["r", "u", "l", "d"]

	# The start state is 0
	start_state = 0

	# End states are all the states excluding w, which is the state reached
	# if the walk terminates in a loop of any kind.
	end_states = []

	# Step 1:
	# Initialize a set of untreated states with state 0 as the only element
	untreated = [0]

	# Initialize an empty set of treated states
	treated = []

	# Initialize an empty set of transfers
	transfers = []

	# The current walk length we are considering
	#cur_length = 1

	# Repeat steps 2-4 until the set of untreated states is empty
	while(len(untreated) > 0):

		# Step 2:
		# Choose any untreated state s, remove it from the set. This will be
		# accomplished by popping the last element.
		s = untreated.pop()

		# Step 3:
		# Construct all possible successors of the state by iterating through
		# all 4 possible directions. In each iteration, augment r by a single
		# step in the corresponding direction, leading to an augmented walk a.
		for d in range(4):


			# If t is a state we have not seen so far, put it in the set of
			# untreated states
			#if t not in treated and not in untreated:
				#untreated.append(t)

			# Put the transfer from s to t in the set of transfers


		# Step 4:
		# Put state s into the set of treated states. If the set of untreated states
		# is not empty, go to 2; otherwise, continue to 5
		treated.append(s)

	# Step 5:
	# We have now collected all necessary states in the set of treated states
	# and all transfers in the set of transfers, thus the automaton is built.
	# As a result, the DFA can now be sent for processing to have its length
	# counted.
	# Send a JSON-formatted DFA to stdout for further processing
	# Format:
	"""
	{
		"transitions":	[
							[1,1,1,1],
							[2,2,2,2],
							[3,3,3,3],
							[4,4,4,4],
							[4,4,4,4]
						],
		"states":[0,1,2,3,4],
		"final":[4],
		"symbols":["a","b","c","d"],
		"start":0
	}
	"""

	json_dfa = 	{
					"transitions": transfers,
					"states": treated,
					"final": end_states,
					"symbols": ["r", "u", "l", "d"],
					"start": start_state
				}
	sys.stdout.write(str(json_dfa))
	sys.stdout.flush()
	print()

if __name__ == '__main__':
	main()