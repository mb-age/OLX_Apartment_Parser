import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://www.olx.pl'
CITY = 'krakow'
APARTMENTS_URL = f'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{CITY}/'

# url from site filtered by price (1000-2000 PLN)
APARTMENTS_URL_FILTERED = f'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{CITY}/?search%5Bfilter_float_price:from%5D=1000&search%5Bfilter_float_price:to%5D=2000'

MIN_PRICE = 1000
MAX_PRICE = 2001

MIN_AREA = 19
MAX_AREA = 200

MIN_FLOOR = 1
MAX_FLOOR = 10

MIN_ROOM_COUNT = 1
MAX_ROOM_COUNT = 4

PATTERN_1 = r'centraln\w*[\s\-:\n]*ogrzewan'
PATTERN_2 = r'ogrzewan\w*[\s\-:\n]*centraln'
PATTERN_3 = r'miejsk'
PATTERN_4 = r'MPEC'
DISTRICT_HEATING = [PATTERN_1, PATTERN_2, PATTERN_3, PATTERN_4]

LOCATIONS = [
    'Krowodrza',
    'Stare Miasto',
    'Podgórze',
    'Grzegórzki',
    'Prądnik Czerwony',
    'Śródmieście',
]

AD_TYPES = [
    'Firmowe',
    'Prywatne',
]

BUILDING_TYPES = [
    'Dom wolnostojący',
    'Blok',
    'Kamienica',
    'Szeregowiec',
    'Apartamentowiec',
    'Loft',
    'Pozostałe',
]


def get_pages_count(url: str) -> int:
    """
        The function `get_pages_count` takes a URL as input, sends a GET request to the URL, parses the HTML
        response, finds the page numbers on the page, and returns the total number of pages.

        :param url: The `url` parameter is a string that represents the URL of a webpage
        :return: the number of pages found on the given URL.
    """
    request = requests.get(url)
    html: str = BeautifulSoup(request.text, 'html.parser')
    page_numbers: list = html.find_all('a', class_='css-1mi714g')
    if page_numbers:
        page_count: int = int(page_numbers[-1].text)
    return page_count


def get_page_url(url: str, page: int) -> str:
    """
        The function takes a URL and a page number as input and returns a modified URL with the page number
        appended as a query parameter.

        :param url: The `url` parameter is a string representing the base URL of a webpage
        :param page: The `page` parameter is an integer that represents the page number
        :return: a modified URL string with the page number appended as a query parameter.
    """
    if '?' in url:
        url: str = url.replace('?', f'?page={page}&')
    else:
        url: str = f'{url}?page={page}'
    return url


def get_apartment_cells(url: str) -> list:
    """
        The function takes a URL as input, retrieves the HTML content from that URL,
        and returns a list of apartment cells found in the HTML.

        :param url: The URL of the webpage from which you want to extract the apartment cells
        :return: a list of apartment cells.
    """
    request = requests.get(url)
    html = BeautifulSoup(request.text, 'html.parser')
    apartments: list = html.find_all('div', class_='css-1sw7q4x')
    return apartments


def get_single_apartment(url: str) -> list:
    """
        The function takes a URL as input, retrieves the HTML content of the webpage,
        and returns a list of apartment data extracted from the HTML.

        :param url: The `url` parameter is a string that represents the URL of a webpage containing
        apartment data
        :return: a list of apartment data.
    """
    request = requests.get(url)
    html = BeautifulSoup(request.text, 'html.parser')
    apartment_data: list = html.find_all('div', class_='css-1wws9er')
    return apartment_data


def get_price(apartment) -> float | None:
    """
        The function extracts the price of an apartment from its HTML representation and returns
        it as a float, or returns None if the price cannot be found.

        :param apartment: The parameter "apartment" is a BeautifulSoup object
        representing an apartment listing
        :return: the price of the apartment as a float value.
    """
    if apartment.find('p'):
        price_html = apartment.find('p', {'class': 'css-10b0gli er34gjf0'})
        price: float = float(price_html.text.split(' zł')[0].replace(' ', '').replace(',', '.'))
        return price


def get_location(apartment) -> str | None:
    """
        The function extracts the district name from an HTML element representing an apartment.

        :param apartment: The parameter "apartment" is a BeautifulSoup object
        representing an apartment listing
        :return: a string value representing the district of the apartment.
    """
    if apartment.find('p'):
        location_html = apartment.find('p', {'class': 'css-veheph er34gjf0'})
        location: str = location_html.text.split(' - ')[0].split(', ')[1]
        return location


def get_area(apartment) -> float:
    """
        The function extracts the area of an apartment from an HTML element.

        :param apartment: The parameter "apartment" is a BeautifulSoup object
        representing an apartment listing
        :return: the area of the apartment as a float value.
    """
    if apartment.find('span'):
        area_html = apartment.find('span', {'class': 'css-643j0o'})
        area: float = float(area_html.text.split()[0].replace(',', '.'))
        return area


def get_precondition(apartment) -> bool:
    """
        The function checks if an apartment meets certain conditions based on its price, location, and area.

        :param apartment: The "apartment" parameter is the BeautifulSoup object that represents an apartment object.
        It is used to retrieve information about the apartment such as its price, location, and area
        :return: a boolean value, which represents whether the given apartment meets the specified
        preconditions.
    """
    price: float = get_price(apartment)
    location: str = get_location(apartment)
    area: float = get_area(apartment)

    price_condition: bool = MIN_PRICE <= price <= MAX_PRICE if price else False
    location_condition: bool = location in LOCATIONS
    area_condition: bool = MIN_AREA <= area <= MAX_AREA if area else False
    precondition: bool = price_condition and location_condition and area_condition
    return precondition


def get_floor(paragraphs_list: list) -> int | None:
    """
        The function takes a list of paragraphs as input and returns the floor number mentioned
        in the paragraphs, or None if no floor number is found.

        :param paragraphs_list: The `paragraphs_list` parameter is a list of strings representing paragraphs
        of text
        :return: The function returns an integer value representing the floor number if it is
        found in the given list of paragraphs. If the floor number is not found or if there is an error, it
        returns `None`.
    """
    try:
        floor: str = next(p for p in paragraphs_list if 'Poziom' in p).split()[-1]
        floor: int = 0 if floor == 'Parter' else -1 if floor == 'Suterena' else 4 if floor == 'Poddasze' else int(floor)
    except:
        floor: None = None
    return floor


def get_building_type(paragraphs_list: list) -> str | None:
    """
        The function takes a list of paragraphs and returns the building type if it is
        found in one of the paragraphs, otherwise it returns None.

        :param paragraphs_list: A list of paragraphs, where each paragraph is a string
        :return: The function `get_building_type` returns a string representing the building type if it is
        found in the list of paragraphs. If the building type is not found, it returns `None`.
    """
    try:
        building_type: str = next(p for p in paragraphs_list if 'Rodzaj zabudowy' in p).split(': ')[-1]
    except:
        building_type: None = None
    return building_type


def get_room_count(paragraphs_list: list) -> int:
    """
        The function takes a list of paragraphs as input and returns the number of rooms
        mentioned in the paragraphs.

        :param paragraphs_list: The `paragraphs_list` parameter is a list of strings, where each string
        represents a paragraph of text
        :return: an integer value, which represents the number of rooms in a given list of paragraphs.
    """
    try:
        room_count: str = next(p for p in paragraphs_list if 'Liczba pokoi' in p).split(': ')[-1].split()[0]
        room_count: int = 1 if room_count == 'Kawalerka' else int(room_count)
    except:
        room_count: int = 0
    return room_count


def get_full_price(apartment, paragraphs_list: list) -> float:
    """
        The function calculates the full price of an apartment by adding the price and rent, if available.

        :param apartment: The "apartment" parameter is the BeautifulSoup object that represents the
        apartment for which we want to calculate the full price.
        :param paragraphs_list: The `paragraphs_list` parameter is a list of strings. Each string represents
        a paragraph of text
        :return: a float value, which represents the full price of an apartment.
    """
    price: float = get_price(apartment)
    try:
        rent: str = next(p for p in paragraphs_list if 'Czynsz' in p)
        rent: float = float(rent.split(': ')[-1].split(' zł')[0] \
                            .replace(' ', '').replace(',', '.'))
        full_price: float = price + rent if not price == rent else price
    except:
        full_price: float = price
    return full_price


def get_apartment_info(apartment, apartment_data) -> str:
    """
        The function extracts information about an apartment from HTML data and returns it as a string.

        :param apartment: The "apartment" parameter is a BeautifulSoup object representing a specific
        apartment listing on a website
        :param apartment_data: The `apartment_data` parameter is a list containing the HTML elements that
        represent the apartment information
        :return: a string that contains the ad title and ad content of the apartment.
    """
    title: str = apartment.find('h6', {'class': 'css-16v5mdi er34gjf0'}).text.lower()
    content: str = apartment_data[0].find('div', {'class': 'css-1t507yq er34gjf0'}).text.lower()
    info: str = f'{title}\n{content}'
    return info


def get_apartment_link(apartment) -> str:
    """
        The function extracts the link to an apartment from a given HTML element and returns it.

        :param apartment: The "apartment" parameter is a BeautifulSoup object that represents the apartment
        :return: the apartment link.
    """
    link: str = apartment.find('a', {'class': 'css-rc5s2u'}).get('href')
    if link.startswith('/'):
        apartment_link: str = MAIN_URL + link
        return apartment_link
    else:
        third_party_site_link: str = link
        # TODO serve third party sites


def apartment_presentation(chosen_apartments: list) -> None:
    """
        The function `apartment_presentation` takes a list of apartments and prints information about each
        apartment.

        :param chosen_apartments: A list of apartments that have been chosen for presentation.
    """
    for apartment in chosen_apartments:
        link, location, price, area, building_type, floor, rooms, info = apartment
        print('\n\n', '-' * 120)
        print(link)
        print(location)
        print(price, 'zł')
        print(area, 'm3')
        print(building_type)
        print(floor, 'floor')
        print(rooms, 'room' if rooms < 2 else 'rooms')
        print(info, end='\n\n')


def olx_parser(apartments_url: str = APARTMENTS_URL) -> list:
    """
        The `olx_parser` function parses apartment listings from a given URL and filters them based on
        specified criteria, returning a list of chosen apartments.

        :param apartments_url: The `apartments_url` parameter is the URL of the website where the apartments
        are listed
        :return: The function `olx_parser` returns a list of lists containing information about
        chosen apartments.
    """
    chosen_apartments: list = []
    page_count: int = get_pages_count(apartments_url)

    for page in range(1, page_count + 1):
        url: str = get_page_url(apartments_url, page)
        apartments: list = get_apartment_cells(url)

        for apartment in apartments:
            precondition: bool = get_precondition(apartment)

            if precondition:
                apartment_link: str = get_apartment_link(apartment)

                if apartment_link:
                    apartment_data: list = get_single_apartment(apartment_link)

                    if apartment_data:
                        paragraphs: list = apartment_data[0].find_all('p', {'class': 'css-b5m1rv er34gjf0'})
                        paragraphs_list: list = [paragraph.text for paragraph in paragraphs]

                        if paragraphs_list:

                            ad_type: str = paragraphs_list[0]
                            floor: int | None = get_floor(paragraphs_list)
                            building_type: str = get_building_type(paragraphs_list)
                            room_count: int = get_room_count(paragraphs_list)
                            full_price: float = get_full_price(apartment, paragraphs_list)
                            info: str = get_apartment_info(apartment, apartment_data)

                            ad_type_condition: bool = ad_type in AD_TYPES
                            floor_condition: bool = MIN_FLOOR <= floor <= MAX_FLOOR if floor else False
                            building_type_condition: bool = building_type in BUILDING_TYPES
                            room_count_condition: bool = MIN_ROOM_COUNT <= room_count <= MAX_ROOM_COUNT
                            price_rent_condition: bool = MIN_PRICE <= full_price <= MAX_PRICE
                            heating_condition: bool = any(pattern in info for pattern in DISTRICT_HEATING)

                            # change if preferences changed
                            condition: bool = floor_condition and building_type_condition and \
                                              room_count_condition and price_rent_condition and heating_condition

                            if condition:
                                apartment_info: list = [
                                    apartment_link,
                                    get_location(apartment),
                                    full_price,
                                    get_area(apartment),
                                    building_type,
                                    floor,
                                    room_count,
                                    info,
                                ]
                                chosen_apartments.append(apartment_info)

    apartment_presentation(chosen_apartments)
    return chosen_apartments


if __name__ == '__main__':
    olx_parser(APARTMENTS_URL_FILTERED)
