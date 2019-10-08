from typing import List


def valid_property(object, property: str):
	if property.startswith('_'):
		return False
	if callable(getattr(object, property)):
		return False
	return True


class JSONable():
	'''Class to define sane json system'''

	def json(self, excludes = set(), includes = set()):
		result = {}
		class_dir = dir(type(self))
		props = [
				x for x in dir(self)
				if valid_property(self, x)
				and x not in class_dir
				and x not in excludes
				or x in includes
			]
		for prop in props:
			result[prop] = getattr(self, prop)
		return result


def check_duplicate_id(ids: List[int]) -> int:
	seen = set()
	for id in ids:
		if id in seen:
			return id
		seen.add(id)
	else:
		return False
