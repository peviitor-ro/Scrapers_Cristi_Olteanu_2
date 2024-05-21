
**Description**

This project automates the scraping of job postings from various websites and submits them to the Peviitor.ro platform. It leverages Object-Oriented Programming (OOP) principles for code organization and maintainability.

**Advantages of Using OOP**

* **Modularity:** The code is divided into well-defined classes (`Scraper`, `UpdatePeViitor`, etc.), making it easier to understand, maintain, and extend.
* **Reusability:** The `Scraper` class serves as a blueprint for creating new scrapers for different websites, promoting code reuse.
* **Encapsulation:** Data and methods are encapsulated within classes, promoting data protection and reducing the risk of unintended side effects.

**Methods in `scrapers.py`**

* `get_soup(self, params=None)`: Fetches and parses HTML content using BeautifulSoup, handling optional request parameters.
* `get_link_soup(self, link)`: Fetches and parses HTML content from a specified link.
* `get_json_link(self, link)`: Fetches and returns JSON data from a link.
* `get_json(self, json=None, data=None, params=None)`: Makes a GET request with optional JSON data, request data, or URL parameters and returns the JSON response.
* `post_json(self, headers=None, json=None, data=None, params=None)`: Makes a POST request with optional headers, JSON data, request data, or URL parameters and returns the JSON response.
* `post_html(self, headers=None, data=None, params=None)`: Makes a POST request that returns parsed HTML content.
* `get_cookies(self, *args)`: Retrieves cookies from the website's response headers.
* `@staticmethod get_validated_city(city)`: Validates a city name against a predefined list of acceptable city names.
* `get_jobs_dict(self, job_title, job_link, city, remote='On-site')`: Creates a dictionary containing job details and appends it to the `jobs_list` attribute.
* `push_peviitor(self)`: Pushes scraped jobs and company logo (if available) to Peviitor.ro using the `UpdatePeViitor` class.

**Inheritance for Creating New Scrapers**

1. Create a new Python file in the `sites` directory following the naming convention `[website_name]_scraper.py`.
2. Import the `Scraper` class from `src.scrapers`.
3. Create a subclass of `Scraper` named after the website (e.g., `RwsScraper` for RWS).
4. Implement a `get_jobs(self)` method that extracts job postings using website-specific logic.
5. Call the base class constructor (`super().__init__(...)`) with company name, URL, and logo URL.
6. Call `get_jobs(self)` to extract jobs and `push_peviitor(self)` to submit them to Peviitor.ro.

**This how data looks on peviitor platform**

![image](https://github.com/peviitor-ro/Scrapers_Cristi_Olteanu_2/assets/142798921/382c579b-8db1-428b-89f2-6bcf9cc46809)

**Automated Daily Execution** 

Scheduled to run daily at 11:05 AM using GitHub Actions workflows (file: scrapers_runner.yml). This ensures job postings are updated regularly on Peviitor.ro.


**Installation**

1. Clone or download the project repository.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Configure your Peviitor.ro API access by updating the `Authorization` header in `update_peviitor.py` with your access token.

**Contributing**

We welcome contributions to this project! Here's how you can get involved:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make changes and write unit tests (if applicable).
4. Submit a pull request for review and merging.

**Potential Problems**

* Website structure changes might break scrapers. Regularly test against the live website.
* Peviitor.ro API may change. Monitor their updates and adapt accordingly.

**Possible Improvements**

* Implement error handling for network issues or API failures.
* Add logging for better debugging and monitoring.
* Enhance the scraping logic to handle a wider range of website structures.

