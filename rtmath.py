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
	vInterp.m_vWorldPos = interp(oVertex1.m_vWorldPos, oVertex2.m_vWorldPos, t)
	return vInterp


def reflect(vIncidentDir, vNorm):
	"""
	:param vIncidentDir: 单位入射向量
	:param vNorm: 单位法线向量
	:return:
	"""
	return vIncidentDir - 2 * np.dot(vIncidentDir, vNorm) * vNorm


def getRotateMatrix(vAxis, fTheta):
	"""
	绕任意轴旋转
	:param vAxis: 旋转轴
	:param fTheta: 旋转角度
	:return:
	"""

	mTemp = np.eye(4)
	fCos = np.cos(fTheta)
	fOneSubCos = 1 - fCos
	fSin = np.sin(fTheta)
	fX, fY, fZ = normalize(vAxis[:3])

	mTemp[0, 0] = fCos + fOneSubCos * fX ** 2
	mTemp[0, 1] = fOneSubCos * fX * fY - fSin * fZ
	mTemp[0, 2] = fOneSubCos * fX * fZ + fSin * fY
	mTemp[1, 0] = fOneSubCos * fX * fY + fSin * fZ
	mTemp[1, 1] = fCos + fOneSubCos * fZ ** 2
	mTemp[1, 2] = fOneSubCos * fY * fZ - fSin * fX
	mTemp[2, 0] = fOneSubCos * fX * fZ - fSin * fY
	mTemp[2, 1] = fOneSubCos * fY * fZ + fSin * fX
	mTemp[2, 2] = fCos + fOneSubCos * fZ ** 2

	return mTemp