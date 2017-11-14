def timefunc(func):
	def inner(*args, **kwargs):
		start = timer()
		results = func(*args, **kwards)
		end = timer()
		message = '{} took {} seconds'.format(func.__name__, end - start)
		print(message)
		return results)
	return inner
