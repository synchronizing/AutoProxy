from autoproxy import Proxy, Config

c = Config()
c.PRINT_LOG = True
c.PRINT_ERROR_LOG = True

p = Proxy(config = c, url = "http://twitter.com")
p.filter()
