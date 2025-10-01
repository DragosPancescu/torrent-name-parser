# torrent-name-parser

> Extract media information from torrent-like filenames (modern Python fork)

`torrent-name-parser` extracts media information from torrent-style filenames. This fork modernizes the original [Python port](https://github.com/divijbindlish/parse-torrent-name) by Divij Bindlish of [Jānis’ JavaScript library](https://github.com/jzjzjzj/parse-torrent-name).

It works for both movies and TV episodes by applying multiple regex rules to parse details such as:

* **title**
* **year**
* **resolution**
* **codec**
* **audio**
* **quality**
* **season/episode numbers**
* **release group**
* And more

---

## Why this fork?

The original Python package supports only Python 2.7 / 3.3 and is no longer maintained. This fork:

* Updates code for modern Python (3.8+)
* Publishes under a new PyPI name (`torrent-name-parser`)
* Fixes compatibility issues
* Adds tests and CI for current versions

---

## Installation

```bash
pip install torrent-name-parser
```

---

## Usage

```python
import torrent_name_parser as TNP  # recommended import style

# Movie example
movie_info = TNP.parse("San Andreas 2015 720p WEB-DL x264 AAC-JYK")
print(movie_info)
# Output:
# {
#     'group': 'JYK',
#     'title': 'San Andreas',
#     'resolution': '720p',
#     'codec': 'x264',
#     'year': 2015,
#     'audio': 'AAC',
#     'quality': 'WEB-DL'
# }

# TV episode example
tv_info = TNP.parse("Mr Robot S01E05 HDTV x264-KILLERS[ettv]")
print(tv_info)
# Output:
# {
#     'episode': 5,
#     'season': 1,
#     'title': 'Mr Robot',
#     'codec': 'x264',
#     'group': 'KILLERS[ettv]',
#     'quality': 'HDTV'
# }
```

### Notes

* Fields like `group`, `excess`, and `episodeName` may occasionally be interchanged.
* The library focuses on extracting **core information**; for full metadata (like episode titles), use with an online database (TMDb, TVDb, OMDb).

---

## Parts Extracted

`audio`, `codec`, `container`, `episode`, `episodeName`, `excess`, `extended`, `garbage`,  
`group`, `hardcoded`, `language`, `proper`, `quality`, `region`, `repack`,  
`resolution`, `season`, `title`, `website`, `widescreen`, `year`


---

## Attribution

* Original JavaScript implementation: [Jānis](https://github.com/jzjzjzj)
* Python port: [Divij Bindlish](https://github.com/divijbindlish/parse-torrent-name)
* This fork (Python 3.x updates, ongoing maintenance): [Dragos Pancescu](https://github.com/DragosPancescu)

---

## License

MIT © [Divij Bindlish](http://divijbindlish.in) (original work)  
MIT © [Dragos Pancescu]([https://github.com/yourprofile](https://github.com/DragosPancescu)) (this fork)
