# Multi-Site Job Scraper with Scrapy

This JobScraper is designed to scrape job listings from multiple sites, including Seek, Indeed, and LinkedIn.

## Requirements

- Python 3.x
- Scrapy
- Other dependencies (listed in `requirements.txt`)

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:curaproject/job-scraper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd multi-site-scraper
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Adding Job Categories in google cloud function (Job_crawler)

To add a job category, simply append the existing job categories separated by commas in runtime envirement. Afterward, deploy the function to make the changes effective.

## Usage

To run the scraper and collect job listings from all three sites, execute the following command in local:

```bash
python main.py
```
