class Stepwise_Result(object):
	def __init__(self, description, param_inclusion,regression_result, adjusted_rs, vif_result):
		self.description = description
		self.param_inclusion = param_inclusion
		self.regression_result = regression_result
		self.adjusted_rs = adjusted_rs
		self.vif_result = [float(int(x*100)/100.0) for x in vif_result]

	def print_object(self):
		print "**************************"
		print str(self.description)
		print 'matrix of parameter inclusion: ' + str(self.param_inclusion)
		print 'adjusted r squared: ' + str(self.adjusted_rs)
		print 'collinearity score: ' + str(self.vif_result)