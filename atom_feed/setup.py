from buildbot_pkg import setup_www_plugin


setup_www_plugin(
    name = 'buildbot-atom-feed',
    packages = ['buildbot_atom_feed'],
    install_requires = ['Jinja2', 'klein'],
    package_data = {
        '': ['VERSION', 'static/.placeholder', 'templates/*.j2'],
        },
    entry_points = '''
        [buildbot.www]
        atom_feed = buildbot_atom_feed:ep
        ''',
    )
