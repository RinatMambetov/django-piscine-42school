import sys

def ft_get_list(arg: str):
	list = arg.split(", ")
	list_stripped = [item.strip() for item in list]
	return list_stripped

def ft_get_city(state: str, states: dict, capital_cities: dict):
	state = state.title()
	key_state_short = states.get(state)
	if not key_state_short:
		return None
	else:
		return capital_cities.get(key_state_short)

def ft_get_key(d: dict, value: str):
	for key, item in d.items():
		if item == value:
			return key
	return None

def ft_get_state(city: str, states: dict, capital_cities: dict):
	key = ft_get_key(capital_cities, city)
	if key is None:
		return None
	else:
		return ft_get_key(states, key)

def ft_all_in(arg: str):
	states = {
		"Oregon":		"OR",
		"Alabama":		"AL",
		"New Jersey":	"NJ",
		"Colorado":		"CO",
    }
	capital_cities = {
    	"OR":	"Salem",
    	"AL":	"Montgomery",
    	"NJ":	"Trenton",
    	"CO":	"Denver",
    }

	arg_list = ft_get_list(arg)
	for item in arg_list:
		if ft_get_city(item, states, capital_cities) is not None:
			print(ft_get_city(item, states, capital_cities) + " is the capital of " + item.title())
		elif ft_get_state(item.capitalize(), states, capital_cities) is not None:
			print(item.capitalize() + " is the capital of " + ft_get_state(item.capitalize(), states, capital_cities))
		else:
			if item:
				print(item + " is neither a capital city nor a state")

def main():
	if len(sys.argv) == 2:
		ft_all_in(sys.argv[1])

if __name__ == '__main__':
    main()
