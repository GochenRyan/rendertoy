import rtmath
import numpy as np
from geometry import *

class CDevice(object):
	def __init__(self, iWidth=800, iHeight=600):
		self.m_iWidth = iWidth
		self.m_iHeight = iHeight
		self.m_aFrameBuffer = np.zeros((iHeight, iWidth, 4), dtype='uint8') * 255  # 帧缓冲
		self.m_aZBuffer = np.zeros((iHeight, iWidth),  dtype='float')  # z缓冲

	def ClearFrameBuffer(self, vColor=vector([0, 0, 0, 255])):
		self.m_aFrameBuffer[..., 0] = vColor[0]
		self.m_aFrameBuffer[..., 1] = vColor[1]
		self.m_aFrameBuffer[..., 2] = vColor[2]
		self.m_aFrameBuffer[..., 3] = vColor[3]

	def ClearZBuffer(self):
		self.m_aZBuffer[...] = 0

	def DrawMesh(self, lVertex, lIndice):
		for tIndices in lIndice:
			self.drawPrimitive(lVertex[tIndices[0]], lVertex[tIndices[1]], lVertex[tIndices[0]])

	def drawPrimitive(self, vVertex1, vVertex2, vVertex3):
		"""
		绘制图元：，法线变换，背面剔除，光栅化
		"""
		import camera
		oCameraMgr = camera.CMgr()
		oCamera = oCameraMgr.GetCamera(camera.I_TYPE_NORMAL)
		mMVP = oCamera.GetViewTrans() * oCamera.GetProjectTrans()
		mNormalTrans = oCamera.GetNormalTrans()

		vPoint1 = vVertex1.copy()
		vPoint2 = vVertex2.copy()
		vPoint3 = vVertex3.copy()

		# MVP变换
		vPoint1.m_vPos *= mMVP
		vPoint2.m_vPos *= mMVP
		vPoint3.m_vPos *= mMVP

		if self.isBackface(vPoint1.m_vPos, vPoint2.m_vPos, vPoint3.m_vPos):
			return

		# 法线变换
		vPoint1.m_vNorm *= mNormalTrans
		vPoint2.m_vNorm *= mNormalTrans
		vPoint3.m_vNorm *= mNormalTrans

		# 归一化
		self.homogenize(vPoint1.m_vPos)
		self.homogenize(vPoint2.m_vPos)
		self.homogenize(vPoint3.m_vPos)

		# rhw
		self.initRhw(vPoint1)
		self.initRhw(vPoint2)
		self.initRhw(vPoint3)

		# 屏幕映射
		self.screenMapping(vPoint1.m_vPos)
		self.screenMapping(vPoint2.m_vPos)
		self.screenMapping(vPoint3.m_vPos)

		# 梯形划分(当作梯形划分为上下两个三角形)
		tTrapezoids = self.trapezoidTriangle(vPoint1, vPoint2, vPoint3)
		for tTrap in tTrapezoids:
			self.drawScanline(tTrap)

	def initRhw(self, vVertex):
		vVertex.rhw = 1. / vVertex.m_vPos[3]

	def screenMapping(self, vPos):
		vPos[0] *= self.m_iWidth
		vPos[1] *= self.m_iHeight

	def isBackface(self, vPos1, vPos2, vPos3):
		"""
		判断是否是逆时针：
		(x1 * y2 - x2 * y1) + (x2 * y3 - x3 * y2) + (x3 * y1 - x1 * y3) >=  0
		"""
		mPos = np.vstack((vPos1, vPos2, vPos3))
		return (np.linalg.det(mPos[:2, :2]) + np.linalg.det(mPos[1:3, :2]) + np.linalg.det(mPos[2:4, 2:4])) >= 0

	def homogenize(self, vPos):
		"""
		归一化：
		([-1, 1] + 1) * 0.5
		"""
		w = vPos[3]
		vPos = vPos / w
		vPos[0] = (vPos[0] + 1) * 0.5
		vPos[1] = (vPos[1] + 1) * 0.5
		vPos[3] = w

	def trapezoidTriangle(self, vVertex1, vVertex2, vVertex3):
		"""切分三角形"""
		if vVertex1.m_vPos[0] == vVertex1.m_vPos[0] == vVertex3.m_vPos[0]:
			return []
		if vVertex1.m_vPos[1] == vVertex1.m_vPos[1] == vVertex3.m_vPos[1]:
			return []

		# y值从高到低
		if vVertex1.m_vPos[1] < vVertex2.m_vPos[1]:
			vVertex1, vVertex2 = vVertex2, vVertex1
		if vVertex1.m_vPos[1] < vVertex3.m_vPos[1]:
			vVertex1, vVertex3 = vVertex3, vVertex1
		if vVertex2.m_vPos[1] < vVertex3.m_vPos[1]:
			vVertex2, vVertex3 = vVertex3, vVertex2

		# 存在一边与x轴平行
		if vVertex1.m_vPos[1] - vVertex2.m_vPos[1] < 0.5:
			if vVertex1.m_vPos[0] > vVertex2.m_vPos[0]:
				vVertex1, vVertex2 = vVertex2, vVertex1
			return (((vVertex1, vVertex3), (vVertex2, vVertex3)),)

		if vVertex2.m_vPos[1] - vVertex3.m_vPos[1] < 0.5:
			if vVertex2.m_vPos[0] > vVertex3.m_vPos[0]:
				vVertex2, vVertex3 = vVertex3, vVertex2
			return (((vVertex1, vVertex2), (vVertex1, vVertex3)),)

		# 不存在一边与x轴平行，一分为二
		t = (vVertex1.m_vPos[1] - vVertex2.m_vPos[1]) / (vVertex1.m_vPos[1] - vVertex3.m_vPos[1])
		vInterp = rtmath.vertexInterp(vVertex1, vVertex3, t)

		if vInterp.m_vPos[0] < vVertex2.m_vPos[0]:
			return (((vVertex1, vInterp),(vVertex1, vVertex2)),((vInterp, vVertex3), (vVertex2, vVertex3)))
		else:
			return (((vVertex1, vVertex2), (vVertex1, vInterp)),((vVertex2, vVertex3), (vInterp, vVertex3)))


	def drawScanline(self, tTrapezoid):
		tLeft = tTrapezoid[0]
		tRight = tTrapezoid[1]

		iTopY = int(tLeft[0].m_vPos[1] + 0.5)
		iBottomY = int(tLeft[1].m_vPos[1] + 0.5)
		for iCurY in range(iBottomY, iTopY):
			# 剔除屏幕外的点

			# 纹理映射

			# 光照
			pass

		# rhw越大的点覆盖越小的点（可以提前）
