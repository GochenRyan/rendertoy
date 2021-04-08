# 用于测试每个流程是否正确
import camera
import numpy as np
from geometry import vector

def Test1():
	oCamera = camera.CUVNCamera(vector([-3, 0, 0, 1]), vector([0, 0, 0, 1]), vector([0, 1, 0, 0]))
	vPos = vector([-2, 0, 0, 1])
	mViewing = oCamera.GetViewTrans()
	print(mViewing)
	vViewPos = np.dot(vPos, mViewing)
	print(vViewPos)

if __name__== '__main__':
	Test1()