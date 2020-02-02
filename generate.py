#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Iterator, NamedTuple, Optional, Union


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
    name: str
    extra: Dict

    def render(self) -> Iterable[str]:
        extra = {**self.extra}
        if len(extra) == 0:
            yield self.name
            return

        yield f'{self.name} ['
        for l in _render(**extra):
            yield '  ' + l
        yield ']'


def node(name: str, **kwargs) -> Node:
    if ' ' in name:
        # TODO check if already quoted first?
        name = f'"{name}"'
    return Node(name=name, extra=kwargs)


Edge = str
def edge(f: Node, t: Node) -> Edge:
    return f'{f.name} -> {t.name}'

blue = 'blue'
dashed = 'dashed'


def url(u: str) -> Extra:
    return {
        'URL': u,
        'fontcolor': blue, # meh
    }


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


def gh(x: str) -> str:
    return f'https://github.com/{x}'


tgbackup = node(
    name='tgbackup', # TODO tmp hack?
    label='telegram_backup',
    **url(gh('fabianonline/telegram_backup')),
)


def dead() -> Extra:
    return {
        'shape': 'cds',
    }


vkexport = node(
    name='vkexport',
    **url(gh('Totktonada/vk_messages_backup')),
    **dead()
    # TODO just unpack dicts if they are in args?
)


endoexport = node(
    name='endoexport',
    **url(gh('karlicoss/endoexport')),
)

ipexport = node(
    name='ipexport',
    label='instapexport',
    **url(gh('karlicoss/instapexport')),
)

def generate_pipelines() -> str:
    sc = cluster(
'''
    // style=dashed;

    tw_manual[shape=invtrapezium];
    twexport;
''',
        *vkexport.render(),
        *tgbackup.render(),
        *endoexport.render(),
        *ipexport.render(),
'''

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
