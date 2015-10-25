import json
import requests

__all__ = ['NDB']


class NDB(object):
    """
    Class to search the USDA Food Database
    More information here: http://ndb.nal.usda.gov/ndb/doc/apilist/API-SEARCH.md

    In order to search the database, you need an API key.
    """

    def __init__(self, key):
        self._key = key
        self._base_url = "http://api.nal.usda.gov/ndb/{}/?format=json"

    def search_keyword(self, q, **kwargs):
        """
        Searches the database by keyword.

        Optional arguments include:
        - fg: Food group ID, default is ""
        - sort: Sort the results by food name (n) or by search relevance (r),
          default is "r"
        - offset: beggining row in the result set to begin, default is 0
        - max: maximum number of rows to return, default is 50

        Returns a dict with the following keys:
        - q: terms requested and used in the search
        - start: beginning item in the list
        - end: last item in the list
        - offset: beginning offset into the results list for the items in the
          list requested
        - total: total number of items returned by the search
        - sort: requested sort order (r = relevance or n = name)
        - fg: food group filter
        - sr: Standard Release version of the data being reported
        - items: a generator of actual food items, wrapped in the Result object
        """
        kwargs['q'] = q
        kwargs['api_key'] = self._key
        res = requests.get(self._base_url.format("search"), params=kwargs).json()
        items = (SearchResult.from_dict(r) for r in res['list']['item'])
        return {"items": items, "start": res['list']['start'],
                "q": res['list']['q'], "end": res['list']['end'],
                "total": res['list']['total'], "sr": res['list']['sr'],
                "sort": res['list']['sort'], "group": res['list']['group']}

    def search_nutrient_report():
        pass

    def search_list():
        pass

    def food_report():
        pass


class SearchResult(object):
    @staticmethod
    def from_dict(d):
        return SearchResult(d['name'], d['ndbno'],
                            d['offset'], d['group'])

    def __init__(self, name="", ndbno="", offset=0, group=""):
        self._name = name
        self._ndbno = ndbno
        self._offset = offset
        self._group = group

    def name(self):
        """
        :return: the name of the SearchResult
        """
        return self._name

    def ndbno(self):
        """
        :return: the NDBno of the SearchResult
        """
        return self._ndbno

    def offset(self):
        """
        :return: the offset of the SearchResult
        """
        return self._offset

    def group(self):
        """
        :return: the food group of the SearchResult
        """
        return self._group

    def toJSON(self):
        """
        converts this object to JSON
        :return a JSON string
        """
        return json.dumps({n[1:]: self.__dict__[n] for n in self.__dict__})

    def __repr__(self):
        return "Result(name=" + self._name + ", " +\
            "ndbno=" + self._ndbno + ")"


class NutrientReport(object):
    pass
