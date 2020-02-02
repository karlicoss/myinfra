#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple, Union


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


def cluster(*args: str, **kwargs) -> Cluster:
    res = list(args) + [f'{k}="{v}"' for k, v in kwargs.items()]
    return Cluster(raw=res)


Renderable = Cluster


def collect() -> Iterator[str]:
    # TODO collect all globals?
    for k, v in globals().items():
        if isinstance(v, Cluster):
            # TODO name??
            yield from v.render(name=k)
            yield '\n'


def generate() -> str:
    return '\n'.join(collect())


def main():
    Path('diagram.dot').write_text(generate())


# TODO eh, these extra nodes are useles..
telegram = cluster(
'''
tg_api [label=API];
''',
    CLOUD,
    label='Telegram',
    URL='https://telegram.org',
    # TODO ugh. url has to be capitulized; not sure if can make it automalic?
)


vkcom = cluster(
'''
vk_api [label=API];
''',
    CLOUD,
    label='VK.com',
    URL='https://vk.com',
)


orange = 'orange'

# TODO "timeline" can be treated as poor man's api??
google = cluster(
    '"Google Location"',
    '"Google Location" -> "Takeout"',
    CLOUD,
    color=orange,
    label='Google',
#   // rankdir="TB";  // eh? not working..
)


if __name__ == '__main__':
    main()
