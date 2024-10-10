# Jumia Web Scraper with Python: Automate Product Data Extraction

Welcome to the Jumia Web Scraper! This Python script automates the extraction of product data from **Jumia**, a popular online shopping platform in Nigeria. It scrapes comprehensive product information, including details and images, enabling efficient data collection and analysis.

## 📌 Features

- **Automated Product Data Scraping**: Efficiently extract product names, brands, prices, specifications, key features, seller information, and URLs from the Jumia website.
- **Image Downloading**: Automatically saves product images locally for further analysis or display.
- **CSV Output**: Outputs the extracted data into CSV files, facilitating easy access and manipulation.
- **Handles Pagination**: Automatically navigates through multiple pages to capture all available products in the selected category.
- **Duplicate Removal**: Detects and removes duplicate records to ensure clean datasets.
- **User-Friendly**: Simple configuration and easy to run, making it accessible for beginners and experienced developers alike.

## 🚀 How It Works

The scraper navigates to the Jumia baby products page, extracts product details and images, and saves the data in a structured CSV format. It iterates through pages to ensure complete data collection.

### Key Steps:

1. **URL Collection**: The script collects product URLs from multiple pages of the Jumia baby products category.
2. **Product Information Extraction**: For each product URL, it scrapes essential details, including:
   - Product Name
   - Brand
   - Price (both raw and formatted)
   - Key Features
   - Specifications
   - Seller Information
3. **Image Downloading**: Downloads and saves product images to a specified directory for easy access.
4. **Data Storage**: The scraped data is saved as a CSV file, allowing for easy analysis and visualization.
5. **Duplicate Handling**: Ensures no duplicate records are present in the final output file.

## 🛠️ Requirements

Before running the script, ensure you have the following packages installed:

- **Python 3.x**
- **BeautifulSoup4**: For parsing HTML and XML documents.
- **lxml**: For processing XML and HTML efficiently.
- **pandas**: For data manipulation and analysis.
- **requests**: For sending HTTP requests and handling responses.

Install the required packages using pip:
```bash
pip install beautifulsoup4 lxml pandas requests
```

## 🏃 How to Run the Script

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ezee-Kits/Jumia-Web-Scraper.git
   cd Jumia-Web-Scraper
   ```

2. **Run the Python Script**:
   ```bash
   python jumia_scraper.py
   ```

3. **View Results**:  
   The scraped data will be saved as `ALL_URL.csv` in the specified directory, along with images in their respective folders.

## 📁 Output Structure

The output CSV file (`ALL_URL.csv`) contains the following fields:

| Column Name        | Description                                        |
|--------------------|----------------------------------------------------|
| NAME               | The product name.                                  |
| BRAND              | The brand of the product.                          |
| PRODUCT_PRICE      | The price of the product in numerical format.     |
| NAIRA_PRICE        | The formatted price in Naira (₦).                 |
| KEY_FEATURES       | A list of key features of the product.            |
| SPECIFICATION      | A list of specifications for the product.         |
| BAG_INFO           | Additional information about the product bag.      |
| SELLER_INFO        | A list of seller information.                      |
| PRODUCT_PIC_URLS   | A list of URLs for product images.                |

### Example Output

```csv
NAME,BRAND,PRODUCT_PRICE,NAIRA_PRICE,KEY_FEATURES,SPECIFICATION,BAG_INFO,SELLER_INFO,PRODUCT_PIC_URLS
"Baby Stroller","BrandX",20000,"₦20,000","Lightweight, Foldable","Color: Red, Weight: 5kg","Included: Rain Cover","Seller1, Seller2","https://example.com/image1.jpg"
```

## 🔧 Future Improvements

- **Expand to Other Categories**: Implement functionality to scrape data from additional categories on Jumia.
- **Error Handling**: Enhance error handling to manage network issues, site changes, and unexpected HTML structures more robustly.
- **Data Cleaning**: Implement advanced data cleaning techniques to improve the quality of the extracted data.
- **User Configuration**: Allow users to specify categories, page limits, and output formats as command-line arguments or configuration files.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or features, feel free to open an issue or submit a pull request. All feedback is appreciated!

## 📞 Support

If you encounter any issues or have questions regarding the scraper, please feel free to contact me via the GitHub repository or open an issue.

## 📚 Resources

- [Jumia Website](https://www.jumia.com.ng/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

Happy scraping!
