import cProfile
import pstats
import os
# 性能分析装饰器定义
def DocProfile(filename):
	def Wrapper(func):
		def ProfiledFunc(*args, **kwargs):
			profile = cProfile.Profile()
			print("profile start")
			profile.enable()
			result = func(*args, **kwargs)
			profile.disable()
			# Sort stat by internal time.
			sortby = "tottime"
			ps = pstats.Stats(profile).sort_stats(sortby)
			ps.dump_stats(filename)
			print("profile finish")
			return result
		return ProfiledFunc
	return Wrapper