import pyglet
from pyglet import image
from defines import *


if __name__ == '__main__':
	game_window = pyglet.window.Window(I_WIDTH, I_HEIGHT)

	#todo: 读取数据

	@game_window.event
	def on_draw():
		"""
		每帧调用
		"""

		#todo: 清理帧缓冲、Z缓冲

		#todo: mvp变换

		#todo: 屏幕映射

		#todo: 光栅化（裁剪、画线or扫描线）

	pyglet.app.run()