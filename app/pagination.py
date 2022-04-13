import urllib.parse
from flask import abort


class Paginate:
    def __init__(self, results, url, limit=20):
        self.url = url
        self.limit = limit
        self.results = results

    def get_results(self, start):
        self.validate_start(start)
        response = {}
        response["start"] = start
        response["limit"] = self.limit
        response["count"] = self.get_result_count()
        response["next"] = self.get_next_url(start, self.url)
        response["previous"] = self.get_previous_url(start, self.url)
        response["results"] = self.results[(start - 1) : (start - 1 + self.limit)]
        return response

    def get_result_count(self):
        return len(self.results)

    def get_previous_url(self, start, url):
        if start == 1:
            return None
        params = {"start": max(1, start - self.limit), "limit": start - 1}
        return url + "?" + urllib.parse.urlencode(params)

    def get_next_url(self, start, url):
        if start + self.limit > self.get_result_count():
            return None
        params = {"start": start + self.limit, "limit": self.limit}
        return url + "?" + urllib.parse.urlencode(params)

    def validate_start(self, start):
        if len(self.results) < start:
            abort(404)
