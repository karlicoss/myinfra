#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union


Data = Union[str, Iterable[str]]

class Cluster(NamedTuple):
    raw: Data
    name: Optional[str]=None

    def render(self, name: Optional[str]=None) -> Iterable[str]: # TODO list str?
        assert self.name == name or (self.name is None) ^ (name is None)
        name = self.name or name # meh
        yield f'subgraph cluster_{name}' + ' {'
        for x in [self.raw] if isinstance(self.raw, str) else self.raw:
            # TODO handle multiline stuff properly?
            yield '  ' + x
        yield '}'


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


def _render(*args: str, **kwargs):
    return list(args) + [f'{k}="{v}"' for k, v in kwargs.items()]


ClusterItem = Union[str, Dict, Node]
def cluster(*args: ClusterItem, name: Optional[str]=None, **kwargs) -> Cluster:
    kw = {**kwargs}
    def it() -> Iterable[str]:
        for x in args:
            if isinstance(x, str):
                yield x
            elif isinstance(x, dict):
                # TODO a bit horrible..
                kw.update(x)
            elif isinstance(x, Node):
                yield from x.render()
            else:
                raise RuntimeError(x)
    ag: Sequence[str] = list(it())
    res = _render(*ag, **kw)
    return Cluster(raw=res, name=name)


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


filled = 'filled'

black = 'black'
gray = 'gray'
green = 'green'
orange = 'orange'
red = 'red'


CLOUD = {
    'style': 'dashed,rounded',
}

DEAD = {
    'style': filled, # TODO need to apaned to styles?
    'color': red, # TODO not sure. looks bit too bright..
}

DEVICE = {
    'style': filled,
    'color': gray,
}

def collect(x: Union[Dict, List]) -> Iterator[str]:
    # TODO collect all globals?
    d: Dict
    if isinstance(x, list):
        # TODO ok, it's a bit horrible...
        # TODO just use this logic in def name or something?
        gl = {id(v): k for k, v in globals().items()}
        d = {gl[id(o)]: o for o in x}
    else:
        d = x
    for k, v in d.items():
        if isinstance(v, Cluster):
            # TODO name??
            yield from v.render(name=k)
            yield '\n'


def generate() -> str:
    misc = [
        phone,
        telegram,
        vkcom,
        google,
        twittercom,
        endomondo,
        instapaper,
        emfit_cloud,
        jawbone,
        devices,
        emfit,
        kobo,
    ]
    return '\n'.join(collect(misc))


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

kobuddy = node(
    name='kobuddy',
    **url(gh('karlicoss/kobuddy')),
)

# TODO use __name__?
emfitexport = node(
    name='emfitexport',
    **url(gh('karlicoss/backup-emfit')),
)


scripts = cluster(
'''
    // style=dashed;
    tw_manual[shape=invtrapezium];
    twexport;
''',
    vkexport,
    tgbackup,
    endoexport,
    ipexport,
'''
    jbexport [shape=cds]; // TODO cross out maybe?

    takeout  [shape=invtrapezium];
''',
    kobuddy,
    emfitexport,
    label='Export scripts',
    style=dashed,
)


# TODO more like 'cluster_fs'?
#  rankdir=LR;
exports = cluster(
'''
    node [shape=cylinder];
    // exp_point [shape=point]; // TODO ughhh. why is everything so hard
    exp_telegram;
    exp_jawbone;
    exp_kobo;
    exp_takeouts;
    # TODO mention kython.ktakeout??
    exp_twitter_archives;

    exp_emfit;
    exp_twitter;
    exp_vk;

    exp_endomondo;
    exp_instapaper;

    data_weight;
    data_blood;
    # TODO mention manual inputs for these..

    exp_bluemaestro;
''',
    style=dashed,
    color=black,
    label='Filesystem',
)
# TODO eh, figure out better shape for 'dead'
# TODO perhaps makes more sense to mark edge?

  #   // exp_point -> exp_telegram [style=dashed, constraint=false];
  #   // exp_point -> exp_jawbone  [style=dashed, constraint=false];
  # }

dals = cluster(
'''
    dal_twitter;
    dal_endomondo;
    dal_kobuddy;
    dal_ip;
''',
    label='Data access layer',
)
# TODO dal links might look better on edges?


def generate_pipelines() -> str:
    return '\n'.join(collect([scripts, exports, dals]))


def generate_post() -> str:

    # TODO https://beepb00p.xyz/takeout-data-gone.html
    # TODO decluser and don't participate in constraints?
    blog = cluster(
        '''
    edge [style=dashed]; 

    blog_hb_kcals [
        label="Making sense of Endomondo's calorie estimation";
        URL="https://beepb00p.xyz/heartbeats_vs_kcals.html";
    ];
    blog_mypkg [
        label="my. package";
        URL="https://beepb00p.xyz/mypkg.html";
    ];
    blog_orger;
    blog_takeout_data_gone;


    // TODO pipelines could link to sad state
    orger_point -> blog_orger;
    mypkg       -> blog_hb_kcals;
    mypkg       -> blog_mypkg;
    takeout     -> blog_takeout_data_gone;
        ''',
        label='Blog posts',
    )

    d = {
        'blog': blog,
    }
    return '\n'.join(collect(d))


phone = cluster(
    # TODO remove arrows as well?
    '''
node [style=invis,shape=point];
gps;

app_endomondo;
app_bluemaestro;
app_jawbone;
    ''',
    DEVICE,
    label='Phone\n(Android)',
)



# TODO eh, these extra nodes are useles..
telegram = cluster(
'''
tg_api [label=API];
''',
    CLOUD,
    url('https://telegram.org'),
    label='Telegram',
)


vkcom = cluster(
'''
vk_api [label=API];
''',
    CLOUD,
    url('https://vk.com'),
    label='VK.com',
)

google_loc = node('Google Location') # TODO enclose in quotes if necessary?
takeout = node('Takeout', **url('https://takeout.google.com'))

# TODO "timeline" can be treated as poor man's api??
google = cluster(
    # TODO make rendering automatic?
    google_loc,
    takeout,
    edge(google_loc, takeout), # TODO something more dsly like multiplication?
    CLOUD,
    color=orange,
    label='Google',
#   // rankdir="TB";  // eh? not working..
)

tw_api = node(name='tw_api', label='API')
tw_archive = node(
    name='tw_archive',
    label='Twitter Archive',
    **url('https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive'),
)

# TODO map manual steps without intermediate nodes?

twittercom = cluster(
    tw_api,
    tw_archive,
    CLOUD,
    color='lightblue',
    label='Twitter',
)

endomondo = cluster(
    'end_api [label=API]',
    CLOUD,
    url('https://www.endomondo.com'),
    color=green,
    label='Endomondo',
)

# TODO also could show how data gets _into_ the services, i.e. clients?

instapaper = cluster(
    'ip_api [label=API]',
    CLOUD,
    url('https://www.instapaper.com'),
    color='lightgray', # TODO for other as well?
    label='Instapaper',
)

emfit_cloud = cluster(
    'emfit_api [label=API]',
    CLOUD,
    label='Emfit',
)

# TODO demonstrate that it's dead
# TODO not sure. wedged? striped? invert colors?
jawbone = cluster(
    'jb_api [label=API]',
    CLOUD,
    DEAD,
    **url('https://en.wikipedia.org/wiki/Jawbone_(company)#UP24'),
    color=orange,
    label='Jawbone\n(dead)',
)

emfit = cluster(
    # TODO dot?
    '''
emfit [shape=point];
emfit_wifi [label="wifi\n(local API)"];
    ''',
    # TODO add https://gist.github.com/harperreed/9d063322eb84e88bc2d0580885011bdd
    url('https://www.emfit.com/why-choose-emfit-for-sleep-analysis'),
    DEVICE,
    name='emfit',
    label='Emfit\n(sleep tracker)',
)


kobo = cluster(
    'kobo_sqlite [label=sqlite]',
    url('https://us.kobobooks.com/products/kobo-aura-one-limited-edition'),
    DEVICE,
    name='kobo',
    label='Kobo reader',
)

wahoo = node(
    name='wahoo',
    label='Wahoo Tickr X\n(HR monitor)',
    **DEVICE,
    **url('https://uk.wahoofitness.com/devices/heart-rate-monitors/wahoo-tickr-x-heart-rate-strap'),
)

jawbone_band = node(
    name='jawbone',
    label='Jawbone\n(sleep tracker)',
    **DEVICE,
)

bluemaestro = node(
    name='bluemaestro',
    label='Bluemaestro\n(environment\nsensor)',
    **DEVICE,
    **url('https://bluemaestro.com/products/product-details/bluetooth-environmental-monitor-and-logger'),
)

devices = cluster(
    wahoo,
    jawbone_band,
    bluemaestro,
    *emfit.render(),
    *kobo.render(),
    label='Devices',
)


def main():
    Path('diagram.dot').write_text(generate())
    Path('pipelines.dot').write_text(generate_pipelines())
    Path('post.dot').write_text(generate_post())


if __name__ == '__main__':
    main()
