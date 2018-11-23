"""
Class library for a Proxy.
"""

# In-House Imports
import autoproxy.proxy_scraper as proxy_scraper
from autoproxy.Task import Task
from autoproxy.Config import Config

# Modules Import
import os
import msgpack
import random
import asyncio
import aiohttp
import time
import math
from os import path
from datetime import datetime

class Proxy:
    """ Class for proxy management and configuration.

    Attributes
    ----------
    config : Config() class
        Configuration for the given proxy class.
    url : string
        String containing the proxies URL.
    name : string
        Class type name.

    Methods
    -------
    grab_proxies()
        Grabs the starting proxy list; currently scraping from TheBigProxyList.com
    filter()
        Filters out all of the grabbed proxy with a given URL, and a given timeout.
    print_proxies()
        Prints all of the proxies gatherer. If filtered, will print in order of quickest to slowest.
    use_proxy()
        Returns a proxy, and updates its 'used' counter to 'used += 1'.
    save()
        Saves the current proxy configuration to file.
    load()
        Loads the current proxy configuration from file.
    __str()__
        Returns describing string for the proxy configuration.

    Static Methods
    --------------
    format_aiohttp
        Formats a given requests formatted proxy into an aiohttp formatted proxy.
    storedProxies
        Checks if a given proxy setting is stored to file.
    """

    def __init__(self, url, config = Config(), load = False, filename = '', directory = ''):
        """ Initialization method.

        Parameters
        ----------
        config : Config() class
            A configuration class for variable management.
        url : string
            URL for the given proxy configuration.
        """

        self.config = config
        self.url = url

        self.proxies = []
        self.times = {
            'created': datetime.today(),
            'filtered': None,
        }

        if load:
            self.load(filename = filename, directory = directory)
        else:
            self.grab_proxies()

    def grab_proxies(self):
        """ Grabs the starting proxy list; currently scraping from TheBigProxyList.com

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.grab_proxies()
        """
        proxies = proxy_scraper.grab_proxies()

        for proxy in proxies:
            self.proxies.append({
                    'request_proxy': proxy,
                    'aiohttp_proxy': self.format_aiohttp(proxy),
                    'pull_time': None,
                    'used': 0,
                })

    def filter(self, timeout = 4, keep_timeout = False):
        """ Filters out all of the grabbed proxy with a given URL, and a given timeout.

        Parameters
        ----------
        timeout : int
            Timeout settings to consider a proxy 'not useful'.
        keep_timeout : bool
            Default is false. If true, will delete any proxy that times out.

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.grab_proxies()
        p.filter(timeout = 10, keep_timeout = False)
        """

        async def async_filter(proxy):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url = self.url, proxy = proxy['aiohttp_proxy'], timeout = timeout) as response:
                        start = time.time()
                        body = await response.text()
                        end = time.time()

                asyncio.wait(0)
                object = {
                    'request_proxy': proxy['request_proxy'],
                    'aiohttp_proxy': proxy['aiohttp_proxy'],
                    'pull_time': end-start,
                    'used': 0,
                }

                index = self.proxies.index(proxy)
                self.proxies[index] = object

                log = "Filtered proxy [{}]; pull time to url [{}] was [{}] seconds.".format(proxy['aiohttp_proxy'], self.url, str(end-start))
                self.config.add_log(err = False, log = log)

            except Exception as e:
                object = {
                    'request_proxy': proxy['request_proxy'],
                    'aiohttp_proxy': proxy['aiohttp_proxy'],
                    'pull_time': float('nan'),
                    'used': 0,
                }

                index = self.proxies.index(proxy)
                self.proxies[index] = object

                error = "Error loading page for proxy [{}], or timeout. {}".format(proxy['aiohttp_proxy'], e)
                self.config.add_log(err = True, log = error)

                pass

        start = time.time()
        t = Task()
        for proxy in self.proxies:
            t.add_task(async_filter(proxy = proxy))
        t.run()
        end = time.time()

        self.proxies = sorted(self.proxies, key=lambda k: k['pull_time'])

        new_proxies = []
        for proxy in self.proxies:
            if not math.isnan(proxy['pull_time']):
                new_proxies.append(proxy)

        log = "Filtered [{}] proxies in [{}] seconds, with a timeout of [{}] seconds; [{}] proxies were captured.".format(len(self.proxies), str(end - start), timeout, len(new_proxies))
        self.config.add_log(err = False, log = log)

        if keep_timeout is False:
            self.proxies = new_proxies

        self.times['filtered'] = datetime.today()

    def print_proxies(self):
        """ Prints all of the proxies gatherer. If filtered, will print in order of quickest to slowest.

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.grab_proxies()
        p.print_proxies()
        """

        for proxy in self.proxies:
            print(proxy)

    def use_proxy(self):
        """ Returns a proxy, and updates its 'used' counter to 'used += 1'.

        Returns
        -------
        proxy : dictionary
            Dictionary with proxy information. Format below.

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.grab_proxies()
        p.use_proxy()
        {'request_proxy': proxy, 'aiohttp_proxy': self.format_aiohttp(proxy), 'pull_time': None, 'used': 0}
        """
        proxy = random.choice(self.proxies)
        proxy['used'] = proxy['used'] + 1

        return proxy

    def save(self, filename, directory):
        """ Saves the current proxy configuration to file.

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.grab_proxies()
        p.save('twitter', '/')

        Notes
        -----
        The proxy settings gets saved with the `self.name` as the files name.
        """

        if self.times['filtered'] is None:
            filtered_time = None
        else:
            filtered_time = str(self.times['filtered'].strftime("%Y-%m-%d %H:%M:%S.%f"))

        object = {
            'times': {
                'created': str(self.times['created'].strftime('%Y-%m-%d')),
                'filtered': filtered_time,
            },
            'proxies': self.proxies,
        }

        with open("{}/{}.msg".format(directory, filename), 'wb') as f:
            msgpack.pack(object, f)

    def load(self, filename, directory):
        """ Loads the current proxy configuration from file.

        Example
        -------
        p = Proxy(url = "http://twitter.com")
        p.load('twitter', '/')
        """

        with open("{}/{}.msg".format(directory, filename), 'rb') as f:
            object = msgpack.unpack(f, encoding='utf-8')

        if object['times']['filtered'] is None:
            filtered_time = None
        else:
            filtered_time = datetime.strptime(object['times']['filtered'], "%Y-%m-%d %H:%M:%S.%f")

        self.times = {
            'created': datetime.strptime(object['times']['created'], "%Y-%m-%d"),
            'filtered': filtered_time,
        }

        self.proxies = object['proxies']

    def __str__(self):
        """ Returns describing string for the proxy configuration.

        Returns
        -------
        string
            String that describes the current class configuration.
        """
        return "Proxy for {}; {}. Currently {} proxies in list.".format(self.name, self.url, len(self.proxies))

    @staticmethod
    def format_aiohttp(proxy):
        """ Formats a given requests formatted proxy into an aiohttp formatted proxy.

        Parameters
        ----------
        proxy : dict
            A proxy with the request format; {'http': '127.0.0.1:8080'}

        Returns
        --------
        string
            A string formatted for aiohttp; "http://127.0.0.1:8080"
        """

        try:
            proxy = str(list(proxy.keys())[0]) + "://" + str(proxy[list(proxy.keys())[0]])
        except:
            raise Exception("Proxy inputted [{}] is not a non-aiohttp formatted proxy.".format(proxy))

        return proxy

    @staticmethod
    def storedProxies(filename, directory):
        """ Checks if a given proxy setting is stored to file.

        Parameters
        ----------
        name : string
            Name of the proxy setting.

        Returns
        bool
            Boolean on whether or not the file exists.
        """
        return os.path.exists("{}/{}.msg".format(directory, filename))
