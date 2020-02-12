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


def fix_id(n):
    nid = n.attrib['id']

    t = n.find('.//' + ns('text'))
    if t is None:
        return

    # this is a bit questionable, but it doesn't seem that fragments work for svg
    # it kind of jumps somewhere, but it doesn't jump at the start of the cluster/node
    # whereas on text nodes, it works fine
    t.attrib['id'] = nid
    del n.attrib['id']


def run(inp: bytes) -> ET.ElementTree:
    root = ET.fromstring(inp)
    st = ET.SubElement(root, 'style')
    st.text = STYLE

    ## make edge labels follow the curve
    # TODO not sure if should use xlabel?
    figures = root.findall(f'.//{NS}g')
    for fig in figures:
        classes = fig.attrib.get('class', '').split()
        if 'edge' not in classes:
            continue
        edge = fig 
        fix_edge(edge)
    ##

    ## for some reason, svg figures are not nested in graphviz output
    figures = root.findall(f'.//{NS}g')
    for fig in figures:
        classes = fig.attrib.get('class', '').split()
        # right, seems lxml doesn't support contains(@class, "node") ???
        if 'node' not in classes:
            continue
        node = fig

        # find the target clusrer id
        CLUST = '_clust_' # see dotpy subgraph() code
        classes = [c for c in classes if c.startswith(CLUST)]
        if len(classes) == 0:
            continue
        [cls] = classes
        clid = cls[len(CLUST):]
        #

        cluster = root.find(f'.//{NS}g[@id="{clid}"]')
        assert cluster is not None

        # reattach to become its child
        node.getparent().remove(node)
        cluster.append(node)
    ##

    ## for some reason, #fragment links don't work properly against clusters
    ## I think svg only likes them on text
    figures = root.findall(f'.//{NS}g')
    for fig in figures:
        classes = fig.attrib.get('class', '').split()
        if 'cluster' in classes or 'edge' in classes:
            fix_id(fig)
    ##

    return root


def main():
    inp = sys.stdin.read()
    res = run(inp.encode('utf8'))
    ress = ET.tostring(res, pretty_print=True).decode('utf8')
    sys.stdout.write(ress)


# TODO right, also node doesn't know its cluster...

# apparently only these are allowed? https://www.w3.org/TR/SVG11/attindex.html#PresentationAttributes
# TODO add a floating button to drop selection?
# ok, that could be a good way of highlighting...

# huh ok, nice so this sort of works..
STYLE = '''
/* relies on target hack in dotpy!!! */
text:target ~ .node text {
    fill: red;
    font-weight: bold;
}
'''


if __name__ == '__main__':
    main()
