from cli import configure, cli

USER="nohsadmin"
PASSWORD="cisco"
ENABLE="cisco"

def base_config():
    configure(['hostname switch-ztd'])
    configure(['username {} privilege 15 password {}'.format(USER,PASSWORD)])
    configure(['enable secret {}'.format(ENABLE)])
    configure(['line vty 0 4', 'login local'])

base_config()