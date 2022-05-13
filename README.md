<p align="center">
  <img src="https://github.com/orklann/caprice/blob/87a3b270c7c8a4df590cb813ac2a45649c3dbbc3/artwork/Caprice_new.png" width=128 height=128 />
</p>


[![PyPI version](https://badge.fury.io/py/caprice.svg)](https://badge.fury.io/py/caprice) 
[![Run Tests](https://github.com/orklann/caprice/actions/workflows/main.yml/badge.svg)](https://github.com/orklann/caprice/actions/workflows/main.yml)  

Caprice
=======
**Caprice** is a robust Python library for generating PDF.

Notes
-----
Caprice is in development, and can not be used in any purpose yet. But It's in rapidly development, just keep watching this repo, you will get surprises.

How to install
--------------
```shell
pip install caprice
```

Usage
-----
```python
from caprice.document import Document

doc = Document()
page = doc.add_page()
page.draw_text(0, 0, "Hello Caprice!")
doc.save("hello.pdf")
```

How to run unit tests
---------------------
```
make test
```

Author
------
[Aaron Elkins](https://twitter.com/ryh1113) ([https://rkt.pixelegg.me](https://rkt.pixelegg.me/))

License
-------
Please see [LICENSE](https://github.com/orklann/caprice/blob/0d250c86b90a6e0bd93d85c7d11b0baa269652b4/LICENSE) for licensing details.
