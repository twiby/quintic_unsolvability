import quintic
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def make_commutator_figure(dim, depth):
	fig = plt.figure()
	fig.suptitle("commutators for dimension "+str(dim), fontweight="bold")
	for d in range(depth + 1):
		ax = fig.add_subplot(1,depth+1, d+1)
		if d == 0:
			title = "permutations"
		else:
			title = "commutators"
		for dd in range(2, d+1):
			title += " of commutators\n"
		ax.set_title(title)

		perms = list(quintic.unique_generalized_commutators(d, dim))
		perms = quintic.unique_sorted_perm_list(perms)
		image = np.zeros((len(perms), dim))
		for p in range(len(perms)):
			image[p, :] = perms[p].idx
		plt.imshow(image)

def show():
	plt.show()

if __name__ == "__main__":
	make_commutator_figure(2, 1)
	make_commutator_figure(3, 2)
	make_commutator_figure(4, 3)
	make_commutator_figure(5, 4)
	plt.show()