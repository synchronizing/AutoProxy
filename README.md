> Depracated for [Frontman](https://github.com/waultics/Frontman). 

# AutoProxy

AutoProxy is a tool designed to make proxy gathering & filtering easy and simple. One of the biggest issue with downloading free proxies online is the lack of knowledge on whether or not the proxy works. AutoProxy makes it easy to gather, filter, and keep track of proxies being utilized for site-specific tasks.

AutoProxy supports both `requests` and `aiohttp`.

**Please note that this is an HTTP proxy gatherer only, and thus websites must be of ```http://``` format! If ```https//``` is used, you will be doing requests from your original IP. Possible addition of ```https``` if requested under Issues.**

![Example](https://i.imgur.com/XVG5KLx.png)

Gathering and filtering 587 proxies in less than 6 seconds, with a timeout of 4 seconds; 109 proxies that work on Twitter with less than 4 second timeout. Code for above:

```Python
from autoproxy import Proxy, Config

c = Config()
c.PRINT_LOG = True
c.PRINT_ERROR_LOG = True

p = Proxy(config = c, url = "http://twitter.com")
p.filter()
```

## Installing

```
git clone https://github.com/synchronizing/AutoProxy.git
cd AutoProxy
pip install .
```

## Using

### Gathering Proxies

Initializing the `Proxy` class automatically gathers proxies from TheBigProxyList, unless the parameter `load` is set to `True`.
```Python
from autoproxy import Proxy

p = Proxy(url = "http://twitter.com")
```

Note that 'load' only loads a previously saved AutoProxy msgpack configuration file. Loading instead:

```Python
from autoproxy import Proxy

p = Proxy(url = "http://twitter.com", load = True, filename = 'Twitter', directory = '/')
```

### Filtering the Proxies

Filtering proxies allows an easy way to check whether or not the proxies gathered works with a specific website. This is done completely asynchronously, and takes seconds to completely with a list of 1,000+ proxies.

```Python
from autoproxy import Proxy

p = Proxy(url = "http://twitter.com")
p.filter(timeout = 10) # Will filter by checking proxies with Twitter.com
```

### Using The Proxies

To use a proxy, simply call the `use_proxy` method.

```Python
from autoproxy import Proxy

p = Proxy(url = "http://twitter.com")
print(p.use_proxy())
{'request_proxy': {'http': '87.98.174.157:3128'}, 'aiohttp_proxy': 'http://87.98.174.157:3128', 'pull_time': 0.24773406982421875, 'used': 1}
```

Notice how the `used` val gets increased by one every time a proxy is called by the `use_proxy` method. This is to keep track of proxy use, depending on application need.

### Configuration

AutoProxy comes with a configuration class for easy management of logs. To print out logs, it is as simple as:

```Python
from autoproxy import Proxy, Config

c = Config()
c.PRINT_LOG = True
c.PRINT_ERROR_LOG = True
p = Proxy(config = c, url = "http://twitter.com")
```
