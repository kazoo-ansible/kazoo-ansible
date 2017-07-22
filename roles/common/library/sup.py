import re
import subprocess

class Process:
    def call_process(self, command_list):
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        exitcode = p.returncode

        stdout = stdout.decode('UTF-8')
        stderr = stderr.decode('UTF-8')

        return exitcode, stdout, stderr

process = Process()

# Matches Name  |  IP
_regex = re.compile(r'(\S+)\s*?\|\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/\d+', re.MULTILINE)

def get_sbc_acls(cookie):
    exit_code, stdout, stderr = _sup_ecallmgr(cookie, ['sbc_acls', 'acl_summary'])

    ips = [match[1] for match in re.findall(_regex, stdout)]

    return ips

def add_sbc_acl(cookie, ip):
    _sup_ecallmgr(cookie, ['allow_sbc', ip, ip])

def remove_sbc_acl(cookie, ip):
    exit_code, stdout, stderr = _sup_ecallmgr(cookie, ['sbc_acls', 'acl_summary'])

    matches = [match for match in re.findall(_regex, stdout) if match[1] == ip]

    for match in matches:
        _sup_ecallmgr(cookie, ['remove_acl', match[0]])

def get_fs_nodes(cookie):
    exit_code, stdout, stderr = _sup_ecallmgr(cookie, ['list_fs_nodes'])

    nodes = [line.replace('freeswitch@', '') for line in stdout.splitlines()]

    return nodes

def add_fs_node(cookie, fs_node):
    try:
        _sup_ecallmgr(cookie, ['add_fs_node', 'freeswitch@' + fs_node])
    except IOError as err:
        if '{error,node_exists}' not in str(err):
            raise err

def remove_fs_node(cookie, fs_node):
    _sup_ecallmgr(cookie, ['remove_fs_node', 'freeswitch@' + fs_node])

def import_media(cookie):
    _sup_kazoo_apps(cookie, ['kazoo_media_maintenance', 'import_prompts', '/opt/kazoo/sounds/en/us/'])

def _sup(cookie, args):
    cmd = ['sup', '-c', cookie]
    cmd.extend(args)
    
    exit_code, stdout, stderr = process.call_process(cmd)
    
    if exit_code:
        raise IOError(stdout)
    
    return exit_code, stdout, stderr

def _sup_kazoo_apps(cookie, args):
    cmd = ['-n', 'kazoo_apps']
    cmd.extend(args)

    return _sup(cookie, cmd)

def _sup_ecallmgr(cookie, args):
    cmd = ['-n', 'ecallmgr', 'ecallmgr_maintenance']
    cmd.extend(args)

    return _sup(cookie, cmd)

