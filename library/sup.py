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
regex = re.compile(r'(\S+)\s*?\|\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/\d+', re.MULTILINE)

def get_sbc_acls(cookie):
    exit_code, stdout, stderr = process.call_process(['sup', '-c', cookie, '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls', 'acl_summary'])

    if exit_code:
        raise IOError(stderr)

    ips = [match[1] for match in re.findall(regex, stdout)]

    return ips

