import requests 
from bs4 import BeautifulSoup
import argparse
import re
import sys




def check_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print(f"Failed to fetch URL ({response.status_code})")
        sys.exit(1)

def get_elements(url, tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(tag)
    return [element.text.strip() for element in elements]


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    html = str(soup)
    pattern = r'https://[^"]+'
    regex = re.compile(pattern)
    matches = re.findall(regex, html)
    print(f"{green}\n\n[!] LINKS FOUND:\n\n{reset}")
    for match in matches:
        print(f"{yellow}Link found: {blue}{match}{reset}")


    
def main():

    parser = argparse.ArgumentParser(
        description='some description yet to be made',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-u', '--url', type=str, required=True, help='target url')
    parser.add_argument('-T', '--title', action='store_true', default=False, required=False, help='titles')
    parser.add_argument('-s', '--subtitle',action='store_true', default=False, required=False, help='subtitles')
    parser.add_argument('-l', '--lists', action='store_true', required=False, help='Lists and their contents')
    parser.add_argument('-p', '--paragraphs', action='store_true', default=False, required=False, help='paragraph text')
    parser.add_argument('-A', '--all', action='store_true', default=False, required=False, help='all arguments')
    parser.add_argument('-L', '--link', action='store_true', default=False, required=False, help='links')
    args = parser.parse_args()
    url = args.url
    check_url(url)
    Green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    reset = "\033[0m"
    if args.all:
        args.title = args.subtitle = args.lists = args.paragraphs = args.link = True
    if args.title:
        titles = get_elements(url, 'h1')
        print(f"{Green}\n\n[!] TITLES FOUND:\n\n{reset}")
        for title in titles:
            print(f"{yellow}Title: {blue}{title}{reset}")
    if args.subtitle:
        subtitles = get_elements(url, 'h2')
        print("\n\n[!] SUBTITLES FOUND:\n\n")
        for sub in subtitles:
            print(f"Subtitle: {sub}")
    if args.lists:
        lists = get_elements(url, 'li')
        print(f"\n\n[!] LISTS FOUND:\n\n")
        for l in lists:
            print(f"List: {l}")

    if args.paragraphs:
        paragraphs = get_elements(url, 'p')
        print(f"\n\n[!] PARAGRAPHS FOUND:\n\n")
        for par in paragraphs:
            print(f" paragraph: {par}\n")

   


    if args.link:
        get_links(url)
        



if __name__ == "__main__":
    main()