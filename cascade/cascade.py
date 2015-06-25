import numpy as np


def independent_cascade(Graph, InitialSet, iterations): 
    Graph = Graph.copy()
    S_1 = np.copy(InitialSet)
    for i in xrange(iterations):
        new_initial_set = list()
        for node in S_1:
            Graph.node[node]['action'] = 1
            # Obtain children Nodes
            children_dict = Graph.succ[node]
            for child,weight in children_dict.items():
                if Graph.node[child]['action'] == 1:
                    continue
                infl = weight['weight']
                # Select 0 or 1 with prob. of 1-infl and infl
                new_action  = np.random.choice(2, p=[1-infl,infl])
                if new_action == 1:
                    new_initial_set.append(child)
                    Graph.node[child]['action'] = new_action
        if len(new_initial_set) == 0:
            break
        else:
            S_1 = np.copy(new_initial_set)
                
    return Graph


def influence_aux(Graph, InitialSet, Iterations, N):
	"""

	"""
	sample = np.zeros(N)
	for i in xrange(N):
		Graph_new = independent_cascade(Graph,InitialSet,Iterations)
		activation_sum = np.sum([1 for node in Graph_new if Graph_new.node[node]['action']])
		sample[i] = activation_sum 
	return sample


def influence(Graph, InitialSet, Iterations, N):
	"""
	"""
	return np.mean(influence_aux(Graph,InitialSet,Iterations,N))

