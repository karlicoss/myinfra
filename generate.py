#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
# from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union, Any

import dotpy
dotpy.init(__name__) # TODO extremely meh

from dotpy import *


def gh(x: str) -> str:
    return f'https://github.com/{x}'


BLOG_COLOR = purple

CLOUD = {
    'style': 'dashed,rounded',
}

DEAD = {
    'style': filled, # TODO need to apaned to styles?
    'color': red, # TODO not sure. looks bit too bright..
}

INVIS = {
    'style': 'invis',
}

DEVICE = {
    'style': filled,
    'color': gray,
}


BLOG_EDGE = {
    'color': BLOG_COLOR,
    'style': dashed,
    'arrowhead': 'none',
}


UI = {
    'style': filled,
    'color': 'pink',
}

NOCONSTRAINT = {
    'constraint': 'false',
}


# TODO pipelines could link to sad state

def blog_post(link: str, *args, **kwargs) -> Node:
    return node( # type: ignore
        *args,
        shape='component',
        color=BLOG_COLOR,
        **url(link, color=BLOG_COLOR), # TODO need extra attr to mark link..
        **kwargs,
    )  # type: ignore[mise]

# TODO FIXME blog edge
blog_orger = blog_post(
    'https://beepb00p.xyz/orger.html',
    label='Orger: plaintext reflection\nof your digital self',
    # constraint='false', # TODO # eh?
)

orger_point = node(shape=point)

def orger_static() -> List[str]:
    return [
        'kobo',
        'twitter',
        'instapaper',
        # TODO actually get them straight from orger modules?
    ]

def orger_todos() -> List[str]:
    return [
        'kobo2org',
        'ip2org',
    ]

orger_static_node = node(
    label='\n'.join(['Static modules'] + orger_static())
)

# TODO come up with a better name.. it involves reddit and hackerviews too
orger_int_node = node(
    label='\n'.join(['Interactive modules'] + orger_todos())
)

# TODO instead of orger, it should be 'Plaintext reflections' or smth like that
# TODO reduce distance between edges...
# TODO eh. maybe instead simply list/url modules and only split into interactive/static?
orger = cluster(
    orger_point,
    orger_static_node,
    orger_int_node,
    blog_orger,
    edge(orger_point, blog_orger, **BLOG_EDGE, constraint='false'),
    # 'blog_orger -> module_twitter [style=invis]',
    url(gh('karlicoss/orger')),
    label='Orger',
)

# TODO add .point attribute to cluster?
orger_outputs_point = node(shape=point)

orger_outputs = cluster(
    'node [shape=cylinder]',
    orger_outputs_point,
    edge(orger_static_node, '"readonly views"'),
    edge(orger_int_node   , '"interative views"'), # TODO
    edge(orger_int_node   , '"todo lists"'),
    label='Org-mode files',
)



# TODO indicate that it's selfhosted?

syncthing = node(**INVIS)
syncthing_cl = cluster(
    syncthing,
    CLOUD,
    url('https://syncthing.net'),
    color='lightblue', # TODO fill?
    label='Syncthing',
)


# TODO these three are same level as orger?
dashboard = node(
    **url('https://beepb00p.xyz/my-data.html#dashboard'),
    label='Dashboard',
    shape=star,
)


timeline = node(
    label='Timeline',
    shape=star,
)

promnesia = node(
    **url(gh('karlicoss/promnesia')),
    label='Promnesia',
    shape=star,
)

scales = node(
    **DEVICE,
)

blood_tests = node(
    label="Blood testing\nfacilities\n(GP/Thriva/etc)",
)


emacs = node(
    label='Emacs\n(Spacemacs)',
    **UI,
)


def generate() -> str:
    items = [
        meta,

        phone,

        scales,
        blood_tests,
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
        syncthing_cl,

        edge(app_endomondo, end_api),
        edge(app_jawbone, jb_api),
        edge(emfit_point, emfit_api),
        edge(app_bm, syncthing), # TODO here, a rooted script is involved
        edge(syncthing, 'exp_bluemaestro'),

        orger,
        orger_outputs,
        emacs,
        edge(orger_outputs_point, emacs),

        '{',
        dashboard,
        timeline,
        promnesia,
        '}',
    ]
    return '\n'.join(map(render, items))


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


MANUAL = {'shape': 'invtrapezium'}

tw_manual = node(
    label='Manual request\n(once)',
    **MANUAL,
)


takeout_manual = node(
    label='Manual request\n(periodic)', 
    **MANUAL, # TODO actually, semi-manual?
)


against_db = blog_post(
    'https://beepb00p.xyz/unnecessary-db.html',
    label='Against unnecessary databases',
)

mydata = blog_post(
    'https://beepb00p.xyz/my-data.html',
    label='What data I collect and why?',
)

scheduler = blog_post(
    'https://beepb00p.xyz/scheduler.html',
    label='In search of a friendlier scheduler',
    # TODO better is not a great adjective here.
    # friendlier??
)


brain_coping = blog_post(
    'https://beepb00p.xyz/pkm-setup.html',
    label='How to cope with a human brain',
)

sad_infra = blog_post(
    'https://beepb00p.xyz/sad-infra.html',
    label='The sad state of personal data and infrastructure',
)


meta = cluster(
    brain_coping,
    sad_infra,
    edge(brain_coping, sad_infra, **INVIS),
    label='Meta',
    style=dashed,
)

twexport = node()
jbexport = node()
# jbexport [shape=cds]; // TODO cross out maybe?

scripts = cluster(
    twexport,
    tw_manual,
    vkexport,
    tgbackup,
    endoexport,
    ipexport,
    jbexport,
    takeout_manual,
    kobuddy,
    emfitexport,
    scheduler,

    label='Export scripts', # TODO instead of label, show legend for stuff that's actually automatic
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
    'subgraph uuu {',
    against_db,
    mydata,

    # TODO ugh. it completely breaks the layout...
    # edge(against_db, mydata),
    '}',

    style=dashed,
    color=black,
    label='Filesystem',
)
# TODO eh, figure out better shape for 'dead'
# TODO perhaps makes more sense to mark edge?

  #   // exp_point -> exp_telegram [style=dashed, constraint=false];
  #   // exp_point -> exp_jawbone  [style=dashed, constraint=false];
  # }

dals = subgraph(
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
    # **url('https://github.com/karlicoss/my'),
    # label='my. package',
    # shape=star,
    shape=point,
)

blog_mypkg = blog_post(
    'https://beepb00p.xyz/mypkg.html',
    label='my. package:\nPython interface to my life',
)

# TODO color arrows all the way through? so it's possible to trace how data propagates


blog_hb_kcals = blog_post(
    'https://beepb00p.xyz/heartbeats_vs_kcals.html',
    label="Making sense of\nEndomondo's calorie estimation",
)

inp_weight = node(
    label='Manual\ninput',
    **MANUAL,
) # TODO possible to automate inputs though

inp_blood = node(
    label='Manual\ninput',
    **MANUAL,
) # TODO once in several month?


mypy_err = blog_post(
    'https://beepb00p.xyz/mypy-error-handling.html',
    label='Using mypy for error handling',
)
# TODO use different style
cachew = node(
    label='cachew\npersistent cache/serialization',
    **url('https://github.com/karlicoss/cachew'),
)
mypkg_out = node('mypkg_out', shape='point')
# TODO space out mypkg_out nodes?

mypkg_usecases = cluster(
    blog_hb_kcals,
    label='Usecases',
    style=dashed,
)

mypkg_tech = cluster(
    mypy_err,
    cachew,
    label='Libraries/patterns',
    style=dashed,
)



def mypkg_promnesia(*, label: str, lid: int):
    aux = node(f'mypkg_aux_{lid}', shape=point)
    # TODO hmm. if I draw labels on these, could be good?
    yield aux
    yield edge(mypkg, aux, label=label, style=dotted)
    yield edge(aux, promnesia)

# TODO multiedges? a -> {b, c}
# TODO font isn't great..
mypkg_promnesia_edges = chain.from_iterable(
    mypkg_promnesia(label=l, lid=i) for i, l in enumerate([
        'Org files', # TODO that perhaps should link from the filesystem..
        'my.fbmessenger',
        'my.hypothesis',
        'my.instapaper',
        'my.pocket',
        'my.reddit',
        'my.telegram',
        'my.twitter',
        'my.vk',
        # TODO ok, think about connecting all mypkg modules (e.g. to dashboard/timeline as well)
        # 'my.weight',
    ])
)

def _mi(from_, **kwargs):
    aux = node('mypkg_in_' + from_, shape=point)
    yield aux
    yield edge(from_, aux, **kwargs)
    yield edge(aux, mypkg)


mypkg_incoming_edges = chain.from_iterable([
    _mi('exp_twitter'    , label='DAL'), # TODO make more space?
    _mi('exp_endomondo'  , label='DAL'),
    _mi('exp_instapaper' , label='DAL', **url(gh('karlicoss/instapexport'))),
    _mi('exp_kobo'       , label='DAL', **url(gh('karlicoss/kobuddy'))),
    _mi('exp_bluemaestro'),

    _mi('exp_takeouts'),
    _mi('exp_twitter_archives'),
    _mi('exp_jawbone'),
    _mi('exp_emfit'),
    _mi('exp_vk'),
    _mi('data_weight'),
    _mi('data_blood'),
    # TODO orgparse
    # TODO note how this edge is still active despite the fact that jbexport isn't working anymore
])

# TODO would be nice to add color; in that case node could be 'contaigious' and propagate color

def generate_pipelines() -> str:
    items = [
        inp_weight,
        inp_blood,
        scripts,

        # ...
        exports,

        # TODO maybe, patch stroke in python?
        edge_tw(tw_api, twexport)     , edge_tw(twexport , 'exp_twitter'),
        edge_tw(tw_archive, tw_manual), edge_tw(tw_manual, 'exp_twitter_archives'),

        edge_end(end_api, endoexport), edge_end(endoexport, 'exp_endomondo'),
        # dals, ??

        'subgraph cluster_xxx {',
        mypkg,
        *mypkg_incoming_edges,

        mypkg_out,

        # TODO group together cachew/mypy_err in a table?
        # add a label 'tecnhiques used'?
        edge(mypkg, mypkg_out),

        blog_mypkg,
        edge(mypkg, blog_mypkg   , **BLOG_EDGE, **NOCONSTRAINT),
        # TODO link separate table with usage examples?
        mypkg_usecases,
        mypkg_tech,
        # edge(blog_mypkg, blog_hb_kcals, **INVIS), # TODO mark this edge as special, merely for ordering?

        edge(mypkg_out, orger_point), # TODO not sure if belongs here..

        *mypkg_promnesia_edges,

        # TODO extract cluster?
        # TODO fix url
        # *url(gh('karlicoss/my')),
        'label="my. package"',

        '}',

        # edge(mypkg, 'alala'),
        # edge('alala', promnesia),


        # TODO need to reorder?

        # TODO debug mode?
        # 'style=invisible',
        'style=dashed',
    ]
    return '\n'.join(map(render, items))


def browser(for_):
    # return new node deliberately
    # TODO how to make unique?
    return node(
        name=f'browser_for_{for_}',
        label='Browser',
        **UI,
    )

ipython = node(
    label='IPython',
    **UI,
)

def generate_post() -> str:
    dbro = browser('dashboard')
    tbro = browser('timeline')
    pbro = browser('promnesia')
    items = [
        ipython,

        dbro,
        edge(dashboard, dbro),

        tbro,
        edge(timeline, tbro),

        pbro,
        edge(promnesia, pbro),

        edge(mypkg_out, ipython),
    ]
    return '\n'.join(map(render, items))


gps = node()
app_bm = node()
app_endomondo = node()
app_jawbone = node()

phone = cluster(
    # TODO remove arrows as well?
    '''
node [style=invis,shape=point];
    ''',
    app_endomondo,
    app_jawbone,
    app_bm,
    gps,
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
google_takeout = node(
    name='Takeout',
    **url('https://takeout.google.com'),
)


blog_takeout_data_gone = blog_post(
    'https://beepb00p.xyz/takeout-data-gone.html',
    label="Google Takeouts silently\nremoves old data",
)

# TODO "timeline" can be treated as poor man's api??
google = cluster(
    google_loc,
    edge(gps, google_loc),
    edge(google_loc, google_takeout), # TODO something more dsly like multiplication?

    # omg, I'm so happy it works so simply
    '{',
    google_takeout,
    blog_takeout_data_gone,
    '}',

    edge(google_takeout, blog_takeout_data_gone, **BLOG_EDGE, constraint='false'),
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

col_twitter = lightblue
def edge_tw(*args, **kwargs):
    # TODO warn on conflict?
    return edge(*args, fillcolor=col_twitter, arrowhead='diamond', **kwargs)


twittercom = cluster(
    tw_api,
    tw_archive,
    CLOUD,
    color=col_twitter,
    label='Twitter',
)

end_api = node(label='API')

col_end = green

def edge_end(*args, **kwargs):
    # TODO warn on conflict?
    return edge(*args, fillcolor=col_end, arrowhead='diamond', **kwargs)


endomondo = cluster(
    end_api,
    CLOUD,
    url('https://www.endomondo.com'),
    color=col_end,
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

emfit_api = node(label='API')

emfit_cloud = cluster(
    emfit_api,
    CLOUD,
    label='Emfit',
)

jb_api = node(label='API')
# TODO demonstrate that it's dead
# TODO not sure. wedged? striped? invert colors?
jawbone = cluster(
    jb_api,
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


emfit_point = node(shape=point)
emfit = cluster(
    emfit_point,
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
    edge(wahoo, app_endomondo, label='BT'),

    jawbone_band,
    edge(jawbone_band, app_jawbone, label='BT'),

    bluemaestro,
    edge(bluemaestro, app_bm, label='BT'),

    *emfit.render(),
    *kobo.render(),

    label='Devices',
    style=dashed,
)


def main():
    Path('diagram.dot').write_text(generate())
    Path('pipelines.dot').write_text(generate_pipelines())
    Path('post.dot').write_text(generate_post())


if __name__ == '__main__':
    main()


# TODO meh. okay, I might need some hackery to properly display edge labels...
# https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath

# TODO dot allows comments?

# TODO maybe, use html table? not sure..
# https://renenyffenegger.ch/notes/tools/Graphviz/examples/index

# TODO add hover anchors everywhere
