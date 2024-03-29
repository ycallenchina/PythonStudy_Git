#1子类继承父类私有属性的机制
#2子类继承父类私有属性的方法
#3子类继承父类的属性后外加自身属性的方法
#4子类继承父类的方法后外加自身方法的方法
#5多继承,以及MRO机制_多继承的关系机制

'''父类的私有属性的机制
		通过改名实现:
		举例: 在父类中的原名,self.__name
			  当父类自身调用时改为,self._父类名__name

			  所以,在外部调用self.__name时,因为与self._父类名__name不同,固出错.
			  '''

#2子类继承父类私有属性的方法
#直接继承会出错,必须改名为self._父类名__name
#实例
import sys
class 父类:
	def __init__(self,n):
		self.__name=n

	def say(self):
		print(f'{self.__name},我是本父类')

class 子类(父类):

	#引用的属性是父类的私有属性__name,方法是自己的.
	def say(self):
		# print(f'{self.__name},我是子类')#---错误写法,因为'子类' object has no attribute '_子类__name'
		print(f'{self._父类__name},我是子类,我使用了你私有属性')



b=父类('父亲')
b.say()

a=子类('父亲')
a.say()


#3子类继承父类的属性后外加自身属性的方法
#super()使用方法
class  孙类(父类):
	def __init__(self,n,arg):
		super().__init__(n)
		#第二种写法:父类.__init__(self,n)#注意:需要写上self参数
		self.arg = arg
	
	def say(self):
		print(f'{self.arg},哈哈,{self._父类__name},我是孙类,我在你属性n参数上加了自己的arg参数')

print(f'  {sys._getframe().f_lineno} 行结果:','----------------------')
c=孙类('n参数','arg参数')
c.say()	


#4子类继承父类的方法后外加自身方法的方法

class  子孙类(父类):
	
	def say(self):
		print(f'哈哈,{self._父类__name},我是你子孙,我在你方法上再加了自己方法')	
		super().say()

d=子孙类('n参数')
d.say()	

#多继承,MRO机制:按继承的顺序开始优先继承同名属性,和同名方法.没有同名的情况就全继承.
'''例如:祖宗类的继承孙类会覆盖子孙类的同名方法say(),也因为子孙类没有自己的__init__,所以继承了孙类的__init__.
即时有,同名__init__,也会按顺序优先继承第一位__init__里的属性,抛弃后面所有类里面的__init__'''
class 祖宗类(孙类,子孙类):
	pass;

print(f'  {sys._getframe().f_lineno}  行结果:','--------------------')
e=祖宗类('n祖宗参数','arg祖宗参数')
e.say()
print(f'  {sys._getframe().f_lineno}  行结果:','查看祖宗类的mro列表:')
print(祖宗类.__mro__)
print(祖宗类.mro())

'''
MRO机制补充说明:
当要生成F的继承顺序时，C3算法过程如下：首先将入度（指向该节点的箭头数量）为零的节点放入列表，
并将F节点及与F节点有关的箭头从上图树中删除；继续找入度为0的节点，找到D和E，左侧优先，故而现将D放入列表，
并从上图树中删除D，这是列表中就有了F、D。继续找入度为0的节点，有A和E满足，左侧优先，所以是A，将A从上图中取出放入列表，
列表中顺序为F、D、E；接下来入度为0的节点只剩下E，取出E放入列表；只剩下B和C节点，且入度都为0，
但左侧优先，二先将B放入列表，然后才是后才是C；不过别忘了，Python所有类都有一个共同的父类，那就是object类，
所以，最好还会把object放入列表末尾。最终生成列表中元素顺序为：F->D->A->E->B->C->object
资料图片网址:https://img2018.cnblogs.com/blog/1539768/201812/1539768-20181203145957255-31915685.png
'''
# 实例说明 继承关系.
class A:
	def go(self):
		print('ImA')
	pass
class B:
	pass
class C:
	pass
class D(A,B):
	pass
class E(B,C):
	def go(self):
		print('ImE')
	pass
class F(D,E):
	pass


F().go()#居E级别比A高,但是然部是imE 是imA
