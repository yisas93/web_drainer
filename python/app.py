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

def get_elements(url, tag, pattern=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(f"SOUP: {soup}")
    if pattern:
        elements = soup.find_all(tag, href=pattern)
    else:
        elements = soup.find_all(tag)
    return [element.text.strip() for element in elements]
    
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
    parser.add_argument('-a', '--a_tags', action='store_true', default=False, required=False, help='<a> tags')
    parser.add_argument('-A', '--all', action='store_true', default=False, required=False, help='all arguments')
    parser.add_argument('-L', '--link', action='store_true', default=False, required=False, help='links')
    args = parser.parse_args()
    url = args.url
    check_url(url)

    if args.all:
        args.title = args.subtitle = args.lists = args.paragraphs = args.a_tags = True
    if args.title:
        titles = get_elements(url, 'h1')
        print(f"[!] Titles:\n")
        for title in titles:
            print(title)
    if args.subtitle:
        subtitles = get_elements(url, 'h2')
        print("[!] Subtitles:\n")
        for sub in subtitles:
            print(sub)
    if args.lists:
        lists = get_elements(url, 'li')
        print(f"[!] Lists:\n")
        for l in lists:
            print(l)

    if args.paragraphs:
        paragraphs = get_elements(url, 'p')
        print(f"[!] Paragraphs:\n")
        for par in paragraphs:
            print(f" paragraph: {par}\n")

    if args.a_tags:
        a_tags = get_elements(url, 'a')
        print(f"[!] <a> Tags:\n")
        for a in a_tags:
            print(a)


    if args.link:
        pattern = re.compile("^https://")
        a = get_elements(url, "a", pattern)
        img = get_elements(url, "img", pattern)
        print("[!] All links are:")
        for elem in a:
            print(f"a tag link: {elem}")
        for elem in img:
            print(f"img link: {elem}")
        



if __name__ == "__main__":
    main()