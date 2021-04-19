import pyglet
from pyglet import image
from defines import *
from geometry import *
import device
import camera

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

I_WINDOW_WIDTH = 800
I_WINDOW_HEIGHT = 600


if __name__ == '__main__':
	game_window = pyglet.window.Window(I_WIDTH, I_HEIGHT)

	#todo: 读取数据

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

	# 纹理（棋盘格）
	aTexture = np.array((256, 256, 4), dtype="uint8") * 255
	grid_size = 32
	for i in range(8):
		# 每隔1个格子
		for j in [x * 2 for x in range(4)]:
			aTexture[i * grid_size: (i + 1) * grid_size, (j + i % 2) * grid_size: (j + i % 2 + 1) * grid_size, :] = vector([1, 128, 255, 255])

	oDevice = device.CDevice(I_WINDOW_WIDTH, I_WINDOW_HEIGHT)
	oCameraMgr = camera.CMgr()
	oCamera = oCameraMgr.GetCamera(camera.I_TYPE_NORMAL)
	mMVP = oCamera.GetViewTrans() * oCamera.GetProjectTrans()
	mNormalTrans = oCamera.GetNormalTrans()

	@game_window.event
	def on_draw():
		"""
		每帧调用
		"""
		print("-----ondraw")

		#todo: 清理帧缓冲、Z缓冲
		oDevice.ClearFrameBuffer(vector([128, 33, 78, 255]))
		oDevice.ClearZBuffer()

		#todo: mvp变换

		#todo: 屏幕映射

		#todo: 光栅化（裁剪、画线or扫描线）

	pyglet.clock.schedule_interval(lambda dt: None, 1 / 60.0)
	pyglet.app.run()