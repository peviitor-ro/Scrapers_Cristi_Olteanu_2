import os
import subprocess

path = os.path.dirname(os.path.abspath(__file__))

exclude = [
    '_main.py',
    '__init__.py',
    'county.py',
    'scrapers.py',
    'update_peviitor.py',
    'validate_city.py',
    'timken_scraper.py'
]

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)