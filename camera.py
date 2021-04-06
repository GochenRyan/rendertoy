import numpy as np
import rtmath

from geometry import vector
"""
相机空间：右手系
"""
class CUVNCamera(object):
	def __init__(self, vEye=vector([0, 0, -3, 1]), vAt=vector([0.23, 0, 0, 1]), vUp=vector([0, 1, 0, 1]), fFov=0.5*np.pi, fAspect=1.0, fNear=1.0, fFar=500.0):
		self.m_vEye = vEye  # 相机的位置
		self.m_vAt = vAt  # 注视目标的位置
		self.m_vUp = vUp  # 上向量
		self.m_mViewTrans = None
		self.m_fFov = fFov
		self.m_fAspect = fAspect
		self.m_fNear = fNear
		self.m_fFar = fFar
		self.m_mProjectTrans = None

	def GetViewTrans(self):
		self.calViewTrans()
		return self.m_mViewTrans

	def calViewTrans(self):
		# 观察空间为右手系，这里算出U、N、V轴在世界空间的表示
		fN = rtmath.normalize(self.m_vEye - self.m_vAt)[:3]
		fU = -rtmath.normalize(np.cross(self.m_vUp[:3], fN))
		fV = rtmath.normalize(np.cross(fU, fN))

		mTemp = np.eye(4)
		mTemp[0, :3] = fU
		mTemp[1, :3] = fV
		mTemp[2, :3] = fN
		mTemp[3, 0] = -np.dot(fU, self.m_vEye[:3])
		mTemp[3, 1] = -np.dot(fV, self.m_vEye[:3])
		mTemp[3, 2] = -np.dot(fN, self.m_vEye[:3])
		self.m_mViewTrans = mTemp

	def GetProjectTrans(self):
		return self.m_mProjectTrans

	def calProjectTrans(self):
		pass

	def SetPos(self, vAt):
		self.m_vAt = vAt
		self.calViewTrans()

	def SetEye(self, vEye):
		self.m_vEye = vEye
		self.calViewTrans()

	def SetUp(self, vUp):
		self.m_vUp = vUp
		self.calViewTrans()

	def SetFov(self, fFov):
		self.m_fFov = fFov

	def SetAspect(self, fAspect):
		self.m_fAspect = fAspect

	def SetNear(self, fNear):
		self.m_fNear = fNear

	def SetFar(self, fFar):
		self.m_fFar = fFar