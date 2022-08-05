#!/usr/bin/python3

import requests
import json
import dewiki
import sys


def request_wikipedia(page: str):
	URL = "https://fr.wikipedia.org/w/api.php"

	PARAMS = {
		"action": "parse",
		"page": page,
		"prop": "wikitext",
		"format": "json",
		"redirects": "true"
	}

	try:
		res = requests.get(url=URL, params=PARAMS)
		res.raise_for_status()
	except requests.HTTPError as e:
		raise e
	try:
		data = json.loads(res.text)
	except json.decoder.JSONDecodeError as e:
		raise e
	if data.get("error") is not None:
		raise Exception(data["error"]["info"])
	return (dewiki.from_string(data["parse"]["wikitext"]["*"]))


def main():
	if (len(sys.argv) == 2):
		try:
			wiki_data = request_wikipedia(sys.argv[1])
		except Exception as e:
			return print(e)
		try:
			file = open("{}.wiki".format(sys.argv[1]), "w")
			file.write(wiki_data)
			file.close
		except Exception as e:
			return print(e)
	else:
		print("Error: wrong amount of arguments")


if __name__ == '__main__':
	main()
