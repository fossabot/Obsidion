# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obsidion',
 'obsidion.cogs.botlist',
 'obsidion.cogs.config',
 'obsidion.cogs.fun',
 'obsidion.cogs.hypixel',
 'obsidion.cogs.images',
 'obsidion.cogs.info',
 'obsidion.cogs.minecraft',
 'obsidion.cogs.misc',
 'obsidion.cogs.rcon',
 'obsidion.cogs.redstone',
 'obsidion.cogs.servers',
 'obsidion.core',
 'obsidion.utils']

package_data = \
{'': ['*'], 'obsidion.cogs.fun': ['resources/*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'aiohypixel>=0.2.1,<0.3.0',
 'aioredis>=1.3.1,<2.0.0',
 'asyncpg>=0.21.0,<0.22.0',
 'asyncrcon>=1.1.4,<2.0.0',
 'beautifulsoup4>=4.9.2,<5.0.0',
 'discord.py>=1.5.0,<2.0.0',
 'fakeredis>=1.4.3,<2.0.0',
 'feedparser>=6.0.1,<7.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.5.2,<5.0.0',
 'mcsrvstats>=0.1.1,<0.2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'uvloop>=0.14.0,<0.15.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'obsidion',
    'version': '0.4.0',
    'description': 'A Minecraft discord bot',
    'long_description': None,
    'author': 'Darkflame72',
    'author_email': 'leon@bowie-co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
