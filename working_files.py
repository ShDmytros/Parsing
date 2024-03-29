from requests import Response
import json


class WorkingWithFiles:
    def make_html(self, response: Response) -> None:
        with open("name.html", "w", encoding="utf-8") as file:
            file.write(response.text)

    def read_html(self) -> str:
        with open('name.html', 'r', encoding='utf-8') as file:
            html = file.read()
        return html

    def make_json(self, data) -> None:
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
