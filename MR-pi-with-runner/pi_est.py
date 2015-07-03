from mrjob.job import MRJob
import random

class MontecarloPi(MRJob):

    def mapper_init(self):
		self.n_trials = 0
		self.n_hits = 0

    def mapper(self,_,line):
        random.seed(int(line))
        self.n_trials += 1
        x, y = random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)
        if x**2 + y**2 < 1.0: 
            self.n_hits += 1

    def mapper_final(self):
        yield "n_trials",self.n_trials 
        yield "n_hits",self.n_hits 

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MontecarloPi.run()
