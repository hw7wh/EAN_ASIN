# Product Information Scraper

## Description
This Python project takes an Excel file as input, which contains EAN (European Article Number) codes, and utilizes these codes to retrieve corresponding ASIN (Amazon Standard Identification Number) codes for multiple European markets : UK, Poland, Netherlands, Italy, France, Spain, Germany, Sweden, and Belgium, if they exist. Additionally, the scraper fetches the product name and prices from various online market stores. Users have the flexibility to receive the output either directly updated in the Excel file, or stored in a MongoDB database.

## Requirements
- Python 3.x
- Required Python libraries: `pandas`, `openpyxl`, `beautifulsoup4`, `requests`,`curl_cffi`
- MongoDB for storing results (optional)

You can describe the folder structure in your README file using a combination of text and code blocks to outline the purpose of each directory and file. Here’s how you might do it:

## Folder Structure
Below is the folder structure of the project, along with a brief description of each file and directory:

```
EAN_ASIN/
│   .gitignore               # Specifies files and directories Git should ignore
│   requirements.txt         # Lists the Python packages required for the project
│   README.md                # This file
│   main.py                  # The main script that runs the scraper
└───input_handlers/
│   │   __init__.py
│   │   excel_handler.py
│   │   csv_handler.py
└───input/
│   │   ean.xlsx        # Excel file containing EAN codes
└───output/
│   │   asin.xlsx        # Excel file containing ASIN codes
└───scraper/
│   │   __init__.py
│   └───website1/
│   │   │   __init__.py
│   │   │   scraper.py       # Scraper script for website1
│   └───website2/
│   │   │   __init__.py
│   │   │   scraper.py       # Scraper script for website2
│   └───...                 # Other website scrapers
└───api/
│   │   __init__.py
│   └───endpoint1/
│   │   │   __init__.py
│   │   │   client.py        # API client script for endpoint1
│   └───endpoint2/
│   │   │   __init__.py
│   │   │   client.py        # API client script for endpoint2
│   └───...                 # Other API clients
└───utils/
    │   __init__.py
    │   helpers.py           # Utility scripts or helper functions
```

- **input/**: This directory contains the Excel file(s) with EAN codes that will be processed by the scraper.
- **output/**: This directory contains the Excel file(s) with ASIN codes that will be generayed as output.
- **scraper/**: This directory contains subdirectories for each website that you are scraping. Each subdirectory has a `scraper.py` script with the scraping logic specific to that website.
- **api/**: This directory contains subdirectories for each API endpoint you are interacting with. Each subdirectory has a `client.py` script for making requests to that specific API endpoint.
- **utils/**: This directory contains utility scripts or helper functions that can be used across different parts of your project.
- **.gitignore**: This file tells Git which files or directories to ignore.
- **requirements.txt**: This file lists the Python packages required for the project.
- **main.py**: This is the main script that you run to start the scraper.
- **README.md**: This file, which provides documentation for the project.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/hw7wh/ean_asin.git
   cd ean_asin
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   MONGODB_URI="your-mongodb-uri"
   DB_NAME="your-db-name"
   COLLECTION_NAME="your-collection-name"
   ```

## Usage
1. Place your Excel file with EAN codes in the `input` directory. Make sure there is a column named "EAN" with the EAN codes.

2. Run the script:
   ```
   python main.py
   ```

3. The script will read the EAN codes, scrape the product information, and write the results back to the Excel file, adding new columns for product name, prices, and ASIN.

## Output
The output will be an updated Excel file with additional columns for:
- Product Name
- Price
- ASIN (if available)

## Contributing
If you would like to contribute to this project, please feel free to submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---