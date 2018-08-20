# AutoProxy

AutoProxy is a tool designed to make proxy gathering & filtering easy and simple. One of the biggest issue with downloading free proxies online is the lack of knowledge on whether or not the proxy works. AutoProxy makes it easy to gather, filter, and keep track of proxies being utilized for site-specific tasks.

AutoProxy supports both `requests` and `aiohttp`.

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

Loading instead:

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
from autoproxy import Proxy

c = Config()
c.PRINT_LOG = True
c.PRINT_ERROR_LOG = True
p = Proxy(config = c, url = "http://twitter.com")
```
