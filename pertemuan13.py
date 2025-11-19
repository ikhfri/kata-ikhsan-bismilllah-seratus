with open("data.txt", "f") as data:
	data.write('Hello')
	data.seek(0)
	print(data.read())