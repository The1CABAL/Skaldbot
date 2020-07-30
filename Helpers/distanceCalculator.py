
def calculate_distance(system1, system2):
	x1 = system1[0]
	y1 = system1[1]
	z1 = system1[2]
	x2 = system2[0]
	y2 = system2[1]
	z2 = system2[2]

	distance = sqrt.math((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
	
	return distance