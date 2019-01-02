from contextlib import contextmanager
import os
import plistlib
from subprocess import check_call
import sys


buildbot_run_code = {
    'master': 'from buildbot.scripts.runner import run; run()',
    'worker': 'from buildbot_worker.scripts.runner import run; run()'
    }
launchctl = '/bin/launchctl'
plistdir = os.path.expanduser('~/Library/LaunchAgents')


def run_command(kind, *args):
    check_call([
        sys.executable,
        '-c', buildbot_run_code[kind],
        ] + list(args))


@contextmanager
def launchd_plist(kind):
    plistlabel = 'org.mworks-project.buildbot.' + kind
    plistfile = os.path.join(plistdir, plistlabel + '.plist')
    
    plist = {
        'Label': plistlabel,
        'ProgramArguments': [
            sys.executable,
            '-c', buildbot_run_code[kind],
            'start',
            '--nodaemon',
            ],
        'KeepAlive': {
            'SuccessfulExit': False,
            },
        'RunAtLoad': True,
        'WorkingDirectory': os.path.join(os.getcwd(), kind),
        'EnvironmentVariables': {
            'LANG': 'en_US.UTF-8',
            },
        'StandardOutPath': 'twistd.log',
        'StandardErrorPath': 'twistd.log',
        }
    
    if os.path.isfile(plistfile):
        check_call([launchctl, 'unload', plistfile])
    
    yield
    
    if not os.path.isdir(plistdir):
        os.makedirs(plistdir)
    
    plistlib.writePlist(plist, plistfile)
    
    check_call([launchctl, 'load', plistfile])
