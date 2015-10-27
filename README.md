# python-ndb

*python-ndb* is a simple wrapper around the
[National Nutrient Database](http://ndb.nal.usda.gov/ndb/search) REST API

## Installation
TODO

## Prerequisites
- [requests](http://docs.python-requests.org/en/latest/)

## Example
```python
import ndb

n = ndb.NDB(YOUR_KEY_HERE)
tofus = n.search_keyword("tofu")
tofu = list(tofus['items'])[0]
print tofu

report = n.food_report(tofu.get_ndbno())
print report['food'].get_nutrients()[0]
```

## Contributing
Is the current code not meeting your needs? Pull-requests are more than welcome!

Just hack away and format your code according to
[PEP 8](https://www.python.org/dev/peps/pep-0008/).

## Legalese
Suggested citation:

> U.S. Department of Agriculture, Agricultural Research Service. 2014. USDA
> National Nutrient Database for Standard Reference, Release . Nutrient Data
> Laboratory Home Page, http://www.ars.usda.gov/nutrientdata
