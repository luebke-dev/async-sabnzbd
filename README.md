# async-sabnzbd
Python wrapper for SABnzbd API

```python

import asyncio
from async_sabnzbd.sabnzbd import Sabnzbd

async def main():
    sabnzbd = Sabnzbd(api_key="mykey", base_url="http://mysabnzbdurl")
    queue = await sabnzbd.queue()
    print(queue)

asyncio.run(main())
```