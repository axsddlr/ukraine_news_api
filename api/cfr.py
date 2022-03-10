# https://microsites-live-backend.cfr.org/alerts/json?conflict=6482&page=0&items_per_page=10
import re

import httpx
import requests
from bs4 import BeautifulSoup

from utils.utils import headers


class Cfr:
    @staticmethod
    def cfr_conflict_news():
        URL = "https://microsites-live-backend.cfr.org/alerts/json?conflict=6482&page=0&items_per_page=25"
        response = requests.get(URL, headers=headers)
        status = response.status_code
        json_response = response.json()
        # return json_response

        results = []
        for each in json_response:
            title = each["title"]
            date = each["date"]
            url = "https://microsites-live-backend.cfr.org" + each["url"]
            excerpt = each["body"]
            excerpt = excerpt.split("<a")[0]
            excerpt = excerpt.split(" (")[0]
            excerpt = excerpt.split("<p>")[1]

            results.append(
                {
                    "title": title,
                    "url": url,
                    "date": date,
                    "excerpt": excerpt,
                }
            )

            # data = {"status": status, "data": result}
        if status != 200:
            raise Exception("API response: {}".format(status))
        return results

    @staticmethod
    def cfr_status():
        URL = "https://www.cfr.org/global-conflict-tracker/conflict/conflict-ukraine"
        html = httpx.get(URL, headers=headers)
        soup = BeautifulSoup(html.content, "lxml")
        status = html.status_code

        base = soup.find(class_=re.compile("conflict__hero--conventions"))

        cfr_module = base.find_all(class_=re.compile("conflict__hero--conventions-wrapper"))
        # return cfr_module

        result = []
        for module in cfr_module:
            # Titles of articles
            region = module.select("p.article-header__metadata-type--with-definition")[1].text.strip()
            impact = module.select("p.article-header__metadata-type--with-definition")[2].text.strip()
            conflict_status = module.select("p.article-header__metadata-type--with-definition")[3].text.strip()
            type_of = module.select("p.article-header__metadata-type--with-definition")[4].text.strip()
            result = (
                {
                    "region": region,
                    "impact_us": impact,
                    "conflict_status": conflict_status,
                    "type_of_conflict": type_of,
                }
            )

        data = {"status": status, "data": result}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    print(Cfr.cfr_status())
