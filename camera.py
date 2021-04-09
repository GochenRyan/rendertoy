import numpy as np
import rtmath

from geometry import vector
"""
相机空间：右手系
"""
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

	def GetViewTrans(self):
		self.calViewTrans()
		return self.m_mViewTrans

	def calViewTrans(self):
		# 观察空间为右手系，这里算出U、N、V轴在世界空间的表示，叉乘顺序为UxV,VxN,NxU
		# 摄像机指向-N方向
		# 过程：1.平移  2.空间变换
		vN = rtmath.normalize(self.m_vEye - self.m_vAt)[:3]
		vU = rtmath.normalize(-np.cross(self.m_vUp[:3], vN))
		vV = rtmath.normalize(-np.cross(vN, vU))

		print(vU, vV, vN)
		print(np.cross(vector([1,0,0]), vector([0,1,0])))

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