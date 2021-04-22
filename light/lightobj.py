"""
投光物
"""
import rtmath
from geometry import vector

class CPointLight(object):
	def __init__(self, vPos=vector([0, 0, 3, 1]), vColor=vector([1., 1., 1.])):
		self.m_vPos = vPos
		self.m_vColor = vColor

	def SetPos(self, vPos):
		self.m_vPos = vPos

	def SetColor(self, vColor):
		self.m_vColor = vColor