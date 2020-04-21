#!/usr/bin/env python3
from itertools import chain
from pathlib import Path
# from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Union, Any

import dotpy
dotpy.init(__name__) # TODO extremely meh

from dotpy import *


debug = False

# TODO lighter boundaries for api bits in services

def gh(x: str) -> str:
    return f'https://github.com/{x}'

def bb(x: str) -> str:
    return f'https://beepb00p.xyz/{x}'


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

noarrow = {
    'arrowhead': 'none',
}

BLOG_EDGE = {
    'color': BLOG_COLOR,
    'style': dashed,
    **noarrow,
}


UI = {
    'style': filled,
    'color': 'pink',
}

NOCONSTRAINT = {
    'constraint': 'false',
}


CYLINDER = {
    # ok, cylinder doesn't take too much extra space
    'shape': cylinder,
}

AUTO = {
    'style': rounded,
}


MANUAL = {
    # ok, trapezium wastes a bit too much space
    # 'shape': 'invtrapezium',
    'style': filled,
    'color': '#fff380',
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



def bbm(x: str):
    return bb(f'my-data.html#{x}')

scales = node(
    label='scales',
    **url(bbm('weight')),
    **DEVICE,
)

blood_tests = node(
    label='Blood tests\n(GP/Thriva/etc)',
    **url(bbm('blood'))
)

sleep_subj = node(
    label='Sleep data\n(subjective)', # TODO link?
    **url(bbm('sleep')),
)


# TODO blog edge?
blog_orger = blog_post(
    bb('orger.html'),
    label='Orger: plaintext reflection\nof your digital self',
)

blog_orger_roam = blog_post(
    bb('myinfra-roam.html#orger'),
    label='Using Orger for\nRoam Research',
)

orger_point = node(shape=point)

def orger_static() -> List[str]:
    return [
        'kobo',
        'twitter',
        'instapaper',
        'youtube',
        'hypothesis',
        'github',
        # TODO actually get them straight from orger modules?
    ]

def orger_todos() -> List[str]:
    return [
        'kobo2org',
        'ip2org',
        'reddit',
        'hackernews',
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
    blog_orger_roam,
    # edge(orger_point, blog_orger     , **BLOG_EDGE, constraint='false'),
    # edge(orger_point, blog_orger_roam, **BLOG_EDGE, constraint='false'),
    #
    # 'blog_orger -> module_twitter [style=invis]',
    url(gh('karlicoss/orger')),
    label='Orger',
    style=dashed,
)

# TODO add .point attribute to cluster?
orger_outputs_point = node(shape=point)

orger_outputs = cluster(
    'node [shape=cylinder]',
    orger_outputs_point,
    edge(orger_static_node, '"readonly views"'),
    edge(orger_int_node   , '"interactive views"'), # TODO
    edge(orger_int_node   , '"todo lists"'),
    label='Org-mode files',
    style=dashed,
)



# TODO indicate that it's selfhosted?

syncthing = node(**INVIS)
syncthing_cl = cluster(
    syncthing,
    CLOUD,
    url('https://syncthing.net'),
    color=lightblue, # TODO fill?
    label='Syncthing',
)


# TODO these three are same level as orger?
dashboard = node(
    **url(bb('my-data.html#dashboard')),
    label='Dashboard',
    shape=star,
)


timeline = node(
    label='Timeline',
    shape=star,
    **url(bb('tags.html#lifelogging')),
)

promnesia = node(
    **url(gh('karlicoss/promnesia')),
    label='Promnesia',
    shape=star,
)


emacs = node(
    label='Emacs\n(Spacemacs)',
    **UI,
)


tgbackup = node(
    label='telegram_backup',
    **url(gh('fabianonline/telegram_backup')),
    **AUTO,
)


vkexport = node(
    **url(gh('Totktonada/vk_messages_backup')),
    **AUTO,
)
# TODO just unpack dicts if they are in args?


endoexport = node(
    **url(gh('karlicoss/endoexport')),
    **AUTO,
)

ipexport = node(
    label='instapexport',
    **url(gh('karlicoss/instapexport')),
    **AUTO,
)

kobuddy = node(
    **url(gh('karlicoss/kobuddy')),
    **AUTO,
)

emfitexport = node(
    **url(gh('karlicoss/backup-emfit')),
    **AUTO,
)


tw_manual = node(
    label='Manual request\n(once)',
    **MANUAL,
)


takeout_manual = node(
    label='Manual request\n(periodic)', 
    **MANUAL, # TODO actually, semi-manual?
)


against_db = blog_post(
    bb('unnecessary-db.html'),
    label='Against\nunnecessary databases',
)

mydata = blog_post(
    bb('my-data.html'),
    label='What data I collect\nand why?',
)

scheduler = blog_post(
    bb('scheduler.html'),
    label='In search of\na friendlier scheduler',
    # TODO better is not a great adjective here.
    # friendlier??
)


brain_coping = blog_post(
    bb('pkm-setup.html'),
    label='How to cope with a human brain',
)

sad_infra = blog_post(
    bb('sad-infra.html'),
    label='The sad state of\npersonal data and infrastructure',
)

dataliberation = blog_post(
    bb('exports.html'),
    label='Building data liberation\ninfrastructure'
)


meta = cluster(
    brain_coping,
    sad_infra,
    mydata,
    # *edges(brain_coping, sad_infra, **INVIS),
    label="Meta\n(why I'm doing all this?)",
    style=dashed,
)

# TODO colored text is clickable links?
legend = cluster(
    node(
        'Device',
        **DEVICE
    ),
    node(
        name='legend_auto',
        label='Automatic\nscript',
        **AUTO,
    ),
    node(
        name='legend_manual',
        label='Manual\nstep',
        **MANUAL,
    ), # TODO order?
    blog_post(
        bb(''),
        label='Entry from my blog\n(clickable)',
        name='legend_blog',
    ),
    node(
        name='legend_ui',
        label='User facing\ninterface',
        **UI,
    ),
    # TODO elaborate what's so special about files?
    node(
        'Disk storage',
        **CYLINDER,
    ),
    # 'Device -> "Manual step" -> legend_blog',
    label='Legend',
    style=dashed,
)

twint = node(**AUTO, **url(gh('twintproject/twint')))
jbexport = node(**AUTO)
# jbexport [shape=cds]; // TODO cross out maybe?

rexport    = node(**AUTO, **url(gh('karlicoss/rexport')))
pinbexport = node(**AUTO, **url(gh('karlicoss/pinbexport')))

exports = cluster(
    twint,
    tw_manual,
    vkexport,
    tgbackup,
    rexport,
    pinbexport,
    endoexport,
    ipexport,
    jbexport,
    takeout_manual,
    kobuddy,
    emfitexport,
    scheduler,
    dataliberation,

    label='Export scripts', # TODO bit misleading; contains manual?
    style=dashed,

    id='exports',
    **url('#exports'), # TODO show anchor sign?
)
#
# TODO legend?
CLOUD_SYNC = dict(
    style=dashed,
    **CYLINDER,
)


data_weight = node(label='org-mode')
data_blood  = node(label='org-mode')
data_sleep  = node(label='org-mode')
exp_twitter = node(label='sqlite')
exp_twitter_archives = node(label='json')


exp_reddit     = node(label='json')
exp_pinb       = node(label='json')
exp_telegram   = node(label='sqlite')
exp_jawbone    = node(label='json')
exp_kobo       = node(label='sqlite')
exp_takeouts   = node(label='json/html')
exp_emfit      = node(label='json')
exp_vk         = node(label='json')
exp_endomondo  = node(label='json')
exp_instapaper = node(label='json')
# ugh. seems like a bug, it should inherit cylinder spect from the cluster
exp_bluemaestro   = node(label='sqlite', **CLOUD_SYNC, color=blue)
exp_materialistic = node(label='sqlite', **CLOUD_SYNC, color=orange)
# TODO FIXME when I hover, highlight both?


# eh. also just to order properly
# cluster_fewfwfjwf = cluster(
# )


filesystem = cluster(
    'node [shape=cylinder]',

    'subgraph cluster_just_to_enforce_order {',
    data_weight,
    data_blood,
    data_sleep,
    'style=invis'
    '}',

    exp_telegram,
    exp_reddit,
    exp_pinb,
    exp_twitter,
    exp_twitter_archives,
    exp_jawbone,
    exp_kobo,
    exp_takeouts,
    exp_emfit,
    exp_vk,
    exp_endomondo,
    exp_instapaper,
    exp_bluemaestro,
    exp_materialistic,
    # TODO mention kython.ktakeout??
    'subgraph filesystem_blog {',
    against_db,
    # TODO ugh. it completely breaks the layout...
    # edge(against_db, mydata),
    '}',

    style=dashed,
    color=black,
    label='Filesystem',
    id='fs', # ok, relying on ids makes sense
    **url("#fs"),
)

# TODO add reference to data access layer to the graph


mypkg = node(
    **url('https://github.com/karlicoss/HPI'),
    label='HPI (Human Programming Interface)',
)

blog_mypkg = blog_post(
    'https://beepb00p.xyz/hpi.html',
    label='HPI:\nMy life in a Python package',
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

inp_sleep = node(
    label='Manual\ninput',
    **MANUAL,
)

mypy_err = blog_post(
    'https://beepb00p.xyz/mypy-error-handling.html',
    label='Using mypy for\nerror handling',
)
# TODO use different style
cachew = node(
    label='cachew\npersistent cache/serialization',
    **url('https://github.com/karlicoss/cachew'),
)
mypkg_out = node('mypkg_out', shape='point')
# TODO space out mypkg_out nodes?

# TODO not sure...
mypkg_usecases = cluster(
    blog_hb_kcals,
    label='Usecases',
    style=dashed,
    # TODO diff stroke color?
)

mypkg_tech = cluster(
    mypy_err,
    cachew,
    label='Libraries/patterns',
    style=dashed,
)


class my:
    fbm        = 'my_fbmessenger'
    hyp        = 'my_hypothesis'
    instapaper = 'my_instapaper'
    pocket     = 'my_pocket'
    reddit     = 'my_reddit'
    tg         = 'my_telegram'
    tw         = 'my_twitter'
    vk         = 'my_vk'
    weight     = 'my_body_weight'
    sleep      = 'my_sleep'
    ex         = 'my_exercise'
    cal        = 'my_calendar'
    blood      = 'my_body_blood'
    pinboard   = 'my_pinboard'


def mymodule_url(module: str) -> Optional[str]:
    if module in {
            my.ex,
            my.sleep,
    }:
        # private atm
        return None
    mp = module.replace('_', '/')
    pp = 'karlicoss/my/blob/master/' + mp
    addpy = module not in {my.cal, my.tw} # meh, hacky
    if addpy:
        pp += '.py'
    return gh(pp)


def mypkg_module(*, module: str, lid: int):
    murl = mymodule_url(module)

    extra = colmap.get(module, {})
    # TODO combine colors?
    # TODO color dots instead?

    aux = node(module, shape=point)
    yield aux
    label = module.replace('_', '.')
    # ok, multiple dotted -- impossible to see.
    # dashed a bit better but still not great..
    yield edge(mypkg, aux, label=label, style=dotted, **extra, **({} if murl is None else url(murl)))



# TODO multiedges? a -> {b, c}
# TODO font isn't great..
mypkg_module_edges = chain.from_iterable(
    mypkg_module(module=l, lid=i) for i, l in enumerate([
        # 'Org files', # TODO that perhaps should link from the filesystem..
        my.fbm,
        my.hyp,
        my.instapaper,
        my.pocket,
        my.reddit,
        # my.tg,
        my.tw,
        my.vk,
        my.pinboard,
        # TODO ok, think about connecting all mypkg modules (e.g. to dashboard/timeline as well)
        my.weight,
        my.sleep,
        my.ex,
        my.cal,
        my.blood,
    ])
)

mypkg_promnesia_edges = [
    edge(mod, promnesia) for mod in {
        my.fbm,
        my.hyp,
        my.instapaper,
        my.pocket,
        my.reddit,
        # my.tg,
        my.tw,
        my.vk,
        my.pinboard,
    }
]

mypkg_dashboard_edges = [
    edge(mod, dashboard) for mod in {
        my.weight,
        my.sleep,
        my.ex,
        my.cal,
        my.blood,
    }
]

# TODO need to display 'DAL' in the middle...
def _mi(from_, **kwargs):
    pcol = kwargs.get('fillcolor')
    # TODO hacky..
    auxcol = {} if pcol is None else dict(color=pcol)

    node_shape = point
    label = kwargs.get('label')
    if label != 'DAL': # TODO how to link to 'data access layer'??
        # hacky...
        # TODO maybe do the opposite? if dal, then arrowhead
        kwargs['arrowhead'] = 'none'
        auxcol.update(dict(
            color=black,
            style=point,
            # meh, but works...
            fixedsize='true',
            width=0.02,
            height=0.02,
        ))
    else:
        kwargs['class'] = 'dal_edge'
    aux = node('mypkg_in_' + from_, shape=point, **auxcol) # TODO ugh. invis doesn't help here; it still takes space..
    yield aux
    # TODO check first..arrowhead='none',
    yield edge(from_, aux, **kwargs)
    yield edge(aux, mypkg)


def mypkg_incoming_edges():
    return chain.from_iterable([
    _mi('exp_reddit'     , label='DAL', **E.reddit, **url(gh('karlicoss/rexport'))),
    _mi('exp_pinb'       , label='DAL', **E.pinb  , **url(gh('karlicoss/pinbexport'))),
    _mi('exp_twitter'                 , **E.tw),
    _mi('exp_endomondo'  , label='DAL', **E.end,    **url(gh('karlicoss/endoexport')), id='dal'), # eh. id here is kinda arbitrary...
    _mi('exp_instapaper' , label='DAL', **E.ip,     **url(gh('karlicoss/instapexport'))),
    _mi('exp_kobo'       , label='DAL', **E.kobo,   **url(gh('karlicoss/kobuddy'))),
    _mi('exp_bluemaestro'),
    _mi('exp_materialistic'),

    _mi('exp_takeouts'),
    _mi('exp_twitter_archives', **E.tw),
    _mi('exp_jawbone', **E.jb),
    _mi('exp_emfit'),
    _mi('exp_vk'),
    _mi('data_weight', **E.weight),
    _mi('data_blood' , **E.blood ),
    _mi('data_sleep'             ),
    # TODO eh, orgparse is a bit unreadable there..
    # TODO note how this edge is still active despite the fact that jbexport isn't working anymore
])

# TODO would be nice to add color; in that case node could be 'contaigious' and propagate color

def mypkgcl():
    return cluster(
        cluster(
            mypkg_tech,
            mypkg_usecases,
            mypkg,
            blog_mypkg,
            INVIS,
            name='mypkg_core',
        ),

        *mypkg_incoming_edges(),

        mypkg_out,

        # TODO group together cachew/mypy_err in a table?
        # add a label 'tecnhiques used'?
        edge(mypkg, mypkg_out),

        edge(mypkg, blog_mypkg   , **BLOG_EDGE, **NOCONSTRAINT),
        # TODO link separate table with usage examples?
        # edge(blog_mypkg, blog_hb_kcals, **INVIS), # TODO mark this edge as special, merely for ordering?

        edge(mypkg_out, orger_point), # TODO not sure if belongs here..

        *mypkg_module_edges,
        *mypkg_promnesia_edges,
        *mypkg_dashboard_edges,

        # *url(gh('karlicoss/my')),
        url('#mypkg'), # TOOD add extra id?
        label='Human Programming Interface',
        id='mypkg',


        style=dashed,
        name='mypkgcl',
    )

def pipelines():
    items = [
        inp_weight,
        inp_sleep,
        inp_blood,
        exports,

        # ...
        filesystem,

        # TODO maybe, patch stroke in python?
        *edges(tw_api    , twint    , 'exp_twitter'         , E.tw),
        *edges(tw_archive, tw_manual, 'exp_twitter_archives', E.tw),

        *edges(end_api, endoexport, exp_endomondo, E.end),

        *edges(tg_api    , tgbackup  , exp_telegram, E.tg),
        *edges(reddit_api, rexport   , exp_reddit  , E.reddit),
        *edges(pinb_api  , pinbexport, exp_pinb    , E.pinb),
        *edges('kobo_sqlite', kobuddy, exp_kobo    , E.kobo),

        edge(jb_api, 'jbexport', E.jb, color=red),
        edge('jbexport', 'exp_jawbone', E.jb),

        *edges('Takeout', takeout_manual, 'exp_takeouts'),
        *edges(emfit_api, emfitexport, 'exp_emfit'),
        *edges(ip_api, ipexport, exp_instapaper, E.ip),

        edge('vk_api', vkexport, label='API closed', **url('https://github.com/Totktonada/vk_messages_backup/pull/8#issuecomment-494582792'), color=red),
        edge(vkexport, 'exp_vk'),

        # TODO hmm, margin look interesting..
        mypkgcl(),

        # edge(mypkg, 'alala'),
        # edge('alala', promnesia),


        # TODO need to reorder?

        'color=red\nstyle=dashed' if debug else 'style=invisible',
    ]
    return items

# TODO remove nodes when there is no data access layer??

def browser(for_, label='Browser'):
    # returns new node deliberately, to prevent edge clutter
    return node(
        name=f'browser_for_{for_}',
        label=label,
        **UI,
    )

ipython = node(
    label='IPython',
    **UI,
)

def post():
    dbro = browser('dashboard', label='Browser\n(HTML)')
    tbro = browser('timeline' , label='Browser\n(HTML)')
    pbro = browser('promnesia', label='Browser\n(extension)')
    items = [
        # edge('exp_takeouts', promnesia, label='Browsing history'),
        # edge('exp_telegram', promnesia, label='Telegram'),

        ipython,

        dbro,
        edge(dashboard, dbro),

        tbro,
        edge(timeline, tbro),

        pbro,
        edge(promnesia, pbro),

        edge(mypkg_out, ipython),

        edge(mypkg_out, timeline),


        *edges(blood_tests, inp_blood , data_blood , **E.blood),
        *edges(scales     , inp_weight, data_weight, **E.weight),
        *edges(sleep_subj , inp_sleep , data_sleep),

    ]
    return items


# TODO give it color?
# TODO actually make node attributes accessible in runtime? so I could do smth.color?
app_bluemaestro_sqlite   = node(label='sqlite', **CLOUD_SYNC, color=blue)
app_materialistic_sqlite = node(label='sqlite', **CLOUD_SYNC, color=orange)
# phone_syncthing          = node(label='Syncthing', **CLOUD) # TODO fill with lightblue?

phone_fss = cluster(
    '''
node [style=solid,shape=rectangle];
    ''',
    app_bluemaestro_sqlite,
    app_materialistic_sqlite,
    # phone_syncthing,
    label='Filesystem',
)

gps = node(label='GPS', shape='rectangle', style='solid')
app_bm = node(
    label='Bluemaestro\napp',
    style='solid',
    shape='rectangle',
)
app_endomondo = node()
app_jawbone = node()

app_materialistic = node(
    label='Materialistic\n(Hackernews app)',
    **url('hidroh/materialistic'),
    style='solid',
    shape='rectangle',
)

phone = cluster(
    # TODO remove arrows as well?
    '''
node [style=invis,shape=point];
    ''',
    app_endomondo,
    app_jawbone,
    gps,
    app_bm,
    phone_fss,
    # TODO demonstrate that root is necessary??
    edge(app_bm           , app_bluemaestro_sqlite  , style=dashed, **noarrow),
    app_materialistic,
    edge(app_materialistic, app_materialistic_sqlite, style=dashed, **noarrow),
    # TODO dashed? to illustrate it's 'using'
    # edge(app_materialistic, phone_fs),
    DEVICE,
    label='Android\nphone',
)



# TODO eh, these extra nodes are useles..

col_tg = '#0088cc'

def api_node(*args, **kwargs):
    return node(
        label='API',
        shape='diamond',
        color='#00000066',
    )



tg_api = api_node()

telegram = cluster(
    tg_api,
    CLOUD,
    url('https://telegram.org'),
    color=col_tg,
    label='Telegram',
)


vk_api = api_node()
vkcom = cluster(
    vk_api,
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
    label="Google Takeout silently\nremoves old data",
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

    edge(google_takeout, blog_takeout_data_gone, **BLOG_EDGE, **NOCONSTRAINT),
    CLOUD,
    color=orange,
    label='Google',
#   // rankdir="TB";  // eh? not working..
)

# TODO map manual steps without intermediate nodes?

col_twitter = lightblue
col_end     = green
col_kobo    = '#bf2026'
col_jb      = '#540baf'
col_blood   = red
col_weight  = 'brown'
col_reddit  = 'pink'
col_ip      = 'lightgray'
col_pinb    = '#3975fa'


tw_api = api_node()
tw_archive = node(
    label='Twitter Archive',
    **url('https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive'),
)


twittercom = cluster(
    tw_api,
    tw_archive,
    CLOUD,
    color=col_twitter,
    label='Twitter',
)


reddit_api = api_node()
reddit = cluster(
    reddit_api,
    CLOUD,
    color=col_reddit,
    label='Reddit',
)

pinb_api = api_node()
pinboard = cluster(
    pinb_api,
    CLOUD,
    color=col_pinb,
    label='Pinboard', # TODO url?
)


class E:
    # TODO warn on conflict?
    end    = dict(arrowhead=diamond, fillcolor=col_end)
    tw     = dict(arrowhead=diamond, fillcolor=col_twitter)
    tg     = dict(arrowhead=diamond, fillcolor=col_tg)
    kobo   = dict(arrowhead=diamond, fillcolor=col_kobo)
    jb     = dict(arrowhead=diamond, fillcolor=col_jb)
    blood  = dict(arrowhead=diamond, fillcolor=col_blood)
    weight = dict(arrowhead=diamond, fillcolor=col_weight)
    reddit = dict(arrowhead=diamond, fillcolor=col_reddit)
    ip     = dict(arrowhead=diamond, fillcolor=col_ip)
    pinb   = dict(arrowhead=diamond, fillcolor=col_pinb)

# meh...
colmap = {
    my.tw    : E.tw,
    my.tg    : E.tg,
    # my.kobo: E.kobo,
    my.sleep : E.jb,
    my.blood : E.blood,
    my.weight: E.weight,
    my.reddit: E.reddit,
    my.instapaper: E.ip,
    my.pinboard  : E.pinb,
}


end_api = api_node()
endomondo = cluster(
    end_api,
    CLOUD,
    url('https://www.endomondo.com'),
    color=col_end,
    label='Endomondo',
)

# TODO also could show how data gets _into_ the services, i.e. clients?

ip_api = api_node()
instapaper = cluster(
    ip_api,
    CLOUD,
    url('https://www.instapaper.com'),
    color=col_ip,
    label='Instapaper',
)

# TODO for API, could just use special arrow style?
emfit_api = api_node()

emfit_cloud = cluster(
    emfit_api,
    CLOUD,
    label='Emfit',
)

jb_api = api_node()
# TODO demonstrate that it's dead
# TODO not sure. wedged? striped? invert colors?
# TODO better way to mark dead?
jawbone = cluster(
    jb_api,
    CLOUD,
    # DEAD,
    **url('https://en.wikipedia.org/wiki/Jawbone_(company)#UP24'),
    color=col_jb,
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
    bluemaestro,
    wahoo,
    jawbone_band,
    kobo,
    emfit,

    edge(wahoo, app_endomondo, label='BT'),
    edge(jawbone_band, app_jawbone, label='BT'),
    edge(bluemaestro, app_bm, label='BT'),

    # label='Devices',
    # style=dashed,
    INVIS,
)


cluster_enforce_ordering = cluster(
    sleep_subj,
    scales,
    blood_tests,
    INVIS,
)


def generate() -> str:
    items = [
        cluster(
            legend,
            meta,
            edge('legend_ui', sad_infra, INVIS),
            INVIS,
            name='group',
        ),

        phone,

        cluster_enforce_ordering,
        telegram,
        twittercom,

        pinboard,
        reddit,
        vkcom,
        google,
        endomondo,
        instapaper,
        emfit_cloud,
        jawbone,
        devices,
        emfit,
        kobo,
        # syncthing_cl, # TODO maybe should't be a sluster??

        edge(app_endomondo, end_api),
        edge(app_jawbone, jb_api),
        edge(emfit_point, emfit_api),
        # TODO hmm, syncthing could be an edge


        # *edges(app_bm, syncthing, exp_bluemaestro), # TODO here, a rooted script is involved
        # TODO not sure about that..

        orger,
        orger_outputs,
        emacs,
        edge(orger_outputs_point, emacs),

        'subgraph cluster_pipelines {',
        *pipelines(),
        '}',

        '{',
        dashboard,
        timeline,
        promnesia,
        '}',

        # TODO hmm. instead, add 'ports' and mention that ports are attached to syncthing?
        # *edges(app_bm           , exp_bluemaestro  , label='Syncthing', **url('https://syncthing.net')),
        # *edges(app_materialistic, exp_materialistic, label='Syncthing', **url('https://synchting.get')),
        *post(),
    ]
    return '\n'.join(map(render, items))



def main():
    Path('diagram.dot').write_text(generate())


if __name__ == '__main__':
    main()


# TODO meh. okay, I might need some hackery to properly display edge labels...
# https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath

# TODO dot allows comments?

# TODO maybe, use html table? not sure..
# https://renenyffenegger.ch/notes/tools/Graphviz/examples/index

# TODO add hover anchors everywhere

# TODO hmm, use xlabel? it doesn't impact layout, might be useful for edges?

# TODO add emacs as org-mode interface?
