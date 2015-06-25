import json
import time

import numpy as np
import networkx as nx

from mrjob.job import MRJob
from networkx.readwrite import json_graph

from cascade.cascade import independent_cascade


class MRInfluence(MRJob):

	def __init__(self, *args, **kwargs):
		super(MRInfluence, self).__init__(*args, **kwargs)
		
		with open(self.options.graph_file, "r") as graph_data:
		    graph_data = json.load(graph_data)
		    self.graph = json_graph.node_link_graph(graph_data)
		 
		self.k = int(self.options.num_init)
		self.t = int(self.options.periods)
		self.initial_nodes = list(np.random.choice(self.graph.nodes(),self.k))


	def configure_options(self):
		super(MRInfluence, self).configure_options()

		self.add_file_option('--graph_file',
			help="Location of json graph file")

		self.add_passthrough_option('--num_init', 
			help="Number of initial nodes")

		self.add_passthrough_option('--periods', default=10,
			help="Number of cascading periods")


	def mapper(self,_,line):
		np.random.seed(int(line))
		new_graph = independent_cascade(self.graph, self.initial_nodes, self.t)
		I = np.sum([new_graph.node[node]['action'] 
			for node in new_graph.nodes_iter()])
		yield "|I(S_1)|", I


	def reducer(self,key,values):
		I_list = list(values)
		yield "f(S_1)", np.mean(I_list)


if __name__ == '__main__':
	start = time.time()
	MRInfluence.run()
	end = time.time() - start
	print end