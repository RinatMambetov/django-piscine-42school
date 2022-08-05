import sys

def ft_print_capital_city(key_state: str):
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
    key_state_short = states.get(key_state)
    if not key_state_short:
        print("Unknown state")
        return
    print(capital_cities.get(key_state_short))

def main():
    if len(sys.argv) == 2:
        ft_print_capital_city(sys.argv[1])

if __name__ == '__main__':
    main()
