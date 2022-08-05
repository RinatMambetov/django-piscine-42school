def ft_print_nums():
	file = open("numbers.txt", "r")
	str = file.read()
	str = str.strip()
	list = str.split(",")
	for num in list:
		print(num)
	file.close

if __name__ == '__main__':
    ft_print_nums()
