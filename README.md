# cigarpriser

Recently I took up the hobby of smoking the occasional cigar. A lot of webshops in Denmark sell cigars online, but it's a nightmare to compare sizes and prices as they're all categorized by brand, and you can only filter cigars from one particular brand. This repo hopes to become a collection of scrapers for different cigar webshops in Denmark (and potentially the US as I'm moving there this year), to make it easy for everyone to compare.

If you just want the scraped results, get the .csv files from the "results" directory. I cannot guarantee that they're updated to reflect the latest prices. One of these days I'll look into whether a Github Action can automate this process, but I do not have the time at the moment.

I'd probably be best to download the scrapers and run them for yourself, if you want to ensure that the data is up-to-date.

To run all scrapers, simply type:

```python
python3 main.py
```
And wait until they finish. They'll create and replace the .csv-files automatically.

Make sure to install BeautifulSoup 4 beforehand, though.

```python
pip3 install bs4
```


I hope to create a tool to handle the repetitive tasks, and let new scrapers hook into it, making it easier to add new scrapers. That's in the future.

Please feel free to create a new issue if there's anything I can help with.

## Supported webshops
| Webshop name  | Webshop URL |
| ------------- | ------------- |
| Cognachuset  | http://cognachuset.dk  |
| Havnens Vin  | http://havnens-vin.dk  |


License-wise, use this code however you please. Consider it your own.
