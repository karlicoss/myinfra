#!/usr/bin/env python3
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union, Any


Data = Union[str, Iterable[str]]



# @lru_cache(1) # TODO hmm, that might not work as expected.. need to init at the end of program??
def _id2obj() -> Dict[int, Any]:
    return {id(v): k for k, v in globals().items()}


def get_name(obj: Any) -> str:
    m = _id2obj()
    oid = id(obj)
    assert oid in m, obj
    return m[oid]


class Cluster(NamedTuple):
    name_: Optional[str]
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
        yield f'subgraph cluster_{name}' + ' {'
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
    return Cluster(name_=name, raw=res)


def node(name: Optional[str]=None, **kwargs) -> Node:
    return Node(name_=name, extra=kwargs)


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


star = 'star'

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


def render(x):
    return '\n'.join(x.render())


def generate() -> str:
    clusters = [
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
    return '\n'.join(map(render, clusters))


def gh(x: str) -> str:
    return f'https://github.com/{x}'


tgbackup = node(
    label='telegram_backup',
    **url(gh('fabianonline/telegram_backup')),
)


def dead() -> Extra:
    return {
        'shape': 'cds',
    }


vkexport = node(
    **url(gh('Totktonada/vk_messages_backup')),
    **dead()
    # TODO just unpack dicts if they are in args?
)


endoexport = node(
    **url(gh('karlicoss/endoexport')),
)

ipexport = node(
    label='instapexport',
    **url(gh('karlicoss/instapexport')),
)

kobuddy = node(
    **url(gh('karlicoss/kobuddy')),
)

emfitexport = node(
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


mypkg = node(
    **url('https://github.com/karlicoss/my'),
    label='my. package',
    shape=star,
)

def generate_pipelines() -> str:
    items = [
        mypkg,
        scripts,
        exports,
        dals,
    ]
    return '\n'.join(map(render, items))

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
# TODO https://beepb00p.xyz/takeout-data-gone.html
# TODO decluser and don't participate in constraints?

def generate_post() -> str:

    clusters = [blog]
    return '\n'.join(map(render, clusters))


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

# TODO use label
google_loc = node(name='Google Location')
takeout = node(
    name='Takeout',
    **url('https://takeout.google.com'),
)

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

tw_api = node(label='API')
tw_archive = node(
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

emfit_wifi = node(
    label='wifi\n(local API)',
    **url('https://gist.github.com/harperreed/9d063322eb84e88bc2d0580885011bdd'),
)

emfit = cluster(
    # TODO dot?
    '''
emfit [shape=point];
    ''',
    emfit_wifi,
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
    label='Wahoo Tickr X\n(HR monitor)',
    **DEVICE,
    **url('https://uk.wahoofitness.com/devices/heart-rate-monitors/wahoo-tickr-x-heart-rate-strap'),
)

jawbone_band = node(
    name='jawbone', # TODO name
    label='Jawbone\n(sleep tracker)',
    **DEVICE,
)

bluemaestro = node(
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
