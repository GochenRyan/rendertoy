import numpy as np

def normalize(vec):
	n = np.linalg.norm(vec)
	return vec / n if n != 0 else vec

def interp(x1, x2, t):
	return x1 + (x2 - x1) * t

def vertexInterp(oVertex1, oVertex2, t):
	import geometry
	vInterp = geometry.CVertex()
	vInterp.m_vPos[3] = 1
	vInterp.m_vPos = interp(oVertex1.m_vPos, oVertex2.m_vPos, t)
	vInterp.m_vTexCoord = interp(oVertex1.m_vTexCoord, oVertex2.m_vTexCoord, t)
	vInterp.m_vNorm = interp(oVertex1.m_vNorm, oVertex2.m_vNorm, t)
	vInterp.m_fRhw = interp(oVertex1.m_fRhw, oVertex2.m_fRhw, t)
	return vInterp

def reflect(vIncidentDir, vNorm):
	"""
	:param vIncidentDir: 单位入射向量
	:param vNorm: 单位法线向量
	:return:
	"""
	return vIncidentDir - 2 * np.dot(vIncidentDir, vNorm) * vNorm