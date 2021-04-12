# 用于测试每个流程是否正确
import camera
import numpy as np
from geometry import vector

def Test1():
	oCamera = camera.CUVNCamera(vEye=vector([-3, 0, 0, 1]), vAt=vector([-2, 0, 0, 1]), vUp=vector([0, 1, 0, 0]))
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
	oCamera = camera.CUVNCamera(vEye=vector([-3, 0, 0, 1]), vAt=vector([-2, 0, 0, 1]), vUp=vector([0, 1, 0, 0]), fAspect=0.5, fFar=3.0)
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


if __name__== '__main__':
	Test2()