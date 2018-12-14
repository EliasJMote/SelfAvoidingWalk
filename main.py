# Created by: Elias Mote, Ryan Moeller
import numpy as np

# This function will check for and report any loops
def check_for_loops(s, d, paths, transfers):
	augmented_path = paths[s] + [d]

	# Check state to see if a loop would be formed
	# A loop can be a rectangle or a square, or it can be more complex.
	# However, regardless of the loop's form, the loop much have at least 3 more 3's than 4's or 3 more
	# 4's than 3's. This is the only way for a loop to be formed.
	# First, check how many 3's and 4's are in the list.
	num_3 = augmented_path.count(3)
	num_4 = augmented_path.count(4)

	# Compare them. If the requirement is not met, simply return false. This will speed things up by
	# eliminating a lot of cases.
	if(not (num_3 >= num_4 + 3) and not (num_4 >= num_3 + 3)):
		return False

	"""

	# Squares are the easiest to check for, so we'll check them first.
	# A square loop is a n x n loop. Length of the square is determined by the number of consecutive 1's.
	# A square of length 1 has the pattern [3,3,3,3] or [4,4,4,4] at the end of the path.
	if((augmented_path == [3,3,3,3] or augmented_path == [[1,2,3,4],3,3,3])
		or (augmented_path == [4,4,4,4] or augmented_path == [[1,2,3,4],4,4,4])):

		# If so, this path will go to the fail state
		transfers[s][d-1] = "w"

		return True

	# Square side length 2: [2,2,3,2,3,2,3,2]
	# Square side length 3: [2,2,2,4,2,2,4,2,2,4,2,2]
	# etc.
	# Walk the path backwards, checking for this type of pattern until the number of 2's at the end is
	# exhausted.
	chain_len = 0
	for i in range(len(augmented_path)):
		if(not (augmented_path[:-i] == 2)):
			break
		chain_len += 1

	# Check the square with chain length
	square_3 = []
	square
	if()

	"""

	# Generate the path as a collection of (x,y) coordinates
	coords = []
	#cur_pos = (0,0)
	cur_pos = np.array([0,0])
	for i in range(len(augmented_path)):
		direction = None
		if(i == 1):
			direction = "right"
			#cur_pos = tuple(map(sum, zip(cur_pos, (1,0))))
			
		else:

			"""
			if(d == 2):
				if(direction == "right"):
					cur_pos += np.array([1,0])
					#cur_pos = tuple(map(sum, zip(cur_pos, (1,0))))
				elif(direction == "up"):
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,1))))
					cur_pos += np.array([0,1])
				elif(direction == "left"):
					#cur_pos = tuple(map(sum, zip(cur_pos, (-1,0))))
					cur_pos += np.array([-1,0])
				elif(direction == "down"):
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,-1))))
					cur_pos += np.array([0,-1])
			"""
			if(d == 3):
				if(direction == "right"):
					direction = "up"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,1))))
					#cur_pos += np.array([0,1])
				elif(direction == "up"):
					direction = "left"
					#cur_pos = tuple(map(sum, zip(cur_pos, (-1,0))))
					#cur_pos += np.array([-1,0])
				elif(direction == "left"):
					direction = "down"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,-1))))
					#cur_pos += np.array([0,-1])
				elif(direction == "down"):
					direction = "right"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,1))))
					#cur_pos += np.array([1,0])
			elif(d == 4):
				if(direction == "right"):
					direction = "down"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,-1))))
				elif(direction == "down"):
					direction = "left"
					#cur_pos = tuple(map(sum, zip(cur_pos, (-1,0))))
				elif(direction == "left"):
					direction = "up"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,1))))
				elif(direction == "up"):
					direction = "right"
					#cur_pos = tuple(map(sum, zip(cur_pos, (0,1))))

		if(direction == "right"):
			cur_pos += np.array([1,0])
		elif(direction == "down"):
			cur_pos += np.array([0,-1])
		elif(direction == "left"):
			cur_pos += np.array([-1,0])
		elif(direction == "up"):
			cur_pos += np.array([0,1])


		coords.append(cur_pos)

	# Walk the list, putting coordinates we've seen into a list. If we find a coordinate we've seen already,
	# return true as a loop has been found.
	# Else, return false.
	coords_seen = []
	for c in coords:
		if(coords_seen.count(c) >= 1):
			return True
		coords_seen.append(c)

	return False


def main():

	import json
	import sys
	from count import count

	# The total length of the self-avoiding walk we are checking
	#k = 3
	k = int(input("Enter a value k for the max length of the self-avoiding path: "))

	# The four directions (the language of the DFA).
	# 1: Immediate return (loop on itself)
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

		for d in range(1,5):

			# Initialize state 0
			# All 4 directions go to state 1
			if(s == 0):
				transfers[s][d-1] = 1
				

			# Initialize state 1
			elif(s == 1):
				if(d == 1):
					transfers[s][d-1] = "w"
				else:
					transfers[s][d-1] = d
				

			elif(cur_length < k):
				if(d == 1):
					transfers.append([-1,-1,-1,-1])
					transfers[s][0] = "w"
				else:
					
					# Only perform this check when the current length is at least 3 and the direction is 2 
					# through 4 (direction 1 always leads to a loop)
					if(cur_length >= 3 and d>= 2):


						# Check for loops and continue if any are found
						if(check_for_loops(s, d, paths, transfers)):
							transfers[s][d-1] = "w"
							continue

					# If t is a state we have not seen so far, put it in the set
					# of untreated states
					t = max(untreated) + 1
					untreated.append(t)

					# Put the transfer from s to t in the set of transfers
					transfers[s][d-1] = t
					paths.append(paths[s] + [d])
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

	treated.append(len(treated))

	for i in range(len(state_lengths)):
		if(state_lengths[i] == k):
			end_states.append(i)

	for s in end_states:
		transfers.append(["w","w","w","w"]) 

	#transfers.append(["w","w","w","w"])

	
	for j in range(len(transfers)):
		for k in range(4):
			if(transfers[j][k] == "w"):
				transfers[j][k] = len(treated) - 1




	json_dfa = 	{
					"transitions": transfers,
					"states": treated,
					"final": end_states,
					"symbols": [1,2,3,4],
					"start": start_state
				}
	#print("Paths:")
	#for p in range(len(paths)):
		#print("State " + str(p) + ": " + str(paths[p]))
	#print()
	#print("Set of treated states:")
	#print(treated)
	#print()
	#print("Set of transfers:")
	#for t in transfers:
		#print(t)
	print(json.dumps(json_dfa))
	#sys.stdout.write(str(json.dumps(json_dfa)))
	#sys.stdout.flush()
	#print()

	#count(json_dfa, k)

if __name__ == '__main__':
	main()