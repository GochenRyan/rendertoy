import base
import light.lightobj as lightobj
from .defines import *

class CMgr(object):
	__metaclass__ = base.Singleton
	m_dType2Light = {
		TYPE_POINT_LIGHT: []
	}

	def AddLight(self, oLight):
		iType = oLight.I_TYPE
		lLight = self.m_dType2Light.get(iType, None)
		if lLight is None:
			return
		lLight.append(oLight)

	def GetLights(self, sType):
		return self.m_dType2Light.get(sType, [])

	def GetLight(self, iID):
		for sType, lLight in self.m_dType2Light.items():
			for oLight in lLight:
				if oLight.m_iID == iID:
					return oLight
		return None
