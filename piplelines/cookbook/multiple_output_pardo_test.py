

"""Test for the multiple_output_pardo example."""

import logging
import re
import tempfile
import unittest

from apache_beam.examples.cookbook import multiple_output_pardo


class MultipleOutputParDo(unittest.TestCase):

  SAMPLE_TEXT = 'A whole new world\nA new fantastic point of view'
  EXPECTED_SHORT_WORDS = [('A', 2), ('new', 2), ('of', 1)]
  EXPECTED_WORDS = [
      ('whole', 1), ('world', 1), ('fantastic', 1), ('point', 1), ('view', 1)]

  def create_temp_file(self, contents):
    with tempfile.NamedTemporaryFile(delete=False) as f:
      f.write(contents)
      return f.name

  def get_wordcount_results(self, temp_path):
    results = []
    with open(temp_path) as result_file:
      for line in result_file:
        match = re.search(r'([A-Za-z]+): ([0-9]+)', line)
        if match is not None:
          results.append((match.group(1), int(match.group(2))))
    return results

  def test_multiple_output_pardo(self):
    temp_path = self.create_temp_file(self.SAMPLE_TEXT)
    result_prefix = temp_path + '.result'

    multiple_output_pardo.run([
        '--input=%s*' % temp_path,
        '--output=%s' % result_prefix]).wait_until_finish()

    expected_char_count = len(''.join(self.SAMPLE_TEXT.split('\n')))
    with open(result_prefix + '-chars-00000-of-00001') as f:
      contents = f.read()
      self.assertEqual(expected_char_count, int(contents))

    short_words = self.get_wordcount_results(
        result_prefix + '-short-words-00000-of-00001')
    self.assertEqual(sorted(short_words), sorted(self.EXPECTED_SHORT_WORDS))

    words = self.get_wordcount_results(result_prefix + '-words-00000-of-00001')
    self.assertEqual(sorted(words), sorted(self.EXPECTED_WORDS))


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()
