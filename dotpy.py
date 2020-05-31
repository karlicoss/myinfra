import sys
from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union, Any


# TODO move this away from core?
cylinder = 'cylinder'
diamond = 'diamond'
point = 'point'
star  = 'star'

dashed = 'dashed'
dotted = 'dotted'
filled = 'filled'
rounded = 'rounded'

lightblue = 'lightblue'
darkgreen = 'darkgreen'
black  = 'black'
blue   = 'blue'
gray   = 'gray'
green  = 'green'
orange = 'orange'
red    = 'red'
purple = 'purple'

record = dict(shape='record')
noconstraint = dict(constraint='false')
invisible = dict(style='invisible')

_MODULE_NAME: Optional[str] = None


def _id2obj() -> Dict[int, Any]:
    # todo document/test
    assert _MODULE_NAME is not None, 'Looks like you forgot to init()'
    globs = vars(sys.modules[_MODULE_NAME])
    return {id(v): k for k, v in globs.items()}


def init(mname: str):
    global _MODULE_NAME
    _MODULE_NAME = mname


def get_name(obj: Any) -> str:
    m = _id2obj()
    oid = id(obj)
    assert oid in m, obj
    return m[oid]


Data = Union[str, Iterable[str]]


class Graph(NamedTuple):
    name_: Optional[str]
    cluster: bool
    raw: Data
    kind: str = 'subgraph'

    @property
    def name(self) -> str:
        sn = self.name_
        if sn is not None:
            return sn
        else:
            return get_name(self)

    def render(self) -> Iterable[str]:
        name = self.name
        mcl = 'cluster_' if self.cluster else ''
        yield f'{self.kind} {mcl}{name}' + ' {'
        for x in [self.raw] if isinstance(self.raw, str) else self.raw:
            # TODO handle multiline stuff properly?
            yield '  ' + x
        yield '}'
Subgraph = Graph # todo deprecate?


Extra = Dict[str, str]
class Node(NamedTuple):
    name_: Optional[str]
    extra: Dict
    set_class: bool = False # meh

    @property
    def name(self) -> str:
        sn = self.name_
        if sn is not None:
            if ' ' in sn:
                # TODO check if already quoted first?
                sn = f'"{sn}"'
            return sn
        else:
            return get_name(self)

    def render(self) -> Iterable[str]:
        extra = {**self.extra}

        if self.set_class:
            assert 'class' not in extra, extra
            extra['class'] = self.name

        if len(extra) == 0:
            yield self.name
            return

        yield f'{self.name} ['
        for l in _render(**extra, self_=self):
            yield '  ' + l
        yield ']'


# todo label is actually name?
Label = str
Nodish = Union[Node, Label]
class Edge(NamedTuple):
    f: Nodish
    t: Nodish
    extra: Dict

    def render(self) -> Iterable[str]:
        f = self.f
        t = self.t
        kwargs = self.extra

        fn = f if isinstance(f, str) else f.name
        tn = t if isinstance(t, str) else t.name
        extras = '' if len(kwargs) == 0 else ' [' + '\n'.join(_render(**kwargs)) + ']'
        yield f'{fn} -> {tn}' + extras

from typing import Callable
Prop = Union[str, Callable[[], str]]


def _render(*args: str, self_=None, **kwargs):
    def handle(x: Prop) -> str:
        if isinstance(x, Callable):
            x = x(self_=self_)
        assert isinstance(x, str), x

        # meh. this is for HTML labels...
        if x[:1] + x[-1:] == '<>':
            return x
        else:
            return f'"{x}"'

    return list(args) + [f'{k}={handle(v)}' for k, v in kwargs.items()]


SubgraphItem = Union[str, Dict, Node, Edge]
def subgraph(
        *args: SubgraphItem,
        name: Optional[str]=None,
        cluster: bool=False,
        klass: Optional[str]=None,
        kind: Optional[str]=None,
        **kwargs,
) -> Graph:
    mclass = {} if klass is None else {'class': klass}
    kw = {**kwargs, **mclass}

    clid = kwargs.get('id') # TODO might be nice to make it automatic?
    mid = {} if clid is None else {'class': '_clust_' + clid}

    # TODO ugh. right, don't think that rendering during construction was a good idea...
    # perhaps need to write few tests and fix it properly...

    def it() -> Iterable[str]:
        for x in args:
            if isinstance(x, dict):
                # TODO a bit horrible..
                # TODO also incorrect if we got inline bits of strings (e.g. adhoc 'subgraph whatever {')
                kw.update(x)
            elif isinstance(x, Graph):
                yield from x.render()
            elif isinstance(x, str):
                yield x
            elif isinstance(x, Node):
                # TODO right, this is pretty horrible...
                # I guess I need to
                # a) do not violate immutability
                # b) wrap str in Node anyway
                # c) pass this to Edge as well
                # x.extra.update(mclass)
                x.extra.update(mid)
                yield from x.render()
            elif isinstance(x, Edge):
                yield from x.render()
            else:
                raise RuntimeError(x)
    ag: Sequence[str] = list(it())
    res = _render(*ag, **kw) # todo ??? what's going on here...
    return Graph(name_=name, cluster=cluster, raw=res, **maybe(kind=kind))

# todo not a great name?
def maybe(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def cluster(*args, **kwargs) -> Graph:
    return subgraph(*args, cluster=True, **kwargs)


def graph(*args, **kwargs) -> Graph:
    return subgraph(*args, **kwargs, kind='graph')


def digraph(*args, **kwargs) -> Graph:
    return subgraph(*args, **kwargs, kind='digraph')


def node(name: Optional[str]=None, set_class=False, **kwargs) -> Node:
    return Node(name_=name, set_class=set_class, extra=kwargs)


EdgeArg = Union[Nodish, Dict]


def edges(f: Nodish, t: Nodish, *args: EdgeArg, **kwargs) -> Iterator[Edge]:
    ee = [f, t]
    # TODO maybe allow multiedges?
    extra = {**kwargs}
    for a in args:
        if isinstance(a, dict):
            extra.update(a)
        else:
            ee.append(a)
    for ff, tt in zip(ee, ee[1:]):
        yield Edge(f=ff, t=tt, extra=extra)


def edge(*args, **kwargs) -> Edge:
    [e] = edges(*args, **kwargs)
    return e


EXTERNAL = blue
INTERNAL = darkgreen
def url(u: str, color=EXTERNAL) -> Extra:
    if u.startswith('#'):
        color = INTERNAL
    return {
        'URL': u,
        'fontcolor': color, # meh
    }


def render(x) -> str:
    if isinstance(x, str):
        return x
    elif hasattr(x, 'render'):
        return '\n'.join(x.render())
    elif isinstance(x, Iterable):
        return '\n'.join(render(c) for c in x)
    else:
        raise RuntimeError(f"Unsupported: {x}")


def with_style(*, svg: str, style: str) -> str:
    from lxml import etree as ET # type: ignore
    root = ET.fromstring(svg.encode('utf8')) # eh? lxml wants it
    st = ET.SubElement(root, 'style')
    st.text = style
    return ET.tostring(root, pretty_print=True).decode('utf8')
    # todo not sure if defs thing is necessary?
    # <defs> </defs>

NS = '{http://www.w3.org/2000/svg}'
def svgns(s):
    return NS + s


def group(*things):
    yield '{'
    yield from things
    yield '}'




def test_node() -> None:
    n = node(name='test', shape='star', label="Some node")
    # todo not sure about quotes for star?
    assert render(n) == '''
test [
  shape="star"
  label="Some node"
]
'''.strip()

    # TODO not sure about this... maybe should be a distinguished class or something
    n = node(name='test', label='< <b>HTML</b> >')
    assert render(n) == '''
test [
  label=< <b>HTML</b> >
]
'''.strip()

    n = node(name='test', **{'class': 'custom'})
    assert render(n) == '''
test [
  class="custom"
]
'''.strip()

    n = node(name='test', set_class=True)
    assert render(n) == '''
test [
  class="test"
]
'''.strip()

    n = node(name='lazy', id=lambda self_: 'so_' + self_.name)
    assert render(n) == '''
lazy [
  id="so_lazy"
]
'''.strip()


def test_edges() -> None:
    e = edges('node1', 'node2', 'node3')
    r = render(e)
    assert r == '''
node1 -> node2
node2 -> node3
'''.strip()


def test_graph() -> None:
    n1 = node(name='nnn')
    # LR = dict(rankdir='LR')
    g = graph(
        'rankdir="LR"',
        n1,
        name='G',
    )
    assert render(g) == '''
graph G {
  rankdir="LR"
  nnn
}
'''.strip()


def test_cluster() -> None:
    n1 = node(name='node1')
    n2 = node(name='node2')
    c = cluster(
        'node [shape=point]',
        n1,
        n2,
        edge(n1, n2),
        name='testcluster',
    )
    r = render(c)
    assert r == '''
subgraph cluster_testcluster {
  node [shape=point]
  node1
  node2
  node1 -> node2
}
'''.strip()
