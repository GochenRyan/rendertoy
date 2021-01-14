import pyglet
from pyglet import image
from defines import *

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


if __name__ == '__main__':
	game_window = pyglet.window.Window(I_WIDTH, I_HEIGHT)

	#todo: 读取数据

	@game_window.event
	def on_draw():
		"""
		每帧调用
		"""
		print("-----ondraw")

		#todo: 清理帧缓冲、Z缓冲

		#todo: mvp变换

		#todo: 屏幕映射

		#todo: 光栅化（裁剪、画线or扫描线）

	pyglet.clock.schedule_interval(lambda dt: None, 1 / 60.0)
	pyglet.app.run()