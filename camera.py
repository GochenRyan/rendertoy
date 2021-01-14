import numpy as np
import rtmath

from geometry import vector

class CUVNCamera(object):
	def __init__(self, vEye=None, vAt=None, vUp=None):
		self.m_vEye = vector([0, 0, -3, 1]) if vEye is None else vEye
		self.m_vAt = vector([0.23, 0, 0, 1]) if vAt is None else vAt
		self.m_vUp = vector([0, 1, 0, 1]) if vUp is None else vUp
		self.m_mViewTrans = None

	def GetViewTrans(self):
		if not self.m_mViewTrans:
			pass
		fN = rtmath.normalize(self.m_vAt - self.m_vEye)[:3]
		fV = rtmath.normalize(self.m_vUp)[:3]
		fU = None # 右手系(todo:确定正负)


		return self.m_mViewTrans

	def SetPos(self, vAt):
		pass

	def SetEye(self, vEye):
		pass

	def SetUp(self, vUp):
		pass