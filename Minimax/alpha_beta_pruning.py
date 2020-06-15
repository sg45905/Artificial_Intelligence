import math

# define the upper and lower limit
# limit - any number large enough to be considered as infinity for the values at the nodes
MAX, MIN = 1000, -1000

# function to prune the tree  - alpha beta pruning
def alphaBeta(current,currentNode,maxTurn,targetNodes,alpha,beta,branch):
	# if current pointer at the last depth
	if current == depth:
		return targetNodes[currentNode]
    
	# if its max's turn
	if maxTurn:
		# suppose the lower limit to be the best
		best = MIN

		# for all branches at a given node
		for i in range(branch):
			val = alphaBeta(current + 1,currentNode * branch + i,False,targetNodes,alpha,beta,branch)
			
			# update best and alpha
			best = max(best,val)
			alpha = max(alpha,best)

			# condition for pruning - beta at upper depth < alpha at current depth - prune tree below the current depth
			if beta <= alpha:
				break
		return best

	# if its min's turn
	else:
		# suppose the upper limit to be the best
		best = MAX

		# for all branches at a given node
		for i in range(branch):
			val = alphaBeta(current + 1,currentNode * branch + i,True,targetNodes,alpha,beta,branch)

			# updtae best and beta
			best = min(best,val)
			beta = min(beta,best)

			# condition for pruning - beta at upper depth < alpha at current depth - prune tree below the current depth
			if beta <= alpha:
				break
		return best

# main functionof the program - call alphabeta
if __name__ == "__main__":
	targetNodes = []

	# take number of nodes and branching factor as input
	noNodes = int(input("Enter Number of target nodes: "))
	branch = int(input("Enter the Branching Factor: "))
	
	# calculate depth of tree
	depth = math.log(noNodes,branch)

	# if the calculated depth has nothing after the decimal
	if depth == int(depth):
		print("Enter the Target Nodes: ")
		
		# transfer all nodes to target node
		for i in range(noNodes):
			targetNodes.append(int(input()))
		
		# input whose turn is first
		maxTurn = bool(input("Write 'True' for Player's turn and 'False' for Computer's turn: "))
		
		# print the result
		print("The optimal value is : ", end = "")
		print(alphaBeta(0,0,maxTurn,targetNodes,MIN,MAX,branch))
	
	# if calculated depth has nothing after the decimal - a complete tree cannot be constructed
	else:
		print("Cannot construct a complete tree out of it")
