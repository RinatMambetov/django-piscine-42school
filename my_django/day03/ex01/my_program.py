#!/usr/bin/python3

from path import Path


def main():
	try:
		Path.makedirs('my_dir')
	except FileExistsError as e:
		print(e)
	Path.touch('my_dir/my_file')
	file = Path('my_dir/my_file')
	file.write_lines(['Hello', 'world!'])
	print(file.read_text())


if __name__ == '__main__':
	main()
