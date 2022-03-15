import httpx

from utils.utils import headers


class BBC:
    @staticmethod
    def bbc_ukraine_news():
        url = "https://push.api.bbci.co.uk/batch"
        querystring = {"t": "/data/bbc-morph-{lx-commentary-data-paged/about/d0b3af0d-c4e5-4bbf-a3ec-3e28d82589a8"
                            "/isUk/false/limit/20/nitroKey/lx-nitro/pageNumber/0/version/1.5.6,"
                            "lx-commentary-data-paged/about/d0b3af0d-c4e5-4bbf-a3ec-3e28d82589a8/isUk/false/limit/20"
                            "/nitroKey/lx-nitro/pageNumber/1/version/1.5.6,"
                            "lx-commentary-data-paged/about/d0b3af0d-c4e5-4bbf-a3ec-3e28d82589a8/isUk/false/limit/20"
                            "/nitroKey/lx-nitro/pageNumber/50/version/1.5.6}?timeout=5"}

        response = httpx.get(url, headers=headers, params=querystring)
        status = response.status_code
        json_response = response.json()
        # return json_response

        base = json_response["payload"]

        for each in base:
            body = each["body"]["results"]
            results = []
            for each1 in body:
                try:
                    summary = each1["summary"]
                except:
                    summary = "not available"
                title = each1["title"]

                try:
                    url = each1["url"]
                except:
                    url = "not available"
                date = each1["lastPublished"]
                try:
                    image = each1["image"]["href"]
                except:
                    image = "not available"

                results.append(
                    {
                        "title": title,
                        "summary": summary,
                        "url": "https://bbc.com" + url,
                        "image": image,
                        "date": date,
                    }
                )

            data = {"status": status, "data": results}

            if status != 200:
                raise Exception("API response: {}".format(status))
            return data
            #


if __name__ == '__main__':
    print(BBC.bbc_ukraine_news())
