from parsing_information import parsing


def main() -> None:
    data_parse = parsing(url='https://books.toscrape.com/catalogue/page-1.html')
    parsing_info: list[dict] = data_parse.parse()


if __name__ == '__main__':
    main()
