import numpy as np

def normalize(vec):
	n = np.linalg.norm(vec)
	return vec / n if n != 0 else vec

def interp(x1, x2, t):
	return x1 + (x2 - x1) * t

def vertexInterp(vVertex1, vVertex2, t):
	import geometry
	vInterp = geometry.CVertex()
	vInterp.m_vPos[3] = 1
	vInterp.m_vPos = interp(vVertex1.m_vPos, vVertex2.m_vPos, t)
	vInterp.m_vTexCoord = interp(vVertex1.m_vTexCoord, vVertex2.m_vTexCoord, t)
	vInterp.m_vNorm = interp(vVertex1.m_vNorm, vVertex2.m_vNorm, t)
	vInterp.m_fRhw = interp(vVertex1.m_fRhw, vVertex2.m_fRhw, t)
	return vInterp