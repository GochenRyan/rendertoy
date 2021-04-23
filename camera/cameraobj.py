"""
相机空间：右手系
"""
import numpy as np
import rtmath
from geometry import vector

TYPE_NORMAL = 1

class CUVNCamera(object):
	def __init__(self, vEye=vector([0, 0, -3, 1]), vAt=vector([0.23, 0, 0, 1]), vUp=vector([0, 1, 0, 0]), fFov=0.5*np.pi, fAspect=1.0, fNear=1.0, fFar=500.0):
		self.m_vEye = vEye  # 相机的位置
		self.m_vAt = vAt  # 注视目标的位置
		self.m_vUp = vUp  # 上向量
		self.m_mViewTrans = None
		self.m_fFov = fFov  # 竖直方向的张开角度
		self.m_fAspect = fAspect
		self.m_fNear = fNear  # 近裁剪平面
		self.m_fFar = fFar  # 远裁剪平面
		self.m_mPerspTrans = None
		self.m_mNormalTrans = None

	def GetNormalTrans(self):
		self.calNormalTrans()
		return self.m_mNormalTrans

	def calNormalTrans(self):
		self.calViewTrans()
		return np.linalg.inv(self.m_mViewTrans[:3, :3]).T

	def GetViewTrans(self):
		self.calViewTrans()
		return self.m_mViewTrans

	def calViewTrans(self):
		"""
		观察空间为右手系，这里算出U、N、V轴在世界空间的表示，叉乘顺序为UxV,VxN,NxU
		摄像机指向-N方向
		过程：1.平移  2.空间变换
		"""
		vN = rtmath.normalize(self.m_vEye - self.m_vAt)[:3]
		vU = rtmath.normalize(-np.cross(self.m_vUp[:3], vN))
		vV = rtmath.normalize(-np.cross(vN, vU))
		mTemp = np.eye(4)
		mTemp[0, :3] = vU
		mTemp[1, :3] = vV
		mTemp[2, :3] = vN
		mTemp[0, 3] = -np.dot(self.m_vEye[:3], vU)
		mTemp[1, 3] = -np.dot(self.m_vEye[:3], vV)
		mTemp[2, 3] = -np.dot(self.m_vEye[:3], vN)
		self.m_mViewTrans = mTemp

	def GetProjectTrans(self):
		self.calProjectTrans()
		return self.m_mPerspTrans

	def calProjectTrans(self):
		"""
		需要考虑Z分量需要取反
		:return:
		"""
		cot = 1. / np.tan(self.m_fFov / 2.)
		zRange = self.m_fFar - self.m_fNear
		mTemp = np.zeros((4, 4))
		mTemp[0, 0] = cot / self.m_fAspect
		mTemp[1, 1] = cot
		mTemp[2, 2] = (self.m_fNear + self.m_fFar) / zRange  # 取反
		mTemp[2, 3] = 2 * self.m_fFar * self.m_fNear / zRange
		mTemp[3, 2] = 1  # 取反
		self.m_mPerspTrans = mTemp

	def SetLookAt(self, vAt):
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

	def GetEye(self):
		return self.m_vEye