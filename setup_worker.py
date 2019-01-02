import os
import pwd
import socket
import subprocess
import sys

import master_config
from passwords import worker_pass
from setup_common import launchd_plist, run_command


workername = sys.argv[1]
workerdir = 'worker'

master_hostname = master_config.hostname
if master_hostname == socket.getfqdn():
    master_hostname = 'localhost'


with launchd_plist('worker'):
    run_command(
        'worker',
        'create-worker',
        '--relocatable',
        '--umask=022',
        workerdir,
        '%s:%d' % (master_hostname, master_config.worker_port),
        workername,
        worker_pass[workername],
        )

    with open(os.path.join(workerdir, 'info/admin'), 'w') as fp:
        # Write current user's full name
        fp.write(pwd.getpwuid(os.getuid())[4] + '\n')

    with open(os.path.join(workerdir, 'info/host'), 'w') as fp:
        fp.write(subprocess.check_output([
            '/usr/sbin/system_profiler',
            '-detailLevel', 'mini',
            'SPHardwareDataType',
            ]))
