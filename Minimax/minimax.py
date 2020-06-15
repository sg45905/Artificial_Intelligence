import math

# the minimax function
def minMax(current,currentNode,maxTurn,targetNodes,depth,branch):
	# if current pointer at the last depth
	if current == depth:
		return targetNodes[currentNode]
    
	# if its max's turn
	if maxTurn:
		maxTurn = False
		l = []
		# for all the branches at a given node
		for x in range(branch):
			l.append(minMax(current + 1,currentNode * branch + (x),maxTurn,targetNodes,depth,branch))
		return max(l)

	# if it min's turn
	else:
		maxTurn = True
		l = []
		# for all the branches at a given node
		for x in range(branch):
			l.append(minMax(current + 1,currentNode * branch + (x),maxTurn,targetNodes,depth,branch))
		return min(l)

# main function of the program - calss minimax
if __name__ == "__main__":
	targetNodes = []
	
	# take nodes as input and branching factor as input
	noNodes = int(input("Enter Number of target nodes: "))
	branch = int(input("Enter the Branching Factor: "))
	
	# calculate depth of the tree
	depth = math.log(noNodes,branch)

	# if the calculated depth has nothing after decimal run the program
	if depth == int(depth):
		print("Enter the Target Nodes: ")
		
		# transfer all nodes to target nodes
		for i in range(noNodes):
			targetNodes.append(int(input()))
		
		# input whose turn is first
		maxTurn = bool(input("Write 'True' for Player's turn and 'False' for Computer's turn: "))
		
		# print the result
		print("The optimal value is : ", end = "")
		print(minMax(0,0,maxTurn,targetNodes,depth,branch))
	
	# if calculated depth has something after decimal - a complete tree cannot be constructed
	else:
		print("Cannot construct a complete tree out of it")
