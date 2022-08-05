import sys

def ft_get_key(d: dict, value: str):
    for key, item in d.items():
        if item == value:
            return key
    return None

def ft_print_state(value: str):
    states = {
        "Oregon":		"OR",
        "Alabama":		"AL",
        "New Jersey":	"NJ",
        "Colorado":		"CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    key = ft_get_key(capital_cities, value)
    if key is None:
        print("Unknown capital city")
        return
    print(ft_get_key(states, key))

def main():
    if len(sys.argv) == 2:
        ft_print_state(sys.argv[1])

if __name__ == '__main__':
    main()
