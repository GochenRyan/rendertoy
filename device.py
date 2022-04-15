import rtmath
import light
import camera
from geometry import *

class CDevice(object):
	def __init__(self, iWidth=800, iHeight=600, mTexture=None):
		self.m_iWidth = iWidth
		self.m_iHeight = iHeight
		self.m_mFrameBuffer = np.zeros((iHeight, iWidth, 4), dtype='uint8') * 255  # 帧缓冲
		self.m_mZBuffer = np.zeros((iHeight, iWidth),  dtype='float')  # z缓冲
		self.m_mTexture = mTexture
		self.m_mModelTrans = np.eye(4)

	def SetModelTrans(self, mModelTrans):
		self.m_mModelTrans = mModelTrans

	def GetFramebuffer(self):
		return self.m_mFrameBuffer

	def GetNormalTrans(self):
		return np.linalg.inv(self.m_mModelTrans[:3, :3]).T

	def ClearFrameBuffer(self, vColor=vector([0, 0, 0, 255])):
		self.m_mFrameBuffer[..., 0] = vColor[0]
		self.m_mFrameBuffer[..., 1] = vColor[1]
		self.m_mFrameBuffer[..., 2] = vColor[2]
		self.m_mFrameBuffer[..., 3] = vColor[3]

	def ClearZBuffer(self):
		self.m_mZBuffer[...] = 0

	def DrawMesh(self, lVertex, lIndice):
		for tIndices in lIndice:
			self.drawPrimitive(lVertex[tIndices[0]], lVertex[tIndices[1]], lVertex[tIndices[2]])

	def drawPrimitive(self, oVertex1, oVertex2, oVertex3):
		"""
		绘制图元：MVP变换，法线变换，背面剔除，光栅化
		"""
		oCameraMgr = camera.CMgr()
		oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)
		mMV = np.dot(oCamera.GetViewTrans(), self.m_mModelTrans)
		mMVP = np.dot(oCamera.GetProjectTrans(), mMV)

		mNormalTrans = self.GetNormalTrans()

		oPoint1 = oVertex1.copy()
		oPoint2 = oVertex2.copy()
		oPoint3 = oVertex3.copy()

		oPoint1.m_vWorldPos = oPoint1.m_vPos.copy()
		oPoint2.m_vWorldPos = oPoint2.m_vPos.copy()
		oPoint3.m_vWorldPos = oPoint3.m_vPos.copy()

		# MVP变换
		oPoint1.m_vPos = np.dot(mMVP, oPoint1.m_vPos)
		oPoint2.m_vPos = np.dot(mMVP, oPoint2.m_vPos)
		oPoint3.m_vPos = np.dot(mMVP, oPoint3.m_vPos)

		# 背面剔除
		if self.isBackface(oPoint1.m_vPos, oPoint2.m_vPos, oPoint3.m_vPos):
			return

		# 法线变换
		oPoint1.m_vNorm[:3] = np.dot(mNormalTrans, oPoint1.m_vNorm[:3])
		oPoint2.m_vNorm[:3] = np.dot(mNormalTrans, oPoint2.m_vNorm[:3])
		oPoint3.m_vNorm[:3] = np.dot(mNormalTrans, oPoint3.m_vNorm[:3])

		# 归一化
		self.homogenize(oPoint1)
		self.homogenize(oPoint2)
		self.homogenize(oPoint3)

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
		oVertex.m_fRhw = 1. / oVertex.m_vPos[3]
		oVertex.m_vTexCoord *= oVertex.m_fRhw

	def screenMapping(self, vPos):
		vPos[0] *= self.m_iWidth
		vPos[1] *= self.m_iHeight

	def isBackface(self, vPos1, vPos2, vPos3):
		"""
		判断是否是逆时针（逆时针顺序为正面）：
		(x1 * y2 - x2 * y1) + (x2 * y3 - x3 * y2) + (x3 * y1 - x1 * y3) >=  0
		"""
		mPos = np.vstack((vPos1, vPos2, vPos3, vPos1))
		return (np.linalg.det(mPos[:2, :2]) + np.linalg.det(mPos[1:3, :2]) + np.linalg.det(mPos[2:4, :2])) < 0

	def homogenize(self, oVertex):
		"""
		归一化：
		([-1, 1] + 1) * 0.5
		"""
		w = oVertex.m_vPos[3]
		vPos = oVertex.m_vPos / w
		vPos[0] = (vPos[0] + 1) * 0.5
		vPos[1] = (vPos[1] + 1) * 0.5
		vPos[3] = w
		oVertex.m_vPos = vPos

	def trapezoidTriangle(self, oVertex1, oVertex2, oVertex3):
		"""切分三角形"""
		if oVertex1.m_vPos[0] == oVertex2.m_vPos[0] == oVertex3.m_vPos[0]:
			return []
		if oVertex1.m_vPos[1] == oVertex2.m_vPos[1] == oVertex3.m_vPos[1]:
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
			# 剔除屏幕外的点
			if iCurY > self.m_iHeight:
				break
			if iCurY < 0:
				continue
			
			t = (iCurY - iBottomY) / iDeltaY
			oStartVertex = rtmath.vertexInterp(oleftBottomVertex, oLeftTopVertex, t)
			oEndVertex = rtmath.vertexInterp(oRightBottomVertex, oRightTopVertex, t)

			iEnd = int(oEndVertex.m_vPos[0] + 0.5)
			iStart = int(oStartVertex.m_vPos[0] + 0.5)
			
			# 剔除屏幕外的点
			if iEnd < 0:
				break
			if iStart > self.m_iWidth:
				break

			oRealStart = oStartVertex
			oRealEnd = oEndVertex
			if iStart < 0 < iEnd:
				t = -iStart / (iEnd - iStart)
				oRealStart = rtmath.vertexInterp(oStartVertex, oEndVertex, t)
				oRealEnd = oEndVertex
				iStart = 0
			if iStart < self.m_iWidth < iEnd:
				t = (self.m_iWidth - iStart) / (iEnd - iStart)
				oRealEnd = rtmath.vertexInterp(oStartVertex, oEndVertex, t)
				oRealStart = oStartVertex
				iEnd = self.m_iWidth

			iSampleNum = iEnd - iStart + 1
			mLineFrameBuffer = self.m_mFrameBuffer[iCurY, iStart: iEnd + 1]
			mLineZBuffer = self.m_mZBuffer[iCurY, iStart: iEnd + 1]
			vRhw = np.linspace(oStartVertex.m_fRhw, oEndVertex.m_fRhw, iSampleNum)

			# 纹理映射
			mLineTex = self.textureLine(self.m_mTexture, oRealStart, oRealEnd, iSampleNum, vRhw)
			# mLineWorldPos = np.linspace(oRealStart.m_vWorldPos, oRealEnd.m_vWorldPos, iSampleNum)
			mLineNorm = np.linspace(oRealStart.m_vNorm, oRealEnd.m_vNorm, iSampleNum)

			oLightMgr = light.CMgr()
			lPointLight = oLightMgr.GetLights(light.TYPE_POINT_LIGHT)
			# oCameraMgr = camera.CMgr()
			# oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)
			# vCameraPos =oCamera.GetEye()
			#
			# # 冯氏光照模型，Phong着色
			# for oPointLight in lPointLight:
			# 	vLightPos = oPointLight.GetPos()
			# 	vLightColor = oPointLight.GetColor()
			# 	for i in range(iSampleNum):
			# 		# 环境
			# 		vAmbient = vector([0.7, 0.7, 0.7, 1])
			#
			# 		# 漫反射
			# 		vNorm = mLineNorm[i]
			# 		vLightDir = rtmath.normalize(vLightPos - mLineWorldPos[i])
			# 		vDiffuse = max(np.dot(vNorm, vLightDir), 0) * vLightColor
			#
			# 		# 镜面反射
			# 		vFragWorldPos = mLineWorldPos[i]
			# 		vViewDir = rtmath.normalize(vCameraPos - vFragWorldPos)
			# 		vIncidentDir = rtmath.normalize(vFragWorldPos - vLightPos)
			# 		vReflectDir = rtmath.reflect(vIncidentDir, vNorm)
			# 		vSpec = 0.5 * pow(max(np.dot(vViewDir, vReflectDir), 0.), 32) * vLightColor
			# 		vFragColor = (vAmbient + vDiffuse + vSpec) * mLineTex[i]
			# 		mLineTex[i] = ((vFragColor * 255) + 0.5).astype(int)


			light_dir = vector([0, 0, 1, 0])
			diffuse = np.maximum(np.atleast_2d(np.dot(mLineNorm, -light_dir)).T, 0) * vector([0.05, 0.05, 0.05, 1])
			ambient = vector([0.7, 0.7, 0.7, 1])
			mLineTex[:, :] = np.minimum((diffuse + ambient) * mLineTex[:, :] * 255, 255)

			# rhw越大的点覆盖越小的点
			vMask = mLineZBuffer <= vRhw
			mLineFrameBuffer[vMask] = mLineTex[vMask]
			mLineZBuffer[vMask] = vRhw[vMask]


	def textureLine(self, mFrameBuffer, oStart, oEnd, iSampleNum, vRhw):
		"""
		读取texcoord对应的纹理
		"""
		iH, iW, iC = mFrameBuffer.shape
		iH -= 1
		iW -= 1

		tStartTex = oStart.m_vTexCoord[0] * iW, oStart.m_vTexCoord[1] * iH
		tEndTex = oEnd.m_vTexCoord[0] * iW, oEnd.m_vTexCoord[1] * iH

		# 映射
		# see https://en.wikipedia.org/wiki/Texture_mapping#Perspective_correctness
		vX = (np.linspace(tStartTex[0], tEndTex[0], iSampleNum) / vRhw + 0.5).astype(int)
		vY = (np.linspace(tStartTex[1], tEndTex[1], iSampleNum) / vRhw + 0.5).astype(int)

		return mFrameBuffer[vY, vX]
