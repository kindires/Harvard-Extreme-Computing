#!/usr/bin/env python


import numpy as np

from mrjob.job import MRJob



class MR_estimate_Pi(MRJob):

	def mapper(self, _, line):
		np.random.seed(int(line))

		hit_counter = 0

		for i in xrange(100):
			x = np.random.random()
			y = np.random.random()
			hit_counter += (x**2 + y**2 <= 1.0)

		yield "Pi", hit_counter

	def reducer(self, key, value):
		# yield key, list(value)
		
		hit_list = list(value)
		
		yield key, ( 4 * np.sum(hit_list) / (100.0 * len(hit_list)) )


if __name__ == '__main__' :
	MR_estimate_Pi().run()

