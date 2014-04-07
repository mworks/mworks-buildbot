from contextlib import contextmanager
import os
import plistlib
from subprocess import check_call


launchctl = '/bin/launchctl'
plistdir = os.path.expanduser('~/Library/LaunchAgents')


@contextmanager
def launchd_plist(kind):
    plistlabel = 'org.mworks-project.buildbot.' + kind
    plistfile = os.path.join(plistdir, plistlabel + '.plist')
    
    plist = {
        'Label': plistlabel,
        'ProgramArguments': [
            '/usr/bin/twistd',
            '--nodaemon',
            '--python=./buildbot.tac',
            ],
        'KeepAlive': {
            'SuccessfulExit': False,
            },
        'RunAtLoad': True,
        'WorkingDirectory': os.path.join(os.getcwd(), kind),
        'StandardOutPath': 'twistd.log',
        'StandardErrorPath': 'twistd-err.log',
        }
    
    if os.path.isfile(plistfile):
        check_call([launchctl, 'unload', plistfile])
    
    yield
    
    if not os.path.isdir(plistdir):
        os.makedirs(plistdir)
    
    plistlib.writePlist(plist, plistfile)
    
    check_call([launchctl, 'load', plistfile])
