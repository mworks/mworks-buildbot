from datetime import datetime, timedelta, tzinfo

import jinja2
from klein import Klein
from twisted.internet import defer

from buildbot.data.resultspec import Filter
from buildbot.process.results import Results
from buildbot.www.plugin import Application


class UTC(tzinfo):

    def utcoffset(self, dt):
        return timedelta()

    def dst(self, dt):
        return timedelta()

    def tzname(self, dt):
        return 'UTC'


class Api(object):

    app = Klein()

    def __init__(self, ep):
        self.ep = ep
        self.env = jinja2.Environment(loader=jinja2.ChoiceLoader([
            jinja2.PackageLoader('buildbot_atom_feed'),
            jinja2.FileSystemLoader('templates'),
            ]))

    def makeConfiguration(self, request):
        config = {
            'title': self.ep.master.config.title + ': latest builds',
            'author': 'Buildbot atom feed',
            'base_url': self.ep.master.config.buildbotURL,
            'builders': [],
            }
        config.update(self.ep.config)
        return config

    @app.route('/', methods=['GET'])
    @defer.inlineCallbacks
    def feed(self, request):
        config = self.makeConfiguration(request)
        request.setHeader('content-type', 'application/xml')
        request.setHeader('cache-control', 'no-cache')

        latest_builds = []

        for builder_name in config['builders']:
            latest_build = yield self.ep.master.data.get(
                ('builders', builder_name, 'builds'),
                filters = [Filter('complete', 'eq', [True])],
                order = ['-number'],
                limit = 1,
                )
            if latest_build:
                info = latest_build[0]
                info['buildername'] = builder_name

                results = info['results']
                if results >= 0 and results < len(Results):
                    results_string = Results[results]
                else:
                    results_string = 'unknown'
                info['title'] = 'Builder "%s": %s' % (builder_name,
                                                      results_string)

                info['url'] = '%s#/builders/%d/builds/%d' % (config['base_url'],
                                                             info['builderid'],
                                                             info['number'])

                latest_builds.append(info)

        latest_builds.sort(key=(lambda info: info['complete_at']), reverse=True)

        if latest_builds:
            updated = latest_builds[0]['complete_at']
        else:
            updated = datetime.now(UTC())
        config['updated'] = updated

        template = self.env.get_template('atom.xml.j2')
        defer.returnValue(template.render(config=config, builds=latest_builds))


ep = Application(__name__, 'Buildbot atom feed', ui=False)
ep.resource = Api(ep).app.resource()
