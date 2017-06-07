import threading
import paramiko
import subprocess

from secret import password as pw
from secret import username as un

# netstat -ln | grep 22
# -listen on interfaces -n do not resolve

# service ssh start
# connect local host

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return


ssh_command('localhost', un, pw, 'id')  # id on cmd line, shows groups
# ClientConnect, username, password, command to run

'''
1a. make a new user :
in commandline
$ useradd 'username goes here'
$ passwd 'secret pw goes here'

1b. for safety:
edit your config to not expose ports/yourself to everyone
$ /etc/ssh/sshd_config
to uncomment the ListenAddress: 127.0.0.1

2. run your ssh service.
$ service ssh start

verify running:
$ netstat -ln | grep 22
# -listen on interfaces / -n do not resolve

note:
don't put the ssh key in your .ssh file, b/c public
and someone can connect to your computer.
if you really want to try, generate a new one:
$ ssh-key gen

3. start service
$ service ssh start
'''
