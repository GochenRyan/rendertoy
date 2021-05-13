#!coding=utf-8
import numpy as np

def vector(lVector):
	return np.array(lVector, dtype="float32")


"""
网格
"""
class CMesh(object):
	def __init__(self, lVertex=None, lIndice=None, aTexture=None):
		self.m_lVertex = lVertex
		self.m_lIndice = lIndice
		self.m_aTexture = np.ones((256, 256, 4), dtype='uint8') * 255 if aTexture is None else aTexture

	def copy(self):
		lVertex = self.m_lVertex[:] if self.m_lVertex else None
		lIndice = self.m_lIndice[:] if self.m_lIndice else None

		return CMesh(lVertex=lVertex,
					 lIndice=lIndice,
					 aTexture=self.m_aTexture.copy())


"""
顶点
"""
class CVertex(object):
	def __init__(self, vPos=None, vNorm=None, vTexCoord=None, fRhw=None, vWorldPos=None):
		self.m_vPos = vector([0.0, 0.0, 0.0, 1.0]) if vPos is None else vPos  # 位置
		self.m_vNorm = vector([0.0, 0.0, 0.0, 0.0]) if vNorm is None else vNorm  # 法线
		self.m_vTexCoord = vector([0.0, 0.0]) if vTexCoord is None else vTexCoord  # 纹理坐标
		self.m_fRhw = 1.0 if fRhw is None else fRhw  # 1 / w
		self.m_vWorldPos = vector([0.0, 0.0, 0.0, 1.0]) if vWorldPos is None else vWorldPos

	def copy(self):
		return CVertex(vPos=self.m_vPos.copy(),
					   vNorm=self.m_vNorm.copy(),
					   vTexCoord=self.m_vTexCoord.copy(),
					   fRhw=self.m_fRhw,
					   vWorldPos=self.m_vWorldPos.copy())

	def __str__(self):
		return """
			pos: ({0}, {1}, {2}, {3})
			normal: ({4}, {5}, {6}, {7})
			texcoord: ({8}, {9})
			rhw: {10}
			world pos: ({11}, {12}, {13}, {14})
		""".format(self.m_vPos[0], self.m_vPos[1], self.m_vPos[2], self.m_vPos[3],
					self.m_vNorm[0], self.m_vNorm[1], self.m_vNorm[2], self.m_vNorm[3],
					self.m_vTexCoord[0], self.m_vTexCoord[1],
					self.m_fRhw,
					self.m_vWorldPos[0], self.m_vWorldPos[1], self.m_vWorldPos[2], self.m_vWorldPos[3])
