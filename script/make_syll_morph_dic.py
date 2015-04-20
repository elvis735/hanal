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
from collections import defaultdict
import logging
import sys

import trie


########
# main #
########
def main(fin, output_stem):
  """
  make syllable-morpheme TRIE dictionary
  :param  fin:          input file
  :param  output_stem:  output file name without extension
  """
  syll_morph_dic = defaultdict(set)
  for line_num, line in enumerate(fin, start=1):
    if line_num % 1000000 == 0:
      logging.info('%dm-th line', (line_num / 1000000))
    line = line.strip()
    if not line:
      continue
    syllable, morph = unicode(line, 'UTF-8').split(u'\t', 1)
    syll_morph_dic[syllable].add(morph)

  trie_root = trie.Node()
  for syllable in sorted(syll_morph_dic.keys()):
    morphs = sorted(list(syll_morph_dic[syllable]))
    trie_root.insert(syllable, u'\t'.join(morphs))

  fout_key = open('%s.trie' % output_stem, 'wb')
  fout_val = open('%s.val' % output_stem, 'w')
  val_serial = 0
  nodes = trie_root.breadth_first_traverse()
  for idx, node in enumerate(nodes):
    logging.debug(u'%d:%s', idx, node)
    val_idx = -1
    if node.value:
      val_idx = val_serial
      val_serial += 1
      fout_val.write((node.value + u'\n').encode('UTF-32LE'))
    fout_key.write(node.pack(val_idx))
  logging.info('Number of nodes: %d', len(nodes))
  logging.info('Number of values: %d', val_serial)


if __name__ == '__main__':
  _PARSER = argparse.ArgumentParser(description='make syllable-morpheme TRIE dictionary')
  _PARSER.add_argument('--input', help='input file <default: stdin>', metavar='FILE', type=file, default=sys.stdin)
  _PARSER.add_argument('-o', '--output', help='output stem', metavar='FILE STEM', required=True)
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
