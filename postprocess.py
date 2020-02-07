#!/usr/bin/env python3
from pathlib import Path
import sys

from lxml import etree as ET # type: ignore

NS = '{http://www.w3.org/2000/svg}'
def ns(s):
    return NS + s


def fix_edge(e):
    eid = e.attrib['id']

    lid = 'label_' + eid

    p = e.find('.//' + ns('path'))

    # if eid == 'edge28':
    #     # print(e.find_all(ns('path')), file=sys.stderr)
    #     print(p, file=sys.stderr)
    #     print(eid, file=sys.stderr)
    if p is None:
        return

    t = e.find('.//' + ns('text'))
    if t is None:
        return


    p.attrib['id'] = lid

    del t.attrib['x']
    del t.attrib['y']
    del t.attrib['text-anchor']
    label = t.text
    t.text = None
    tp = ET.SubElement(t, 'textPath')
    tp.attrib['href'] = '#' + lid
    tp.attrib['startOffset'] = '7%' # TODO ok, maybe needs to be configurable..
    tp.attrib['side'] = 'right'
    tp.text = label
    # TODO url?


def run(inp: bytes) -> ET.ElementTree:
    root = ET.fromstring(inp)
    edges = root.findall(f'.//{NS}g[@class="edge"]')

    for e in edges:
        fix_edge(e)

    return root


def main():
    inp = sys.stdin.read()
    res = run(inp.encode('utf8'))
    ress = ET.tostring(res, pretty_print=True).decode('utf8')
    sys.stdout.write(ress)


if __name__ == '__main__':
    main()
