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

	def drawPrimitive(self, oVertex1, oVertex2, oVertex3):
		"""
		绘制图元：，法线变换，背面剔除，光栅化
		"""
		import camera
		oCameraMgr = camera.CMgr()
		oCamera = oCameraMgr.GetCamera(camera.I_TYPE_NORMAL)
		mMVP = oCamera.GetViewTrans() * oCamera.GetProjectTrans()
		mNormalTrans = oCamera.GetNormalTrans()

		oPoint1 = oVertex1.copy()
		oPoint2 = oVertex2.copy()
		oPoint3 = oVertex3.copy()

		# MVP变换
		oPoint1.m_vPos *= mMVP
		oPoint2.m_vPos *= mMVP
		oPoint3.m_vPos *= mMVP

		if self.isBackface(oPoint1.m_vPos, oPoint2.m_vPos, oPoint3.m_vPos):
			return

		# 法线变换
		oPoint1.m_vNorm *= mNormalTrans
		oPoint2.m_vNorm *= mNormalTrans
		oPoint3.m_vNorm *= mNormalTrans

		# 归一化
		self.homogenize(oPoint1.m_vPos)
		self.homogenize(oPoint2.m_vPos)
		self.homogenize(oPoint3.m_vPos)

		# rhw
		self.initRhw(oPoint1)
		self.initRhw(oPoint2)
		self.initRhw(oPoint3)

		# 屏幕映射
		self.screenMapping(oPoint1.m_vPos)
		self.screenMapping(oPoint2.m_vPos)
		self.screenMapping(oPoint3.m_vPos)

		# 梯形划分(当作梯形划分为上下两个三角形)
		tTrapezoids = self.trapezoidTriangle(oPoint1, oPoint2, oPoint3)
		for tTrap in tTrapezoids:
			self.drawScanline(tTrap)

	def initRhw(self, oVertex):
		oVertex.rhw = 1. / oVertex.m_vPos[3]

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

	def trapezoidTriangle(self, oVertex1, oVertex2, oVertex3):
		"""切分三角形"""
		if oVertex1.m_vPos[0] == oVertex1.m_vPos[0] == oVertex3.m_vPos[0]:
			return []
		if oVertex1.m_vPos[1] == oVertex1.m_vPos[1] == oVertex3.m_vPos[1]:
			return []

		# y值从高到低
		if oVertex1.m_vPos[1] < oVertex2.m_vPos[1]:
			oVertex1, oVertex2 = oVertex2, oVertex1
		if oVertex1.m_vPos[1] < oVertex3.m_vPos[1]:
			oVertex1, oVertex3 = oVertex3, oVertex1
		if oVertex2.m_vPos[1] < oVertex3.m_vPos[1]:
			oVertex2, oVertex3 = oVertex3, oVertex2

		# 存在一边与x轴平行
		if oVertex1.m_vPos[1] - oVertex2.m_vPos[1] < 0.5:
			if oVertex1.m_vPos[0] > oVertex2.m_vPos[0]:
				oVertex1, oVertex2 = oVertex2, oVertex1
			return (((oVertex1, oVertex3), (oVertex2, oVertex3)),)

		if oVertex2.m_vPos[1] - oVertex3.m_vPos[1] < 0.5:
			if oVertex2.m_vPos[0] > oVertex3.m_vPos[0]:
				oVertex2, oVertex3 = oVertex3, oVertex2
			return (((oVertex1, oVertex2), (oVertex1, oVertex3)),)

		# 不存在一边与x轴平行，一分为二
		t = (oVertex1.m_vPos[1] - oVertex2.m_vPos[1]) / (oVertex1.m_vPos[1] - oVertex3.m_vPos[1])
		oInterp = rtmath.vertexInterp(oVertex1, oVertex3, t)

		if oInterp.m_vPos[0] < oVertex2.m_vPos[0]:
			return (((oVertex1, oInterp),(oVertex1, oVertex2)),((oInterp, oVertex3), (oVertex2, oVertex3)))
		else:
			return (((oVertex1, oVertex2), (oVertex1, oInterp)),((oVertex2, oVertex3), (oInterp, oVertex3)))


	def drawScanline(self, tTrapezoid):
		tLeft = tTrapezoid[0]
		tRight = tTrapezoid[1]

		iTopY = int(tLeft[0].m_vPos[1] + 0.5)
		iBottomY = int(tLeft[1].m_vPos[1] + 0.5)

		oLeftTopVertex = tLeft[0]
		oleftBottomVertex = tLeft[1]
		oRightTopVertex = tRight[0]
		oRightBottomVertex = tRight[1]

		iDeltaY = iTopY - iBottomY
		for iCurY in range(iBottomY, iTopY):
			t = (iCurY - iBottomY) / iDeltaY
			oStartVertex = rtmath.vertexInterp(oleftBottomVertex, oLeftTopVertex, t)
			oEndVertex = rtmath.vertexInterp(oRightBottomVertex, oRightTopVertex, t)

			iEnd = int(oEndVertex.m_vPos[0] + 0.5)
			iStart = int(oStartVertex.m_vPos[0] + 0.5)
			iSampleNum = iEnd - iStart + 1

			# 剔除屏幕外的点
			# 纹理映射

			# 光照
			pass

		# rhw越大的点覆盖越小的点（可以提前）
