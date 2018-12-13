# Created by: Elias Mote, Ryan Moeller

def main():

	import json
	import sys

	# The total length of the self-avoiding walk we are checking
	k = 4
	#k = input("Enter a value k for the max length of the self-avoiding path: ")

	# The four directions (the language of the DFA).
	# 1: Immediate return
	# 2: Continue in the same direction as the previous step
	# 3: A step in the opposite direction to the second to last step (if there
	# isn't a second to last step, this could be considered a left or right)
	# 4: The remaining direction
	directions = [1, 2, 3, 4]

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
	transfers = [[-1,-1,-1,-1] for _ in range(2)]

	# State lengths
	state_lengths = [0 for _ in range(5)]

	# Path to reach each state
	paths = [[]]

	# The current walk length we are considering
	cur_length = 0

	# Repeat steps 2-4 until the set of untreated states is empty
	# State "w" is a loop and therefore fail state
	while(len(untreated) > 0):

		# Step 2:
		# Choose any untreated state s, remove it from the set. This will be
		# accomplished by removing the first element.
		s = untreated.pop(0)

		cur_length = state_lengths[s]

		#print("Current state = " + str(s))
		#print("State length = " + str(cur_length))
		#print()


		# Step 3:
		# Construct all possible successors of the state by iterating through
		# all 4 possible directions. In each iteration, augment r by a single
		# step in the corresponding direction, leading to an augmented walk a.
		# For l > 1, direction 1 always goes to state "w"

		if(s == 0):
			untreated.append(1)
			state_lengths[1] = 1
			paths.append([[]])
			paths[s+1][0] = [1,2,3,4]
		elif(s == 1):
			paths.append(paths[s] + [2])
			paths.append(paths[s] + [3])
			paths.append(paths[s] + [4])
			untreated.append(2)
			untreated.append(3)
			untreated.append(4)
			state_lengths[2] = 2
			state_lengths[3] = 2
			state_lengths[4] = 2

		for d in range(4):

			# Initialize state 0
			# All 4 directions go to state 1
			if(s == 0):
				transfers[s][d] = 1
				

			# Initialize state 1
			elif(s == 1):
				if(d == 0):
					transfers[s][d] = "w"
				else:
					transfers[s][d] = d+1
				

			elif(cur_length < k):
				if(d == 0):
					transfers.append([-1,-1,-1,-1])
					transfers[s][0] = "w"
				else:
					# Check state a to see if a loop would be formed
					# We'll start with a loop of length 1
					# A loop of length 1 is formed when the last 3 directions
					# were [3,3,3] or [4,4,4] and the current direction is 3
					# or 4, respectively
					# Only perform this check when the current length is at
					# least 3
					if(cur_length >= 3 and d>= 2):

						# Now, check if the path is equivalent to [3,3,3] or
						# [4,4,4]
						if(((paths[s][-3:] == [3,3,3] or paths[s][-3:] == [[1,2,3,4],3,3]) and d == 2)
							or ((paths[s][-3:] == [4,4,4] or paths[s][-3:] == [[1,2,3,4],4,4]) and d == 3)):

							# If so, this path will go to the fail state
							transfers[s][d] = "w"

							# Continue the loop
							continue

					# If t is a state we have not seen so far, put it in the set
					# of untreated states
					t = max(untreated) + 1
					untreated.append(t)

					# Put the transfer from s to t in the set of transfers
					transfers[s][d] = t
					paths.append(paths[s] + [d+1])
					state_lengths.append(-1)
					state_lengths[t] = cur_length + 1


		# Step 4:
		# Put state s into the set of treated states. If the set of untreated
		# states is not empty, go to 2; otherwise, continue to 5
		treated.append(s)

	# The final state is the fail state "w"
	transfers.append(["w","w","w","w"])

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
							["1","1","1","1"],
							["w","1","2","2"],
							["w","1","3","2"],
							["w","1","2","2"],
							["w","w","w","w"]
						],
		"states": [0,1,2,3,4],
		"final": [3],
		"symbols": ["f","l","b","r"],
		"start": 0
	}
	"""
	json_dfa = 	{
					"transitions": transfers,
					"states": treated,
					"final": end_states,
					"symbols": [1,2,3,4],
					"start": start_state
				}
	print("Paths:")
	for p in range(len(paths)):
		print("State " + str(p) + ": " + str(paths[p]))
	print()
	#print("Set of treated states:")
	#print(treated)
	#print()
	print("Set of transfers:")
	for t in transfers:
		print(t)
	#sys.stdout.write(str(json_dfa))
	#sys.stdout.flush()
	#print()

if __name__ == '__main__':
	main()