#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
make syllable-morpheme TRIE dictionary
"""
__author__ = 'krikit(krikit@naver.com)'
__copyright__ = 'Copyright (C) 2014-2015, krikit. All rights reserved. BSD 2-Clause License'


###########
# imports #
###########
import argparse
import logging
import sys

import trie


########
# main #
########
def main(fin, fout):
  """
  make syllable-morpheme TRIE dictionary
  :param  fin:   input file
  :param  fout:  output file
  """
  trie_root = trie.Node()
  prev_line = ''
  for line_num, line in enumerate(fin, start=1):
    line = line.strip()
    if not line:
      continue
    if line == prev_line:
      logging.error('Duplicate line at (%d): %s', line_num, line)
      sys.exit(1)
    elif line < prev_line:
      logging.error('File is not sorted (%d): %s', line_num, line)
      sys.exit(2)
    prev_line = line
    syllable, morph = unicode(line, 'UTF-8').split(u'\t', 1)
    trie.insert(trie_root, syllable, morph)

  # TODO(krikit): flatten tree structured trie into single array
  nodes = trie.breadth_first_traverse(trie_root)
  for idx, node in enumerate(nodes):
    logging.debug(u'%d:%s', idx, node)


if __name__ == '__main__':
  _PARSER = argparse.ArgumentParser(description='make syllable-morpheme TRIE dictionary')
  _PARSER.add_argument('--input', help='input file <default: stdin>', metavar='FILE', type=file, default=sys.stdin)
  _PARSER.add_argument('--output', help='output file <default: stdout>', metavar='FILE',
                       type=argparse.FileType('w'), default=sys.stdout)
  _PARSER.add_argument('--log-level', help='set logging level', metavar='LEVEL')
  _PARSER.add_argument('--log-file', help='set log file <default: stderr>', metavar='FILE')
  _ARGS = _PARSER.parse_args()
  _LOG_CFG = {'format':'[%(asctime)-15s] %(levelname)-8s %(message)s', 'datefmt':'%Y-%m-%d %H:%M:%S'}
  if _ARGS.log_level:
    _LOG_CFG['level'] = eval('logging.%s' % _ARGS.log_level.upper())    # pylint: disable=W0123
  if _ARGS.log_file:
    _LOG_CFG['filename'] = _ARGS.log_file
  logging.basicConfig(**_LOG_CFG)    # pylint: disable=W0142
  main(_ARGS.input, _ARGS.output)
