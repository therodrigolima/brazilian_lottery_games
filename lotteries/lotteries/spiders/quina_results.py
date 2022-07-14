import logging
import scrapy
import ipdb
import requests

from pprint import pprint

ip = ipdb.set_trace


class Spider(scrapy.Spider):
    name = "quina_results"

    URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/quina/{0}"

    def start_requests(self):
        url = self.URL
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "servicebus2.caixa.gov.br",
            "Origin": "https://loterias.caixa.gov.br",
            "Referer": "https://loterias.caixa.gov.br/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        }
        meta = {}
        yield scrapy.Request(
            url=url.format(""), meta=meta, headers=headers, callback=self.get_games
        )

    def get_games(self, response):
        data = response.json()
        game_last_number = data.get("numero") + 1

        for number in range(1, game_last_number):
            url = self.URL.format(number)
            yield scrapy.Request(url=url, callback=self.run_games)

    def run_games(self, response):
        data = response.json()

        yield data