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
	def __init__(self, vPos=None, vNorm=None, vTexCoord=None, fRwh=None):
		self.m_vPos = vector([0.0, 0.0, 0.0]) if vPos is None else vPos  # 位置
		self.m_vNorm = vector([0.0, 0.0, 0.0]) if vNorm is None else vNorm  # 法线
		self.m_vTexCoord = vector([0.0, 0.0]) if vTexCoord is None else vTexCoord  # 纹理坐标
		self.m_fRwh = vector([0.0, 0.0, 0.0]) if fRwh is None else fRwh  # 1 / w

	def copy(self):
		return CVertex(vPos=self.m_vPos.copy(),
					   vNorm=self.m_vNorm.copy(),
					   vTexCoord=self.m_vTexCoord.copy(),
					   fRwh=self.m_fRwh.copy())