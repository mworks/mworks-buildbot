# To use this configuration, create a symbolic link to this file named
# "local_config.py"

master_hostname = 'dicarlo-mwdev.mit.edu'
master_admin = 'Christopher Stawarz <cstawarz@mit.edu>'
webstatus_port = 8010

from local_passwords import slave_pass, webstatus_pass
slave_port = 9989

installer_destination_path = '/Library/WebServer/Documents/mw'
