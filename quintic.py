#### UNSOLVABILITY OF THE QUINTIC ####

def lists_equal(l1, l2):
	if len(l1) != len(l2):
		return False
	for i in range(len(l1)):
		if l1[i] != l2[i]:
			return False
	return True

class Permutation:
	def __init__(self, N, idx):
		self.N = N
		self.idx = idx

	def apply(self, l=None):
		if l is None:
			l = [str(n+1) for n in range(self.N)]
		return tuple([l[i] for i in self.idx])

	def revert(self):
		return Permutation(self.N, sorted(range(self.N), key=self.idx.__getitem__))

	def augment(self, n):
		return Permutation(self.N+1, [n] + self.idx)

	def compose(self, P):
		return Permutation(self.N, P.apply(self.idx))

	def __str__(self):
		return str(self.apply())

	def __eq__(self, obj):
		return lists_equal(self.idx, obj.idx)

	def __lt__(self, obj):
		if self.N != obj.N:
			raise ValueError("cannot compare permutations of different dimensions")
		if self == obj:
			return False
		for i in range(self.N):
			if self.idx[i] == obj.idx[i]:
				continue
			return self.idx[i] < obj.idx[i]


def permutations_from_idx(idx):
	if len(idx) == 1:
		yield Permutation(1, idx)
	else:
		for i in range(len(idx)):
			for perm in permutations_from_idx(idx[:i] + idx[i+1:]):
				yield perm.augment(idx[i])

def permutations(N):
	for p in permutations_from_idx(list(range(N))):
		yield p

def commutator(P1, P2):
	return P1.compose(P2).compose(P1.revert()).compose(P2.revert())


def generalized_commutators(Depth, N):
	if Depth == 0:
		for p in permutations(N):
			yield p
	else:
		commutators = [c for c in unique_generalized_commutators(Depth-1, N)]
		for c1 in commutators:
			for c2 in commutators:
				yield commutator(c1, c2)

def unique_generalized_commutators(Depth, N):
	permuts = []
	for c in generalized_commutators(Depth, N):
		a = c.apply()
		if not a in permuts:
			permuts.append(a)
			yield c

def is_solved(dim, commutator_depth):
	all_commutations = [c.apply() for c in unique_generalized_commutators(commutator_depth, dim)]

	for c in all_commutations:
		if c != tuple([str(n+1) for n in range(dim)]):
			return (False, c)
	return True


# solvability of the quadratic
dim = 2
commutator_depth = 1 # needs nth roots
print("dim", dim, "with commuting depth", commutator_depth, "solved:", is_solved(dim, commutator_depth))

# solvability of the cubic
dim = 3
commutator_depth = 2 # needs 2 nested nth roots
print("dim", dim, "with commuting depth", commutator_depth, "solved:", is_solved(dim, commutator_depth))

# solvability of the quadric
dim = 4
commutator_depth = 3 # needs 3 nested nth roots
print("dim", dim, "with commuting depth", commutator_depth, "solved:", is_solved(dim, commutator_depth))

### To really prove the unsolvability of the quintic, 
### we need to show that we can produce a non trivial commutator of arbitrary depth.
### We choose that they all will have the result ('3', '1', '2', '4', '5')

def derive_commutators(p):
	assert(len(p) % 2 == 0)
	return [commutator(p[2*i], p[2*i+1]) for i in range(int(len(p)//2))]

def derive_end_commmutator(p):
	assert(len(p) % 2 == 0)
	while len(p) > 1:
		assert(len(p) % 2 == 0)
		p = derive_commutators(p)
	return p[0]

def switcher(idx_1, idx_2):
	idx = [n for n in range(5)]
	idx[idx_1] = idx_2
	idx[idx_2] = idx_1
	return Permutation(5, idx)

def as_commutator(p):
	non_fixed_points = []
	fixed_points = []
	for i in range(5):
		if p.idx[i] == i:
			fixed_points.append(i)
		else:
			non_fixed_points.append(p.idx[i])

	parity = bool(non_fixed_points[0] > non_fixed_points[1])

	s_1 = switcher(non_fixed_points[0], fixed_points[0])
	if parity:
		s_2 = switcher(non_fixed_points[1], fixed_points[1])
	else:
		s_2 = switcher(non_fixed_points[2], fixed_points[1])

	p_1 = s_1.compose(p).compose(s_1)
	p_2 = s_2.compose(p.revert()).compose(s_2)

	return p_1, p_2

def as_commutators(p):
	perms = []
	for i in range(len(p)):
		p1, p2 = as_commutator(p[i])
		perms.append(p1)
		perms.append(p2)
	return perms

def as_generalized_commutator(p, depth):
	perms = [p]
	for d in range(depth):
		perms = as_commutators(perms)
	return perms

def unique_sorted_perm_list(perms):
	unique_perms = []
	for p in perms:
		if not p in unique_perms:
			unique_perms.append(p)
	return sorted(unique_perms)


print()
c_0 = Permutation(5, [2,0,1,3,4])
print("interpreting", c_0, "as a commutator of any depth")

depth = 2
ordered_set_of_perms = []
while True:
	perms = as_generalized_commutator(c_0, depth)
	assert(c_0 == derive_end_commmutator(perms))
	perms = unique_sorted_perm_list(perms)
	if lists_equal(perms, ordered_set_of_perms):
		break
	ordered_set_of_perms = perms
	depth += 1

print("unique set of permutations needed for commutator of any depth: ")
[print(p) for p in ordered_set_of_perms]
print("reached at depth", depth-1)
