#! /usr/bin/env PYTHONIOENCODING=utf8 PYTHONUNBUFFERED=1 /usr/local/bin/python3

# <bitbar.title>Nagios</bitbar.title>
# <bitbar.version>1.0</bitbar.version>
# <bitbar.author>Samuel Marchal</bitbar.author>
# <bitbar.author.github>zessx</bitbar.author.github>
# <bitbar.desc>Monitor Nagios instance.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/zessx/bitbar-nagios</bitbar.abouturl>

import re
import requests

# <config>
NAGIOS_HOST = 'https://nagios.example.com'
NAGIOS_USERNAME = ''
NAGIOS_PASSWORD = ''
# </config>

if not NAGIOS_HOST or not NAGIOS_USERNAME or not NAGIOS_PASSWORD:
    print("Nagios: config error | color=purple")

try:
    data = str(requests.get("%s/cgi-bin/nagios3/tac.cgi" % NAGIOS_HOST, auth=(NAGIOS_USERNAME, NAGIOS_PASSWORD)).content)

    critical = int(re.search('>(\d+)\sCritical<', data, re.MULTILINE)[1])
    warning = int(re.search('>(\d+)\sWarning<', data, re.MULTILINE)[1])
    unknown = int(re.search('>(\d+)\sUnknown<', data, re.MULTILINE)[1])
    ok = int(re.search('>(\d+)\sOk<', data, re.MULTILINE)[1])

    services = ok + warning + unknown + critical
    color = 'green'
    if critical > 0:
        color = 'red'
    elif warning > 0 or unknown > 0:
        color = 'yellow'

    output = "%u Ok" % ok
    if services != ok:
      first = True
      if critical > 0:
        output = "{} Cri.".format(critical)
        first = False
      if warning > 0:
        output = ('' if first else output + ' / ') + "{} War.".format(warning)
        first = False
      if unknown > 0:
        output = ('' if first else output + ' / ') + "{} Unk.".format(unknown)

    print("Nagios: {} | color={} href={}/cgi-bin/nagios3/status.cgi?host=all&servicestatustypes=28".format(output, color, NAGIOS_HOST))

except requests.exceptions.ConnectionError:
    print("Nagios: host unreachable | color=purple")
