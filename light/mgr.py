import base
import light.lightobj as lightobj
from .defines import *

class CMgr(object):
	__metaclass__ = base.Singleton
	def __init__(self):
		self.m_dType2Light = {
			I_POINT_LIGHT: lightobj.CPointLight()
		}

	def GetCamera(self, iType):
		return self.m_dType2Light.get(iType)
