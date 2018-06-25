from common import JSONable

class System(JSONable):
	def __init__(self):
		self.projects = []
	def json(self):
		result = super().json()
		result['type'] = 'System'
		return result
