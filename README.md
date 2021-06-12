# Rainbow Six Siege 🕹 Player 👨‍🚀 stats 💹 Tracker 🖲

![](https://img.shields.io/badge/scrapy-v2.5.0-brightgreen)

It is a rainbow six siege players stats tracker Built with  Srcapy(Python).

Step 1: Install scrapy

```
pip install scrapy
```

Step 2: Clone project to you local directory

Step 3: Go to Project directory e.g. .../r6stats

step 4: openn terminal and run following command.

```
scrapy crawl r6st -a p=[playername] -a pl=[plaform]

e.g. = scrapy crawl r6st -a NaMeles_hOstAge pl=pc
```

This will run spider and scrap the data, but it won't store the data.

for storing data into *json* or *csv*  run follwing command.

```
scrapy crawl r6st -a p=[playername] -a pl=[plaform] -o [filename/path]

e.g. = scrapy crawl r6st -a NaMeles_hOstAge pl=pc -o data.json
```

Given example will store the data into data.json file.

You can also make class of the spider and use it in your project host it locally using  [Scrapyd](https://github.com/scrapy/scrapyd) .

If you like my work, Check out other works I do.

Feel free to raise any issue or to request new feature.

Contact:

IG: [🌚乃卄卂ᐯ乇丂卄🌝 (@\_chevi.\_)](https://www.instagram.com/_chevi._/)

Mail: [Gmail](mailto:bsmarty978@gmail.com)

