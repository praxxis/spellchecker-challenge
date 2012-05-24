from collections import defaultdict
from difflib import SequenceMatcher
import sys

class TrieNode(object):
	def __init__(self):
		self.value = None
		self.parent = None
		self.end = False
		self.leafs = defaultdict(TrieNode)

	def add(self, word, value=None, parent=None):

		self.parent = parent
		self.value = value

		if word:
			first, rest = word[0], word[1:]

			self.leafs[first].add(rest, first, self)
		else:
			# reached the end of the letters, flag that it is a full word
			self.end = True

	def contains(self, word):

		# last node and at the end of the word, must be an exact match
		if self.end and not word:
			return True

		first, rest = word[0], word[1:]

		if first in self.leafs:

			# this letter exists, continue the search down the trie
			return self.leafs[first].contains(rest)
		else:
			return False

	def walk(self):
		string = self.value
		parent = self.parent

		# build the string by walking back along the tree until hitting the root node
		while parent and parent.parent:
			string = parent.value + string
			parent = parent.parent

		return string

class Trie(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.root = TrieNode()

	def add(self, word):
		self.root.add(word.strip().lower())

	def contains(self, word):
		return self.root.contains(word.strip().lower())

class SpellChecker(object):

	VOWELS = ['a', 'e', 'i', 'o', 'u']

	def __init__(self, trie):
		self.trie = trie

		self.reset()

	def reset(self):
		self.suggestions = []

	def word_similarity(self, a, b):
		return SequenceMatcher(a=a, b=b).ratio()

	def find_best_suggestion(self, word, suggestions):

		# try and find the suggestion most similar to the word provided
		suggestions = [suggestion.walk() for suggestion in suggestions]
		sorted_suggestions = sorted([(self.word_similarity(word, suggestion), suggestion) for suggestion in suggestions])

		# the list is sorted in ascending order, so pick the last match as it has the highest similarity
		return sorted_suggestions[-1][1]

	def spellcheck(self, word):

		word = word.lower()

		suggestions = self.generate_suggestions(word, self.trie.root)

		if not suggestions:
			return False

		# because the suggestion check will pessimistically check for suggestions the actual
		# word, if it was correctly spelled, will be the last element in the suggestions list
		if suggestions[-1].walk() == word:
			return word

		return self.find_best_suggestion(word, suggestions)

	def generate_suggestions(self, word, branch):

		suggestions = []

		i = 0

		while i < len(word):
			char = word[i]

			# check for potential incorrect vowels
			if char in self.VOWELS:
				# omit the current vowel
				matches = [letter for letter in self.VOWELS if letter != char]

				rest = word[i+1:]

				for vowel in matches:
					# if a leaf for alternate vowel exists, see if we can match the rest of the word off it
					if vowel in branch.leafs:
						suggestions += self.generate_suggestions(rest, branch.leafs[vowel])

			# see if the character is part of a repeating sequence
			if i > 0 and char == word[i-1]:
				# if it is part of a sequence, generate suggestions for each letter in the sequence
				# the "word" starts as the first repeating letter, then
				# reduces by one letter and any remaining letters each step
				# for example, checking sheeeep: -> shee, eep -> shee, ep -> shee, p
				try:
					x = i
					while char == word[x-1]:
						x += 1
						suggestions += self.generate_suggestions(word[x:], branch)

				except IndexError:
					# the string repeated letters until its end so there were no more
					# letters to find branches for
					pass

			if not char in branch.leafs:
				# dead end: the letter does not exist in the current branches leafs so
				# there is no word using this combination of letters and thus no suggestion
				break

			# set the branch to the leaf that is the character we're looking at
			branch = branch.leafs[char]
			i += 1

		# if we've reached the end of the search word we've found
		# an actual word add it to the suggestions list
		if branch.end:
			suggestions.append(branch)

		return suggestions

if __name__ == '__main__':

	DICTIONARY = '/usr/share/dict/words'

	trie = Trie()
	checker = SpellChecker(trie)

	with open(DICTIONARY, 'r') as f:
		for line in f:
			trie.add(line)

	prompt = ''
	if sys.stdin.isatty():
		# we only want a prompt when called directly
		prompt = '>'

	while 1:
		try:
			input = raw_input(prompt)

			if not input:
				break

			result = checker.spellcheck(input)

			if result:
				print result
			else:
				print 'NO SUGGESTION'

		except (KeyboardInterrupt, EOFError):
			break