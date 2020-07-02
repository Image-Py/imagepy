# Manager

Manager是一个通用容器，类似一个内存数据库，负责对象的增删查改



### 方法列举：

* **add(self, name, obj, tag=None):** 添加一个对象，tag作为可选标签，对象添加在有序列表的最前面

* **adds(self, objs):** 批量添加name, obj, tag列表

* **gets(self, name=None, tag=None, obj=None):** 获取满足条件的对象，返回name, obj, tag列表，None表示不作为条件

* **get(self, name=None, tag=None, obj=None):** 获取满足条件的第一个object，如果没有满足返回None，空缺参数用来获取第一个对象。

* **has(self, name=None, tag=None, obj=None):** 返回是否存在匹配条件的对象

* **active(self, name=None, tag=None, obj=None):** 将满足筛选条件的记录移动到列表最前

* **set(self, name, obj, tag=None):** 通过name，tag筛选记录，将obj赋值

* **remove(self, name=None, tag=None, obj=None):** 删除满足条件的记录

* **names(self, tag=None):** 返回所有的name列表

* **write(self, path=None):** 将记录写入文件，只有可以json序列号的对象才支持写入。

* **def read(self, path):** 从文件读取记录到当前manager

  

### 用法举例

这个例子演示如何使用add,  get

```python
def add_get_test():
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
	print(manager.gets())
    # >>> [('one', 'object1', None)]
```



这个例子演示如何利用tag进行筛选

```python
def tag_test():
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
```



这个例子说明容器内部是按照添加的倒序存放的，调用active可以将满足条件的元素置顶。

```python
def order_test():
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
```



这个例子演示了默认情况下，相同name, tag的对象重复添加，会覆盖之前的记录，但是在构造时用unique=False则允许重复添加。

```python
def unique_test():
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
```



manager对象可以write到文件，也可以从文件read，构造时如果传入path参数，则自动从路径进行read。记录为name, obj, tag的列表，以json格式存储，因此manager可以读写的条件是，所有元素都可以json化。

```python
def io_test():
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
```

