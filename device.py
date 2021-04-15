import numpy as np
from geometry import *

class CDevice(object):
	def __init__(self, iWidth, iHeight):
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
		pass

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
		pass

	def drawScanline(self, tTrapezoid):
		pass