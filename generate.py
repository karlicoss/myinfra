#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Iterator, NamedTuple, Union


CLOUD = 'style="dashed,rounded";';


Data = Union[str, Iterable[str]]

class Cluster(NamedTuple):
    raw: Data

    def render(self, name: str) -> Iterable[str]: # TODO list str?
        yield f'subgraph cluster_{name}' + ' {'
        for x in [self.raw] if isinstance(self.raw, str) else self.raw:
            # TODO handle multiline stuff properly?
            yield '  ' + x
        yield '}'


def _render(*args: str, **kwargs):
    return list(args) + [f'{k}="{v}"' for k, v in kwargs.items()]


def cluster(*args: str, **kwargs) -> Cluster:
    res = _render(*args, **kwargs)
    return Cluster(raw=res)


Extra = Dict[str, str]


class Node(NamedTuple):
    label: str
    extra: Dict

    def render(self) -> Iterable[str]:
        yield f'{self.label} ['
        for l in _render(**self.extra):
            yield '  ' + l
        yield ']'


def node(label: str, **kwargs) -> Node:
    if ' ' in label:
        # TODO check if already quoted first?
        label = f'"{label}"'
    return Node(label=label, extra=kwargs)


Edge = str
def edge(f: Node, t: Node) -> Edge:
    return f'{f.label} -> {t.label}'


Renderable = Cluster


def collect(d: Dict) -> Iterator[str]:
    # TODO collect all globals?
    for k, v in d.items():
        if isinstance(v, Cluster):
            # TODO name??
            yield from v.render(name=k)
            yield '\n'


def generate() -> str:
    return '\n'.join(collect(d=globals()))


blue = 'blue'
dashed = 'dashed'


def generate_pipelines() -> str:
    sc = cluster(
'''
    // style=dashed;

    tw_manual[shape=invtrapezium];
    twexport;

    vkexport [shape=cds];

    tgbackup;

    endoexport;
    ipexport;

    jbexport [shape=cds]; // TODO cross out maybe?

    takeout  [shape=invtrapezium];
''',
        label='Export scripts',
        style=dashed,
    )
    d = {
        'scripts': sc,
    }
    return '\n'.join(collect(d=d))




def url(u: str) -> Extra:
    return {
        'URL': u,
        'fontcolor': blue, # meh
    }



# TODO eh, these extra nodes are useles..
telegram = cluster(
'''
tg_api [label=API];
''',
    CLOUD,
    label='Telegram',
    **url('https://telegram.org'),
)


vkcom = cluster(
'''
vk_api [label=API];
''',
    CLOUD,
    label='VK.com',
    **url('https://vk.com'),
)


orange = 'orange'

google_loc = node('Google Location') # TODO enclose in quotes if necessary?
takeout = node('Takeout', **url('https://takeout.google.com'))

# TODO "timeline" can be treated as poor man's api??
google = cluster(
    # TODO make rendering automatic?
    *google_loc.render(),
    *takeout.render(),
    edge(google_loc, takeout), # TODO something more dsly like multiplication?
    CLOUD,
    color=orange,
    label='Google',
#   // rankdir="TB";  // eh? not working..
)

# pipelines = cluster(
#     label='Pipelines',
#     color='coral',
#     style='filled',
# )


def main():
    Path('diagram.dot').write_text(generate())
    Path('pipelines.dot').write_text(generate_pipelines())


if __name__ == '__main__':
    main()
