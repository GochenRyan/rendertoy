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

if __name__== '__main__':
	Test1()