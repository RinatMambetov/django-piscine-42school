def ft_get_key(d: dict, value: str):
	for key, val in d.items():
		if val == value:
			return key
	return None

def ft_get_long_dict(d: dict):
	years = []
	names = []

	for musician in d:
		years.append(musician[0])
		names.append(musician[1])
	return dict(zip(years, names))

def ft_print_dict(d: dict):
	for key, value in d.items():
		print(value, ":", key)

def ft_list_to_dict():
	d = [
		('Hendrix'		, '1942'),
		('Allman'		, '1946'),
		('King'			, '1925'),
        ('Clapton'		, '1945'),
        ('Johnson'		, '1911'),
        ('Berry'		, '1926'),
        ('Vaughan'		, '1954'),
        ('Cooder'		, '1947'),
        ('Page'			, '1944'),
        ('Richards'		, '1943'),
        ('Hammett'		, '1962'),
        ('Cobain'		, '1967'),
        ('Garcia'		, '1942'),
        ('Beck'			, '1944'),
        ('Santana'		, '1947'),
        ('Ramone'		, '1948'),
        ('White'		, '1975'),
        ('Frusciante'	, '1970'),
        ('Thompson'		, '1949'),
        ('Burton'		, '1939')
	]
	musicians_dict_short = {}

	musicians_dict_long = ft_get_long_dict(d)
	for key, value in musicians_dict_long.items():
		if not value in musicians_dict_short.values():
			musicians_dict_short[key] = value
		else:
			if ft_get_key(musicians_dict_short, value) is not None:
				old_key = ft_get_key(musicians_dict_short, value)
			new_key = old_key + " " + key
			musicians_dict_short[new_key] = musicians_dict_short.pop(old_key)
	ft_print_dict(musicians_dict_short)

if __name__ == '__main__':
    ft_list_to_dict()
