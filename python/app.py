#!/bin/bash
import requests 
from bs4 import BeautifulSoup
import argparse
import re
import sys

green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
reset = "\033[0m"
red = "\033[31m"

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception.RequestException as e: 
        print(f"Failed to fetch URL ({e})")
        sys.exit(1)
    
def get_proxies():
    try:
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        if response.status_code == 200:
            clean_list = response.text.split("\n")
            return [proxy.strip() for proxy in clean_list if proxy.split()]
    except requests.RequestException as e:
        print(f"Failed to get proxies ({e})")
        return []

def check_proxies(proxy_list, url):
    for proxy in proxy_list:
        proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(f"Proxy {proxy} is working")
                return proxy
        except requests.RequestException:
            print(f"{red}Proxy {proxy} failed{reset}")
    return None
            

def get_elements(url, tag, use_proxy=False, proxy=None):
    while use_proxy:
        try:
            proxies = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
            }
            response = requests.get(url, proxies=proxies, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.find_all(tag)
            return [element.text.strip() for element in elements]                
        except Exception as e:
            print(f"There was a problem :{e}")
            return None
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(tag)
        return [element.text.strip() for element in elements]
    except Exception.RequestException as e:
        print(f"An error occured: {e}")

def get_links(url, use_proxy=False, proxy=None):
    proxies = None
    if use_proxy and proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        html = str(soup)
        pattern = r'https://[^"]+'
        regex = re.compile(pattern)
        matches = re.findall(regex, html)

        print(f"{green}\n\n[!] LINKS FOUND:\n\n{reset}")
        for match in matches:
            print(f"{yellow}Link found: {blue}{match}{reset}")
        return matches
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
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
    parser.add_argument('-P', '--proxies', action='store_true', default=False, required=False, help='proxies')
    args = parser.parse_args()


    url = args.url
    check_url(url)
    
    proxy = None
    use_proxy = False
    if args.proxies:
        use_proxy = True
        proxy_list = get_proxies()
        proxy = check_proxies(proxy_list, url)
        if not proxy:
            cont = input("No available proxies, type 'c' to continue without proxies : ")
            if cont.lower() == "c":
                use_proxy = False
            else: 
                print("No proxies found, exiting...")
                sys.exit(1)           
       
        
    if args.all:
        args.title = args.subtitle = args.lists = args.paragraphs = args.link = True
    
    output_files = {}
    
    if args.title:
        titles = get_elements(url, 'h1', use_proxy=use_proxy, proxy=proxy)
        print(f"{green}\n\n[!] TITLES FOUND:\n\n{reset}")
        output_files['titles.txt'] = titles
        for title in titles:
            print(f"{yellow}Title: {blue}{title}{reset}")


    if args.subtitle:
        subtitles = get_elements(url, 'h2', use_proxy=use_proxy, proxy=proxy)
        print(f"{green}\n\n[!] SUBTITLES FOUND:\n\n{reset}")
        output_files['subtitles.txt'] = subtitles
        for sub in subtitles:
            print(f"{yellow}Subtitle: {blue}{sub}{reset}")

    if args.lists:
        lists = get_elements(url, 'li', use_proxy=use_proxy, proxy=proxy)
        print(f"{green}\n\n[!] LISTS FOUND:\n\n{reset}")
        output_files['lists.txt']= lists
        for l in lists:
            print(f"{yellow}List: {blue}{l}{reset}")

    if args.paragraphs:
        paragraphs = get_elements(url, 'p', use_proxy=use_proxy, proxy=proxy)
        print(f"{green}\n\n[!] PARAGRAPHS FOUND:\n\n{reset}")
        output_files['paragraphs.txt']= paragraphs
        for par in paragraphs:
            print(f"{yellow}Paragraph: {blue}{par}{reset}\n")
   

    if args.link:
        links = get_links(url)
        output_files['links.txt']= links


    for filename, content in output_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            for item in content:
                f.write(item + '\n')


    print(f"\n\n{green}[!] Output save to files")
        



if __name__ == "__main__":
    main()