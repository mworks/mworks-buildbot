import shutil

from setup_common import launchd_plist, run_command


masterdir = 'master'


with launchd_plist('master'):
    run_command(
        'master',
        'create-master',
        '--relocatable',
        masterdir,
        )
    
    for filename in ('master.cfg', 'master_config.py', 'passwords.py'):
        shutil.copy(filename, masterdir)
