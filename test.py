# 用于测试每个流程是否正确
import camera
import numpy as np
from geometry import vector

def Test1():
	oCameraMgr = camera.CMgr()
	oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)
	oCamera.SetEye(vector([-3, 0, 0, 1]))
	oCamera.SetLookAt(vector([-2, 0, 0, 1]))
	oCamera.SetUp(vector([0, 1, 0, 0]))
	vPos = vector([-2, 0, 0, 1])
	mViewing = oCamera.GetViewTrans()
	print(mViewing)
	vViewPos = np.dot(mViewing, vPos)
	vViewPos = [int(i) for i in vViewPos]
	print(vViewPos)


def Test2():
	"""
	近大远小
	Z的范围映射到[-1,1]。当Z等于NearZ时映射结果为-1，而当Z等于FarZ时映射结果为1
	"""
	oCameraMgr = camera.CMgr()
	oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)
	oCamera.SetEye(vector([-3, 0, 0, 1]))
	oCamera.SetLookAt(vector([-2, 0, 0, 1]))
	oCamera.SetUp(vector([0, 1, 0, 0]))
	oCamera.SetAspect(0.5)
	oCamera.SetFar(3.0)
	vFarPos = vector([0, 0, 0, 1])  # far
	vNearPos = vector([-2, 0, 0, 1])  # near

	mViewing = oCamera.GetViewTrans()
	vViewFar = np.dot(mViewing, vFarPos)
	print("vViewFar: ", vViewFar)
	vViewNear = np.dot(mViewing, vNearPos)
	print("vViewNear: ", vViewNear)

	mPresp = oCamera.GetProjectTrans()
	print(mPresp)
	vPrespFarPos = np.dot(mPresp, vViewFar)
	print("vPrespFarPos: ", vPrespFarPos)
	vPrespNearPos = np.dot(mPresp, vViewNear)
	print("vPrespNearPos: ", vPrespNearPos)

	vVertex1 = vector([30, 40, 0, 1])
	print(np.dot(mPresp, vVertex1))



def Test3():
	import geometry
	import device
	oDevice = device.CDevice()
	oVertex1 = geometry.CVertex(vector([30, 40, 0, 1]), vector([0, 0, 1, 0]), vector([0, 0]), 0.5)
	oVertex2 = geometry.CVertex(vector([10, 20, 0, 1]), vector([0, 0, 1, 0]), vector([1, 0]), 0.8)
	oVertex3 = geometry.CVertex(vector([20, 0, 0, 1]), vector([0, 0, 1, 0]), vector([0, 1]), 0.2)

	tTrapezoids = oDevice.trapezoidTriangle(oVertex1, oVertex2, oVertex3)
	print(tTrapezoids)
	for tTrapezoid in tTrapezoids:
		for oVertex in tTrapezoid:
			print(oVertex[0])
			print(oVertex[1])
			print("---------")


def Test4():
	import device
	import geometry

	oCameraMgr = camera.CMgr()
	oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)
	oCamera.SetEye(vector([-3, 0, 0, 1]))
	oCamera.SetLookAt(vector([-2, 0, 0, 1]))
	oCamera.SetUp(vector([0, 1, 0, 0]))
	oCamera.SetAspect(0.5)
	oCamera.SetFar(300.0)

	mTexture = np.ones((256, 256, 4), dtype="uint8")
	grid_size = 32
	for i in range(8):
		# 每隔1个格子
		for j in [x * 2 for x in range(4)]:
			mTexture[i * grid_size: (i + 1) * grid_size, (j + i % 2) * grid_size: (j + i % 2 + 1) * grid_size,
			:] = vector([1. / 255, 128. / 255, 1, 1])

	oDevice = device.CDevice(mTexture=mTexture)
	oVertex1 = geometry.CVertex(vector([30, 40, 0, 1]), vector([0, 0, 1, 0]), vector([0, 0]), 0.5)
	oVertex2 = geometry.CVertex(vector([10, 20, 0, 1]), vector([0, 0, 1, 0]), vector([1, 0]), 0.8)
	oVertex3 = geometry.CVertex(vector([20, 0, 0, 1]), vector([0, 0, 1, 0]), vector([0, 1]), 0.2)
	oDevice.drawPrimitive(oVertex1, oVertex2, oVertex3)
	print("------zbuff:")
	iCount = 0
	for vZBuffer in oDevice.m_mZBuffer:
		for z in vZBuffer:
			if z > 1e-6:
				print("------count", iCount)
				print(vZBuffer)
				break
		iCount += 1
	print("------framebuffer")
	# print(oDevice.m_mFrameBuffer)

if __name__== '__main__':
	Test2()