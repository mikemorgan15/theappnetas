# theappnetas

A Python module for making API calls to your 9.x AppNeta appliance, for configuration purposes

Run 'pip install -r requirements.txt' to install dependencies.

### Usage:

```
from theappnetas.appliance import Appliance

appliance = Appliance(host='m25.mydomain.com', username='admin', password='password')

appliance.put_hostname(hostname='my-new-appliance')
appliance.get_hostname()
> 'my-new-appliance'

etc
```

See example.py for full list of available methods.

p.s. not an official AppNeta product.  Use at own risk etc.
