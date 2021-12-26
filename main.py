def main():
	import quintic

	# solvability of the quadratic
	dim = 2
	commutator_depth = 1 # needs nth roots
	print("dim", dim, "with commuting depth", commutator_depth, "solved:", quintic.is_solved(dim, commutator_depth))

	# solvability of the cubic
	dim = 3
	commutator_depth = 2 # needs 2 nested nth roots
	print("dim", dim, "with commuting depth", commutator_depth, "solved:", quintic.is_solved(dim, commutator_depth))

	# solvability of the quadric
	dim = 4
	commutator_depth = 3 # needs 3 nested nth roots
	print("dim", dim, "with commuting depth", commutator_depth, "solved:", quintic.is_solved(dim, commutator_depth))

	### To really prove the unsolvability of the quintic, 
	### we need to show that we can produce a non trivial commutator of arbitrary depth.
	### We choose that they all will have the result ('3', '1', '2', '4', '5')

	print()
	c_0 = quintic.Permutation(5, [2,0,1,3,4])
	print("interpreting", c_0, "as a commutator of any depth")

	depth = 2
	ordered_set_of_perms = []
	while True:
		perms = quintic.as_generalized_commutator(c_0, depth)
		assert(c_0 == quintic.derive_end_commmutator(perms))
		perms = quintic.unique_sorted_perm_list(perms)
		if quintic.lists_equal(perms, ordered_set_of_perms):
			break
		ordered_set_of_perms = perms
		depth += 1

	print("unique set of permutations needed for commutator of any depth: ")
	[print(p) for p in ordered_set_of_perms]
	print("reached at depth", depth-1)

def make_figures():
	import display
	display.make_commutator_figure(2, 1)
	display.make_commutator_figure(3, 2)
	display.make_commutator_figure(4, 3)
	display.make_commutator_figure(5, 2)
	display.show()

if __name__ == "__main__":
	main()
	make_figures()
