import os
import time
import requests
import argparse
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, unquote, urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError()


def get_book_text_by_id(url, book_id):
    book_text_url = f"{url}txt.php"
    params = {
        "id": book_id
    }
    response = requests.get(book_text_url, params=params)
    check_for_redirect(response)
    response.raise_for_status()
    book_text = response.text
 
    return book_text


def get_book_html_by_id(url, book_id):
    book_url = f"{url}b{book_id}/"
    response = requests.get(book_url)
    check_for_redirect(response)
    response.raise_for_status()
    book_html = response.text
    
    return book_html


def parse_book_page(html):
    soup = BeautifulSoup(html, 'lxml')

    title_tag = soup.find('h1')
    title_text = title_tag.text
    title, author = title_text.split('::')
    title = title.strip()
    author = author.strip()

    cover_tag = soup.find(class_='bookimage').find('img')['src']

    genre_tags = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genre_tags]

    comment_tags = soup.find_all(class_='texts')
    comments = [text_tag.find(class_='black').text for text_tag in comment_tags]
    comments = '\n'.join(comments)
    
    return {
        'title': title,
        'author': author,
        'cover_tag': cover_tag,
        'genres': genres,
        'comments': comments
    }


def download_txt(book_text, filename, folder):
    filename = sanitize_filename(filename)
    book_filepath = os.path.join(folder, filename + '.txt')

    with open(book_filepath, "w", encoding="utf-8") as book:
        book.write(book_text)

    return book_filepath


def download_image(cover_url, folder):
    filename = urlsplit(cover_url).path.split("/")[-1]
    filename = unquote(filename)
    image_filepath = os.path.join(folder, filename + '.jpg')

    response = requests.get(cover_url)
    check_for_redirect(response)
    response.raise_for_status()

    with open(image_filepath, 'wb') as image:
        image.write(response.content)

    return image_filepath


def main():
    parser = argparse.ArgumentParser(description='Download books from tululu.org.')
    parser.add_argument('--start_id', type=int, default=1, help='Start book ID to download')
    parser.add_argument('--end_id', type=int, default=10, help='End book ID to download')
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    base_directory = os.path.dirname(os.path.abspath(__file__))
    
    books_directory = os.path.join(base_directory, "books")
    os.makedirs(books_directory, exist_ok=True)
    
    images_directory = os.path.join(base_directory, "images")
    os.makedirs(images_directory, exist_ok=True)
     
    
    for book_id in range(start_id, end_id + 1):
        try:
            url = "https://tululu.org/"
            
            book_text = get_book_text_by_id(url, book_id)
            book_html = get_book_html_by_id(url, book_id)

            book_properties = parse_book_page(book_html)
            book_filename = f"{book_id}.{book_properties['title']}"
            book_cover_url = urljoin(url, book_properties['cover_tag'])
            
            download_txt(book_text, book_filename, books_directory)
            download_image(book_cover_url, images_directory)
    
        except requests.exceptions.HTTPError:
            print(f'There is no Book {book_id} to download.\n')
        
        except requests.exceptions.ConnectionError:
            print ('No connection...Another try in 5 sec')
            time.sleep(5)


if __name__ == '__main__':
    main()