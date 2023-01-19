x = 2
y = 2
def generate_uid():
	uid = 3 ** 2
	return uid

def generate_another_uid():
	uid = 4 ** 2
	return uid
# if user y has same id as another user (x)
if y == x:
	print("in 1st if statement")
	# generate an id until y != x
	while y == x:
		print("in while loop")
		y = generate_uid()
		print(y)
		if y == x:
			print("in 2nd if statement")
			y += 1
			print(y)

print()
print()

y = x
if y == x:
	print("in 1st if statement")
	# generate an id until y != x
	while y == x:
		print("in while loop")
		y = generate_uid()
		print(y)
		