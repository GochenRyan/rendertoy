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
		pass