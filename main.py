import pyglet
from pyglet import image
from defines import *
from geometry import *
import device
import camera
import light
import base

"""
3D流水线：物体->多边形->顶点->变换->光栅化->屏幕
1. 执行局部坐标到世界坐标变换
2. 物体消除
3. 执行背面消除
4. 执行世界坐标到相机坐标变换
5. 执行3D裁剪
6. 执行相机坐标到透视坐标变换，即投影
7. 执行透视坐标到视口（屏幕）坐标变换
8. 光栅化多边形

规定：
1. 左手系，观察空间右手系(与Unity相同)
2. 右乘、列矩阵
"""

@base.DocProfile("./cpf_run.prof")
def main():
	oGameWindow = pyglet.window.Window(I_WIDTH, I_HEIGHT)

	# 顶点
	lVertex = [
		# 上
		CVertex(vector([1, 1, 1, 1]), vector([0, 1, 0, 0]), vector([0, 0])),
		CVertex(vector([-1, 1, 1, 1]), vector([0, 1, 0, 0]), vector([1, 0])),
		CVertex(vector([1, 1, -1, 1]), vector([0, 1, 0, 0]), vector([0, 1])),
		CVertex(vector([1, 1, -1, 1]), vector([0, 1, 0, 0]), vector([0, 1])),
		CVertex(vector([-1, 1, 1, 1]), vector([0, 1, 0, 0]), vector([1, 0])),
		CVertex(vector([-1, 1, -1, 1]), vector([0, 1, 0, 0]), vector([1, 1])),
		# 下
		CVertex(vector([1, -1, -1, 1]), vector([0, -1, 0, 0]), vector([1, 1])),
		CVertex(vector([-1, -1, 1, 1]), vector([0, -1, 0, 0]), vector([1, 0])),
		CVertex(vector([-1, -1, 1, 1]), vector([0, -1, 0, 0]), vector([0, 0])),
		CVertex(vector([1, -1, 1, 1]), vector([0, -1, 0, 0]), vector([0, 0])),
		CVertex(vector([-1, -1, -1, 1]), vector([0, -1, 0, 0]), vector([0, 1])),
		CVertex(vector([1, -1, -1, 1]), vector([0, -1, 0, 0]), vector([1, 1])),
		# 前
		CVertex(vector([1, 1, 1, 1]), vector([0, 0, 1, 0]), vector([0, 1])),
		CVertex(vector([1, -1, 1, 1]), vector([0, 0, 1, 0]), vector([0, 0])),
		CVertex(vector([-1, 1, 1, 1]), vector([0, 0, 1, 0]), vector([1, 0])),
		CVertex(vector([-1, 1, 1, 1]), vector([0, 0, 1, 0]), vector([0, 1])),
		CVertex(vector([1, -1, 1, 1]), vector([0, 0, 1, 0]), vector([1, 0])),
		CVertex(vector([-1, -1, 1, 1]), vector([0, 0, 1, 0]), vector([1, 1])),
		# 后
		CVertex(vector([-1, 1, -1, 1]), vector([0, 0, -1, 0]), vector([0, 1])),
		CVertex(vector([-1, -1, -1, 1]), vector([0, 0, -1, 0]), vector([0, 0])),
		CVertex(vector([1, -1, -1, 1]), vector([0, 0, -1, 0]), vector([1, 0])),
		CVertex(vector([-1, 1, -1, 1]), vector([0, 0, -1, 0]), vector([0, 1])),
		CVertex(vector([1, -1, -1, 1]), vector([0, 0, -1, 0]), vector([1, 0])),
		CVertex(vector([1, 1, -1, 1]), vector([0, 0, -1, 0]), vector([1, 1])),
		# 左
		CVertex(vector([1, 1, 1, 1]), vector([1, 0, 0, 0]), vector([1, 1])),
		CVertex(vector([1, 1, -1, 1]), vector([1, 0, 0, 0]), vector([0, 1])),
		CVertex(vector([1, -1, -1, 1]), vector([1, 0, 0, 0]), vector([0, 0])),
		CVertex(vector([1, 1, 1, 1]), vector([1, 0, 0, 0]), vector([1, 1])),
		CVertex(vector([1, -1, -1, 1]), vector([1, 0, 0, 0]), vector([0, 0])),
		CVertex(vector([1, -1, 1, 1]), vector([1, 0, 0, 0]), vector([1, 0])),
		# 右
		CVertex(vector([-1, 1, -1, 1]), vector([-1, 0, 0, 0]), vector([1, 1])),
		CVertex(vector([-1, 1, 1, 1]), vector([-1, 0, 0, 0]), vector([0, 1])),
		CVertex(vector([-1, -1, 1, 1]), vector([-1, 0, 0, 0]), vector([0, 0])),
		CVertex(vector([-1, 1, -1, 1]), vector([-1, 0, 0, 0]), vector([1, 1])),
		CVertex(vector([-1, -1, 1, 1]), vector([-1, 0, 0, 0]), vector([0, 0])),
		CVertex(vector([-1, -1, -1, 1]), vector([-1, 0, 0, 0]), vector([1, 0])),
	]

	# 索引
	lIndice = [
		[0, 1, 2],
		[3, 4, 5],

		[6, 7, 8],
		[9, 10, 11],

		[12, 13, 14],
		[15, 16, 17],

		[18, 19, 20],
		[21, 22, 23],

		[24, 25, 26],
		[27, 28, 29],

		[30, 31, 32],
		[33, 34, 35],
	]

	# lVertex = [
	# 	CVertex(vector([0, 2, 0, 1]), vector([1, 0, 0, 0]), vector([0, 0])),
	# 	CVertex(vector([0, 0, 2, 1]), vector([1, 0, 0, 0]), vector([1, 0])),
	# 	CVertex(vector([0, -2, 0, 1]), vector([1, 0, 0, 0]), vector([0, 1])),
	# ]
	#
	# lIndice = [
	# 	[0, 1, 2],
	# ]

	# 纹理（棋盘格）
	mTexture = np.ones((256, 256, 4), dtype="uint8")
	grid_size = 32
	for i in range(8):
		# 每隔1个格子
		for j in [x * 2 for x in range(4)]:
			mTexture[i * grid_size: (i + 1) * grid_size, (j + i % 2) * grid_size: (j + i % 2 + 1) * grid_size, :] = vector([1. / 255, 128. / 255, 1, 1])

	oDevice = device.CDevice(I_WIDTH, I_HEIGHT, mTexture)
	oCameraMgr = camera.CMgr()
	oCamera = oCameraMgr.GetCamera(camera.TYPE_NORMAL)

	oCamera.SetEye(vector([-3, 0, 0, 1]))
	oCamera.SetLookAt(vector([-2, 0, 0, 1]))
	oCamera.SetUp(vector([0, 1, 0, 0]))
	oCamera.SetAspect(1.0)
	oCamera.SetFar(300.0)

	oLight = light.CPointLight(1)
	oLightMgr = light.CMgr()
	oLightMgr.AddLight(oLight)

	oFrame = image.create(I_WIDTH, I_HEIGHT)

	@oGameWindow.event
	def on_draw():
		"""
		每帧调用
		"""

		oGameWindow.clear()
		# oDevice.ClearFrameBuffer(vector([128. / 255, 33. / 255, 78. / 255, 1]))
		oDevice.ClearFrameBuffer(vector([1, 0, 0, 1]))
		oDevice.ClearZBuffer()

		oDevice.DrawMesh(lVertex, lIndice)

		mFrameBuffer = oDevice.GetFramebuffer()

		oFrame.set_data("RGBA", I_WIDTH * 4, mFrameBuffer.tostring())
		oFrame.blit(0, 0)

	pyglet.clock.schedule_interval(lambda dt: None, 1 / 60.0)
	pyglet.app.run()


if __name__ == '__main__':
	main()