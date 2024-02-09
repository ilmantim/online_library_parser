import argparse
import os
import json
import time
import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parser import check_for_redirect, parse_book_page, get_book_text_by_id, \
    get_book_html_by_id, download_txt, download_image
    

def main():
    base_directory = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(
        description='This program allows to download books from tululu.org.'
    )
    parser.add_argument('--start_page', type=int, default=1, help='Enter the id of the first page')
    parser.add_argument('--end_page', type=int, default=1, help='Enter the id of the last page')    
    parser.add_argument(
        '--dest_folder',
        help='Enter the directory for text, images, json to be stored in',
        default=base_directory,
        type=str
    )
    parser.add_argument('--skip_imgs', help='Skips images downloading',
                        default=False, action='store_true')
    parser.add_argument('--skip_txt', help='Skips txt downloading',
                        default=False, action='store_true')
            
    args = parser.parse_args()
    
    books_directory = os.path.join(args.dest_folder, "books")
    os.makedirs(books_directory, exist_ok=True)
    
    images_directory = os.path.join(args.dest_folder, "images")
    os.makedirs(images_directory, exist_ok=True)

    downloaded_books = []

    for page_num in range (args.start_page, args.end_page + 1):
        try:
            science_fiction_url = "https://tululu.org/l55/"
            science_fiction_url_by_pages = f'{science_fiction_url}{page_num}'
            response = requests.get(science_fiction_url_by_pages)
            check_for_redirect(response)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            selector = ".bookimage a"
            books = soup.select(selector)
    
            for book in books:
                try:

                    href = book['href']
                    book_id = re.findall(r'\d+', href)[0]

                    url = "https://tululu.org/"
        
                    book_text = get_book_text_by_id(url, book_id)
                    book_html = get_book_html_by_id(url, book_id)
                    book_url = f'{url}/b{book_id}/'
                    print (book_url)
        
                    book_properties = parse_book_page(book_html)
                    downloaded_books.append(book_properties)
                    book_filename = f"{book_id}.{book_properties['title']}"
        
                    book_cover_url = urljoin(book_url, book_properties['cover_tag'])
                    
                    if not args.skip_txt:
                        download_txt(book_text, book_filename, books_directory)

                    if not args.skip_imgs:
                        download_image(book_cover_url, images_directory)

                except requests.exceptions.HTTPError:
                    print(f'There is no Book {book_id} to download.\n')
        
                except requests.exceptions.ConnectionError:
                    print ('No connection...Another try in 5 sec')
                    time.sleep(5)
        
        except requests.exceptions.ConnectionError:
            print ('No connection...Another try in 5 sec')
            time.sleep(5)

    downloaded_books_path = os.path.join(args.dest_folder, "downloaded_books.json")
    with open(downloaded_books_path, "w", encoding='utf-8') as file:
        json.dump(downloaded_books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()