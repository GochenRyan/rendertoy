#!coding=utf-8
g_lSingletonCls = []

def Reset():
	global g_lSingletonCls
	for oCls in g_lSingletonCls:
		oCls.ClearInstance()

class Singleton(type):
	def __init__(cls, name, base, dct):
		super(Singleton, cls).__init__(name, base, dct)
		cls.instance = None

	def __call__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = super(Singleton, cls).__call__( *args, **kwargs)
			global g_lSingletonCls
			g_lSingletonCls.append(cls)
			return cls.instance

	def ClearInstance(cls):
		cls.instance = None

	def HasInstance(cls):
		return cls.instance != None