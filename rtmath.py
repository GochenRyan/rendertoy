import numpy as np

def normalize(vec):
	n = np.linalg.norm(vec)
	return vec / n if n!= 0 else vec