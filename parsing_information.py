import json
import requests
from requests import Response
from itertools import zip_longest
from parsel import Selector
from working_files import WorkingWithFiles


# pip install requests parsel


class parsing(WorkingWithFiles):
    def __init__(self, url):
        self.final_list = None
        self.position = None
        self.availabilities = None
        self.page = None

        self.url = url
        self.naked_url = "https://books.toscrape.com/catalogue/"
        self.headers = self.get_headers()
        self.response = self.make_request()
        self.make_html(response=self.response)
        self.data_list(self.parse())
        self.make_json(data=self.final_list)

    def get_headers(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/122.0.0.0 Safari/537.36',
        }

    def make_request(self) -> Response:
        return requests.get(url=self.url, headers=self.headers)

    def parse(self):

        self.final_list: list = []
        self.position: int = 0
        self.page: int = 0

        while True:
            self.availabilities: list[list[str]] = []
            self.page = self.page + 1
            print(self.page)

            selector = Selector(text=self.response.text)
            for product in selector.css('article.product_pod'):
                stock = product.xpath(
                    'normalize-space(.//div[@class="product_price"]/p[contains(@class, "availability")])').getall()
                self.availabilities.append(stock)

            ratings = selector.css('article.product_pod p.star-rating')
            ratings = ratings.css('p::attr(class)').getall()

            titles = selector.css('article.product_pod h3 a::attr(title)').getall()

            links = selector.css('article.product_pod h3 a::attr(href)').getall()

            prices = selector.css('p.price_color::text').getall()

            links_image = selector.css('div.image_container a img::attr(src)').getall()

            for price, link, title, link_image, rating, availability in zip_longest(prices, links, titles, links_image,
                                                                                    ratings,
                                                                                    self.availabilities):
                for ava in availability:
                    availability = str(ava)  # Я перевожу список в рядок, щоб текст виводився без дужок

                self.position += 1
                self.final_list.append({
                    f"{self.position}. {title}": f"Price {price[1::]}. {availability}. Rating {rating[12::]}/Five. Link "
                                                 f"to buy '{self.naked_url}{link}'. Link to look an image '{self.url}/"
                                                 f"{link_image}'"})
            next_button = selector.css('li.next a::attr(href)').get()
            if next_button:
                new_url = "https://books.toscrape.com/catalogue/" + next_button
                self.response = requests.get(url=new_url, headers=self.headers)
            else:
                break
        return self.final_list

    def data_list(self, data):
        print(json.dumps(data, indent=2, ensure_ascii=False))