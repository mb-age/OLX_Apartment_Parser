# OLX Apartment Scraper

This Python script scrapes apartment listings from OLX, filters them based on specified criteria, and presents the chosen apartments.

## Prerequisites

- Python 3.11
- Required Python packages: `requests`, `beautifulsoup4` (you can install them using `pip install requests beautifulsoup4`)

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/mb-age/OLX_Apartment_Parser.git
    cd olx_parser
    ```

2. Run the script:

    ```bash
    python main.py
    ```

   Make sure to adjust the script parameters such as `CITY`, `MIN_PRICE`, `MAX_PRICE`, `MIN_AREA`, `MAX_AREA`, etc., based on your preferences.

## Script Overview

- **`main.py`**: The main script that contains the OLX scraper logic.

### Functions:

- **`get_pages_count(url)`**: Function to get the total number of pages for a given URL.
- **`get_page_url(url, page)`**: Function to get the URL for a specific page.

### Scraping Functions:

- **`get_apartment_cells(url)`**: Function to get a list of apartment cells from a given URL.
- **`get_single_apartment(url)`**: Function to get information about a single apartment from a given URL.

### Filtering Functions:

- **`get_precondition(apartment)`**: Function to check if an apartment meets specified conditions based on price, location, and area.
- **`get_floor(paragraphs_list)`**: Function to extract the floor number mentioned in the paragraphs.
- **`get_building_type(paragraphs_list)`**: Function to extract the building type mentioned in the paragraphs.
- **`get_room_count(paragraphs_list)`**: Function to extract the number of rooms mentioned in the paragraphs.
- **`get_full_price(apartment, paragraphs_list)`**: Function to calculate the full price of an apartment by adding price and rent.

### Presentation Functions:

- **`apartment_presentation(chosen_apartments)`**: Function to print information about each chosen apartment.

### Execution:

- **`olx_parser(apartments_url)`**: Function to parse apartment listings from a given URL and filter them based on specified criteria, returning a list of chosen apartments.

## Customization

Feel free to customize the script by adjusting the parameters, such as filtering conditions, locations, ad types, building types, etc., according to your preferences.
