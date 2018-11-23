from autoproxy import Proxy, Config

p = Proxy(url = "http://twitter.com")
p.filter()

# This method will not keep track of how many times you've used the proxies.
for i in p.proxies:
    print(i)

# To keep track of proxy use, instead, use:
print(p.use_proxy())

# Notice on running this, the last proxy `used` value will be 1.
