
import unittest

from spellcheck import Trie, SpellChecker

class TestTrie(unittest.TestCase):

	def setUp(self):
		self.trie = Trie()

	def tearDown(self):
		self.trie.reset()

	def test_add_contains(self):
		self.trie.add('bayern')
		self.trie.add('chelsea')

		self.assertTrue(self.trie.contains('bayern'))
		self.assertTrue(self.trie.contains('chelsea'))


	def test_contains_partial_word(self):
		self.trie.add('ban')
		self.trie.add('banana')

		self.assertTrue(self.trie.contains('ban'))
		self.assertTrue(self.trie.contains('banana'))

	def test_not_contains(self):
		self.trie.add('ban')

		self.assertFalse(self.trie.contains('banana'))
		self.assertFalse(self.trie.contains('aardvark'))

	def test_lowercase(self):
		self.trie.add('BAN')

		self.assertTrue(self.trie.contains('BAN'))
		self.assertTrue(self.trie.contains('ban'))

class TestSpellcheckTrie(unittest.TestCase):
	def setUp(self):
		self.trie = Trie()
		self.checker = SpellChecker(self.trie)

	def tearDown(self):
		self.trie.reset()
		self.checker.reset()

	def test_exact_match(self):
		self.trie.add('bayern')

		self.assertEqual(self.checker.spellcheck('bayern'), 'bayern')

	def test_miss(self):
		self.trie.add('bayern')

		self.assertFalse(self.checker.spellcheck('byern'))

	def test_vowel(self):
		self.trie.add('bayern')

		self.assertEqual(self.checker.spellcheck('bayarn'), 'bayern')

	def test_vowel_miss(self):
		self.trie.add('bayern')

		self.assertFalse(self.checker.spellcheck('barn'))

	def test_vowel_last_letter(self):
		self.trie.add('ygapo')

		self.assertEqual(self.checker.spellcheck('ygapu'), 'ygapo')

	def test_repeating_chars(self):
		self.trie.add('job')

		self.assertEqual(self.checker.spellcheck('jjoobbb'), 'job')

	def test_repeating_chars_smaller_word(self):
		self.trie.add('cuppy')
		self.trie.add('cuphead')

		self.assertEqual(self.checker.spellcheck('ccoppphead'), 'cuphead')

	def test_spellcheck_backtrack(self):
		self.trie.add('pea')
		self.trie.add('peep')
		self.trie.add('peeper')
		self.trie.add('peephole')
		self.trie.add('peon')
		self.trie.add('peonage')
		self.trie.add('people')

		self.assertEqual(self.checker.spellcheck('peepple'), 'people')

	def test_challenge_words(self):
		self.trie.add('conspiracy')
		self.trie.add('sheep')
		self.trie.add('people')
		self.trie.add('wake')

		self.assertEqual(self.checker.spellcheck('CUNsperrICY'), 'conspiracy')
		self.assertEqual(self.checker.spellcheck('sheeeeep'), 'sheep')
		self.assertEqual(self.checker.spellcheck('peepple'), 'people')
		self.assertEqual(self.checker.spellcheck('weke'), 'wake')
		self.assertEqual(self.checker.spellcheck('sheeple'), 'sheep')

	def test_vowels_and_repeating_letters(self):
		self.trie.add('sdrucciola')

		self.assertEqual(self.checker.spellcheck('sdrucciila'), 'sdrucciola')

if __name__ == '__main__':
	unittest.main()
