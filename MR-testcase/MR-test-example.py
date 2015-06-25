try:
	import unittest2 as unittest
except ImportError:
	import unittest

from StringIO import StringIO

from mrjob.job import MRJob


class MRInitJob(MRJob):

	def __init__(self, *args, **kwargs):
		super(MRInitJob, self).__init__(*args, **kwargs)
		self.sum_amount = 0
		self.multiplier = 0
		self.combiner_multiplier = 1

	def mapper_init(self):
		self.sum_amount += 10

	def mapper(self, key, value):
		yield(None, self.sum_amount)

	def reducer_init(self):
		self.multiplier += 10

	def reducer(self, key, values):
		yield(None, sum(values) * self.multiplier)

	def combiner_init(self):
		self.combiner_multiplier = 2

	def combiner(self, key, values):
		yield(None, sum(values) * self.combiner_multiplier)


class MRInitTestCase(unittest.TestCase):

	def test_mapper(self):
		j = MRInitJob()
		j.mapper_init()
		self.assertEqual(j.mapper(None, None).next(), (None, j.sum_amount))

	def test_init_funcs(self):
		num_inputs = 2
		stdin = StringIO("x\n"*num_inputs)
		mr_job = MRInitJob(['-r', 'inline', '--no-conf', '-'])
		mr_job.sandbox(stdin=stdin)

		results = []
		with mr_job.make_runner() as runner:
			runner.run()
			for line in runner.stream_output():
				key, value = mr_job.parse_output_line(line)
				results.append(value)

		self.assertEqual(results[0], num_inputs * 10 * 10 * 2)


if __name__ == "__main__":
	unittest.main()