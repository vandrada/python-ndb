# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

__all__ = ['NDB']


class NDB(object):
    """
    Class to search the USDA Food Database
    More information here:
        http://ndb.nal.usda.gov/ndb/doc/apilist/API-SEARCH.md

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
        res = requests.get(self._base_url.format("search"),
                           params=kwargs).json()
        items = (SearchResult.from_dict(r) for r in res['list']['item'])
        return {"items": items, "start": res['list']['start'],
                "q": res['list']['q'], "end": res['list']['end'],
                "total": res['list']['total'], "sr": res['list']['sr'],
                "sort": res['list']['sort'], "group": res['list']['group']}

    def search_nutrient_report():
        pass

    def search_list():
        pass

    def food_report(self, ndbno, **kwargs):
        """
        Searches the database for a food report.

        Optional arguments include:
        - type: report type, [b]asic or [f]ull or [s]tats; default is b

        Returns a dict with the following keys:
        - food: a FoodReport object
        - sr: standard release version
        - footnotes
        """
        kwargs['ndbno'] = ndbno
        kwargs['api_key'] = self._key
        res = requests.get(self._base_url.format("reports"),
                           params=kwargs).json()
        food = FoodReport.from_dict(res['report']['food'])
        return {"sr": res['report']['sr'], "type": res['report']['type'],
                "footnotes": res['report']['footnotes'], "food": food}


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

    def get_name(self):
        """
        :return: the name of the SearchResult
        """
        return self._name

    def get_ndbno(self):
        """
        :return: the NDBno of the SearchResult
        """
        return self._ndbno

    def get_offset(self):
        """
        :return: the offset of the SearchResult
        """
        return self._offset

    def get_group(self):
        """
        :return: the food group of the SearchResult
        """
        return self._group

    def __str__(self):
        return self._name

    def __repr__(self):
        return "Result(name={}, ndbno={}".format(self._name, self._ndbno)


class FoodReport(object):
    @staticmethod
    def from_dict(d):
        nutrients = [Nutrient.from_dict(n) for n in d['nutrients']]
        return FoodReport(name=d['name'], ndbno=d['ndbno'],
                          nutrients=nutrients)

    def __init__(self, name="", ndbno="", nutrients=[]):
        self._name = name
        self._ndbno = ndbno
        self._nutrients = nutrients

    def get_name(self):
        return self._name

    def get_ndbno(self):
        return self._ndbno

    def get_nutrients(self):
        return self._nutrients

    def __str__(self):
        return "{} Report".format(self._name)

    def __repr__(self):
        return "FoodReport(name={}, ndbno={}, nutrients={})".format(
            self._name, self._ndbno, self._nutrients)


class Nutrient(object):
    """
    Nutrient class used by FoodReport
    """
    @staticmethod
    def from_dict(d):
        measures = [] if d.get('measures', None) is None else \
            [Measure.from_dict(m) for m in d['measures']]

        return Nutrient(nutrient_id=d.get('nutrient_id', ''),
                        name=d.get('name', ''),
                        sourcecode=d.get('sourcecode', ''),
                        unit=d.get('unit', ''),
                        value=d.get('value', ''),
                        group=d.get('group', ''),
                        se=d.get('se', ''),
                        dp=d.get('dp', ''),
                        measures=measures)

    def __init__(self, nutrient_id="", name="", group="", unit="", value="",
                 sourcecode="", dp="", se="", measures=[]):
        self._nutrient_id = nutrient_id
        self._name = name
        self._group = group
        self._sourcecode = sourcecode
        # to handle micrograms
        self._unit = unit.encode('utf8')
        self._value = value
        self._dp = dp
        self._se = se
        self._measures = measures

    def get_nutrient_id(self):
        return self._nutrient_id

    def get_name(self):
        return self._name

    def get_group(self):
        return self._group

    def get_sourcecode(self):
        return self._sourcecode

    def get_unit(self):
        return self._unit

    def get_value(self):
        return self._value

    def get_dp(self):
        return self._dp

    def get_se(self):
        return self._se

    def measures(self):
        return self._measures

    def __str__(self):
        return self._name

    def __repr__(self):
        return """Nutrient(nutrient_id={}, name={}, sourcecode={}, unit={},
            value={}, measures=<{}>)""".format(
            self._nutrient_id, self._name, self._sourcecode,
            self._unit, self._value, len(self._measures))


class Measure(object):
    """
    The Measure class represents the nutrient measurements returned by a food
    report
    """

    @staticmethod
    def from_dict(d):
        return Measure(label=d.get('label', ''), eqv=d.get('eqv', ''),
                       qty=d.get('qty', ''), value=d.get('value', ''))

    def __init__(self, label="", eqv="", qty="", value=""):
        self._label = label
        self._eqv = eqv
        self._qty = qty
        self._value = value

    def get_label(self):
        return self._label

    def get_eqv(self):
        return self._eqv

    def get_qty(self):
        return self._qty

    def get_value(self):
        return self._value

    def __str__(self):
        return self._label()

    def __repr__(self):
        return "Measure(label={}, eqv={}, qty={}, value={})".format(
            self._label, self._eqv, self._qty, self._value)
