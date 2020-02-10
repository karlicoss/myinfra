import sys
from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union, Any


cylinder = 'cylinder'
diamond = 'diamond'
point = 'point'
star  = 'star'

dashed = 'dashed'
dotted = 'dotted'
filled = 'filled'
rounded = 'rounded'

lightblue = 'lightblue'
black  = 'black'
blue   = 'blue'
gray   = 'gray'
green  = 'green'
orange = 'orange'
red    = 'red'
purple = 'purple'




_mname: Optional[str] = None
def _id2obj() -> Dict[int, Any]:
    assert _mname is not None
    globs = vars(sys.modules[_mname])
    return {id(v): k for k, v in globs.items()}


def init(mname: str):
    global _mname
    _mname = mname


def get_name(obj: Any) -> str:
    m = _id2obj()
    oid = id(obj)
    assert oid in m, obj
    return m[oid]


Data = Union[str, Iterable[str]]


class Subgraph(NamedTuple):
    name_: Optional[str]
    cluster: bool
    raw: Data

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
        yield f'subgraph {mcl}{name}' + ' {'
        for x in [self.raw] if isinstance(self.raw, str) else self.raw:
            # TODO handle multiline stuff properly?
            yield '  ' + x
        yield '}'


Extra = Dict[str, str]
class Node(NamedTuple):
    name_: Optional[str]
    extra: Dict

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
        if len(extra) == 0:
            yield self.name
            return

        yield f'{self.name} ['
        for l in _render(**extra):
            yield '  ' + l
        yield ']'


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


def _render(*args: str, **kwargs):
    return list(args) + [f'{k}="{v}"' for k, v in kwargs.items()]


SubgraphItem = Union[str, Dict, Node, Edge]
def subgraph(
        *args: SubgraphItem,
        name: Optional[str]=None,
        cluster: bool=False,
        klass: Optional[str]=None,
        **kwargs,
) -> Subgraph:
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
            elif isinstance(x, Subgraph):
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
    res = _render(*ag, **kw)
    return Subgraph(name_=name, cluster=cluster, raw=res)


def cluster(*args, **kwargs) -> Subgraph:
    return subgraph(*args, cluster=True, **kwargs)


def node(name: Optional[str]=None, **kwargs) -> Node:
    return Node(name_=name, extra=kwargs)


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


def url(u: str, color=blue) -> Extra:
    return {
        'URL': u,
        'fontcolor': color, # meh
    }


def render(x):
    if isinstance(x, str):
        return x
    else:
        return '\n'.join(x.render())
