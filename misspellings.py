
import sys
from spellcheck import Trie
import random

DEBUG = True

VOWELS = ['a', 'e', 'i', 'o', 'u']

def generate_misspelling(leafs):

	word = ''

	# pick a random branch to start walking down
	letter = random.choice(leafs.keys())

	leaf = leafs[letter]

	if not leaf.end or (leaf.end and leaf.leafs):
		word += generate_misspelling(leaf.leafs)

	if DEBUG and leaf.end:
		sys.stderr.write('-' + leaf.walk() + "\n")

	return mutate_letter(letter) + word

def mutate_letter(letter):

	rand = random.randint(1, 100)

	# because we don't want to end up with crazy
	# words, keep the letter the same most of the time
	if 1 <= rand <= 30 and letter in VOWELS:
		return random.choice([vowel for vowel in VOWELS if vowel != letter])
	elif 31 <= rand <= 40:
		return letter * random.randint(2, 3)
	elif 41 <= rand <= 100:
		return letter

	return letter

if __name__ == '__main__':
	DICTIONARY = '/usr/share/dict/words'

	trie = Trie()

	with open(DICTIONARY, 'r') as f:
		for line in f:
			trie.add(line)

	leafs = trie.root.leafs

	for i in range(20):
		misspelling = generate_misspelling(leafs)

		if DEBUG:
			sys.stderr.write('+' + misspelling + "\n")

		print misspelling


