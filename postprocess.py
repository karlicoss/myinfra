#!/usr/bin/env python3
from pathlib import Path
from lxml import etree as ET # type: ignore

NS = '{http://www.w3.org/2000/svg}'
def ns(s):
    return NS + s


def fix_edge(e):
    eid = e.attrib['id']
    lid = 'label_' + eid

    p = e.find(ns('path'))

    if p is None:
        return

    t = e.find(ns('text'))
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
    tp.attrib['startOffset'] = '10%'
    tp.attrib['side'] = 'right'
    tp.text = label
    # TODO url?


def run(inp: Path) -> ET.ElementTree:
    root = ET.parse(str(inp))
    edges = root.findall(f'.//{NS}g[@class="edge"]')

    for e in edges:
        fix_edge(e)

    return root


def main():
    res = run(Path('infra.svg'))
    Path('patched.svg').write_bytes(ET.tostring(res, pretty_print=True))


if __name__ == '__main__':
    main()
