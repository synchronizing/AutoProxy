"""
Function library for Proxy gathering.
"""

# In-House Import
from autoproxy.settings import BIGPROXYLIST_PASS

# Modules Import
import requests

def grab_proxies():
    """ Grabs a list of free proxies from a TheBigProxyList service.

    Returns
    -------
    list
        A list of dictionaries formatted as requests proxy setting.

    Notes
    -----
    The return of this function is specifically to be utilized with 'requests',
    not 'aiohttp'. Proxies from here are formatted within the Proxy() class for
    aiohttp use.
    """
    r = requests.get('http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass={}'.format(BIGPROXYLIST_PASS))

    proxies = []
    for i in r.text.split('\n'):
        curr = i.split(',')[0]
        proxies.append({'http': curr})
    proxies = proxies[:-1]

    return proxies
