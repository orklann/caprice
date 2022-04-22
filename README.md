<p align="center">
  <img src="https://github.com/orklann/caprice/blob/87a3b270c7c8a4df590cb813ac2a45649c3dbbc3/artwork/Caprice_new.png" width=128 height=128 />
</p>

[![Run Tests](https://github.com/orklann/caprice/actions/workflows/main.yml/badge.svg)](https://github.com/orklann/caprice/actions/workflows/main.yml)  

Caprice
=======
**Caprice** is a robust Python library for generating PDF.

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
python -m unittest
```

Author
------
[Aaron Elkins](https://twitter.com/ryh1113) ([https://rkt.pixelegg.me](https://rkt.pixelegg.me/))
