"""
投光物
"""
import rtmath
from .defines import *
from geometry import vector

class CPointLight(object):
	I_TYPE = TYPE_POINT_LIGHT
	def __init__(self, iID, vPos=vector([0, 0, 3, 1]), vColor=vector([1., 1., 1.])):
		self.m_iID = iID
		self.m_vPos = vPos
		self.m_vColor = vColor

	def SetPos(self, vPos):
		self.m_vPos = vPos

	def SetColor(self, vColor):
		self.m_vColor = vColor

	def GetPos(self):
		return self.m_vPos

	def GetColor(self):
		return self.m_vColor