import sys
sys.path.append('../../')

from sciapp import Manager

def add_get_test():
	'''
	add(name, object, tag=None): add one name, object pair (at first). 
	has(name=None, tag=None, obj=None): check exists, None matches any.

	get(name=None, tag=None): get the first matched object, or None.
		None matches any, so get() return the first object.
	gets(name=None, tag=None): get all matched [(name, obj, tag)...]
		None matches any, so gets() return all records.
	remove(name=None, tag=None, obj=None): remove all matched records
		None matches any, so remove() would clear the list.
	'''
	print('manager test add, get, gets:')
	manager = Manager()
	# add a name, value pair
	manager.add(name='one', obj='object1')
	# you can also omit the name, obj
	manager.add('two', 'object2')

	print(manager.names())
	# >>> ['two', 'one'] , the later inserted is at first!
	print(manager.get())
	# >>> object1 , return the first object, or None
	print(manager.get(name='one'))
	# >>> object1 , return the first matched object, or None
	print(manager.gets())
	# >>> [('two', 'object2', None), ('one', 'object1', None)]
	manager.remove(name='two')
	# >>> [('one', 'object1', None)]
	print(manager.gets())
	print()

def tag_test():
	'''
	another information for searching. default tag is None.
	'''
	print('manager test with tag:')
	manager = Manager()
	manager.add('one', 'object1', 'low')
	manager.add('two', 'object2', 'low')
	manager.add('one', 'OBJECT1', 'up')
	manager.add('two', 'OBJECT2', 'up')

	print(manager.gets(tag='low'))
	# >>> [('two', 'object2', 'low'), ('one', 'object1', 'low')]
	print(manager.gets(tag='up'))
	# >>> [('two', 'OBJECT2', 'up'), ('one', 'OBJECT1', 'up')]
	print()

def order_test():
	'''
	add method puts object at first, get() means the lasted one.
	you can use active to move record to the first.
	'''
	print('manager order test:')
	manager = Manager()
	manager.add('one', 'object1')
	manager.add('two', 'object2')
	manager.add('three', 'object3')
	print(manager.names())
	# >>> ['three', 'two', 'one']
	manager.active('one')
	print(manager.names())
	# >>> ['one', 'three', 'two']
	print()

def unique_test():
	'''
	unique means add a object with same name and tag would replace the old one.
	if you want allow the duplicate records, please use unique=False.
	'''
	print('manager unique test:')
	manager = Manager()
	manager.add('one', 'object1')
	manager.add('one', 'OBJECT1')
	print(manager.gets())
	# >>> [('one', 'OBJECT1', None)]

	manager = Manager(unique=False)
	manager.add('one', 'object1')
	manager.add('one', 'OBJECT1')
	print(manager.gets())
	# >>> [('one', 'OBJECT1', None), ('one', 'object1', None)]
	print()

def io_test():
	'''
	manager object has read and write method to transform with file.
	'''
	print('show how to read and write a manager:')
	manager = Manager()
	manager.add('one', 'object1')
	manager.add('two', 'object2')
	manager.write('manager.json')

	manager = Manager()
	manager.read('manager.json')
	print(manager.gets())
	# >>> [('one', 'object1', None), ('two', 'object2', None)]

	# you can also pass path parameter when init a Manager
	manager = Manager(path='manager.json')
	print(manager.gets())
	# >>> [('one', 'object1', None), ('two', 'object2', None)]
	print()

if __name__ == '__main__':
	add_get_test()
	tag_test()
	order_test()
	unique_test()
	io_test()