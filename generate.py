#!/usr/bin/env python3
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

DEVICE = {
    'style': filled,
    'color': gray,
}


BLOG_EDGE = {
    'color': BLOG_COLOR,
    'style': dashed,
    'arrowhead': 'none',
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

orger_point = node(shape='point')

# TODO instead of orger, it should be 'Plaintext reflections' or smth like that
# TODO reduce distance between edges...
# TODO eh. maybe instead simply list/url modules and only split into interactive/static?
orger = cluster(
    orger_point,
    '''
module_twitter;
orger_point -> module_twitter [style=invis];

module_kobo;
module_twitter -> module_kobo [style=invis];

module_instapaper;
module_kobo -> module_instapaper [style=invis];

module_kobo2org;
module_instapaper -> module_kobo2org [style=invis];

module_ip2org;
module_kobo2org -> module_ip2org [style=invis];
    ''',
    blog_orger,
    'blog_orger -> module_twitter [style=invis]',
    edge(orger_point, blog_orger, **BLOG_EDGE),
    url(gh('karlicoss/orger')),
    label='Orger',
)


# TODO indicate that it's selfhosted?
syncthing = cluster(
    'syncthing [style=invis]',
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

def generate() -> str:
    items = [
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
        syncthing,
        edge(app_bm, 'syncthing'), # TODO here, a rooted script is involved
        edge('syncthing', 'exp_bluemaestro'),

        orger,
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


scripts = cluster(
    'twexport',
    tw_manual,
    vkexport,
    tgbackup,
    endoexport,
    ipexport,
    'jbexport',
    # jbexport [shape=cds]; // TODO cross out maybe?
    takeout_manual,
    kobuddy,
    emfitexport,
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
    **url('https://github.com/karlicoss/my'),
    label='my. package',
    shape=star,
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


def generate_pipelines() -> str:
    items = [
        '{',
        mypkg,
        blog_mypkg,
        edge(mypkg, blog_mypkg   , **BLOG_EDGE),
        blog_hb_kcals,
        edge(mypkg, blog_hb_kcals, **BLOG_EDGE),
        '}',

        inp_weight,
        inp_blood,
        scripts,
        exports,
        dals,
    ]
    return '\n'.join(map(render, items))

UI = {
    'style': filled,
    'color': 'pink',
}

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

        edge(mypkg, ipython),
    ]
    return '\n'.join(map(render, items))


gps = node()
app_bm = node()

phone = cluster(
    # TODO remove arrows as well?
    '''
node [style=invis,shape=point];

app_endomondo;
app_jawbone;
    ''',
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
    edge(wahoo, 'app_endomondo', label='BT'),

    jawbone_band,
    edge(jawbone_band, 'app_jawbone', label='BT'),

    bluemaestro,
    edge(bluemaestro, app_bm, label='BT'),

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


# TODO meh. okay, I might need some hackery to properly display edge labels...
# https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath
