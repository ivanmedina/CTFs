import numpy as np

a = np.array([0], dtype=int)
# val = int(input("This hammer hits so hard it creates negative matter\n"))

val = int(2635249153387078802)

if val == -1:
	exit()
a[0] = val
a[0] = (a[0] * 7) + 1
print(a[0])
if a[0] == -1:
	print("flag!")




# 1844674407370955161

# 18446744073709551616

# -5534023222112865488

# 18446744073709551616/7
# 2635249153387078802

# kqctf{2635249153387078802}
