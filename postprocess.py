#!/usr/bin/env python3
from pathlib import Path
from lxml import etree as ET

def ns(s):
    return '{http://www.w3.org/2000/svg}' + s


def run(inp: Path) -> ET.ElementTree:
    root = ET.parse(str(inp))
    # TODO meh
    elems = root.findall('.//{http://www.w3.org/2000/svg}g/{http://www.w3.org/2000/svg}text')
    [ce] = [e for e in elems if e.text == 'Calendar']
    c = ce.getparent()
    cp = c.find(ns('path'))
    cp.attrib['id'] = 'hello'

    ct = ce

    del ct.attrib['x']
    del ct.attrib['y']
    del ct.attrib['text-anchor']
    label = ct.text
    ct.text = None
    tp = ET.SubElement(ct, 'textPath')
    tp.attrib['href'] = f'#hello'
    tp.attrib['startOffset'] = '10%'
    tp.attrib['side'] = 'right'
    tp.text = label
    # TODO url?

    return root

def main():
    res = run(Path('infra.svg'))
    Path('patched.svg').write_bytes(ET.tostring(res, pretty_print=True))


if __name__ == '__main__':
    main()
