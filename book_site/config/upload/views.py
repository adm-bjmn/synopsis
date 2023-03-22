from django.shortcuts import render
from .forms import upload_form
from .models import csv_file
import csv
import requests
from synopsis.models import Book
import requests
import lxml
from bs4 import BeautifulSoup
from django.contrib import messages
# Create your views here.


# --- Unused function ---
def upload_by_csv(request):
    form = upload_form(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(
            request, ('Form successfully uoploaded'))
        form = upload_form()
        new_file = csv_file.objects.get(processed=False)
        # add in a try loop here for bad file uploads
        with open(new_file.file_name.path, 'r') as f:
            new_releases = csv.reader(f)
            for rows in new_releases:
                print(rows)
                # next step is to clean the input from the csv and make use
                # it is a well presented list ready for slcing
                # then the slices can be used to create a new book object.
                title = rows[1]
                author = rows[2]
                publish_date = rows[3]
                synopsis = rows[4]
                genre = rows[5]
                purchase_link = rows[6]
                img_link = rows[7]
                Book.objects.create(
                    title=title,
                    author=author,
                    publish_date=publish_date,
                    synopsis=synopsis,
                    genre=genre,
                    purchase_link=purchase_link,
                    img_link=img_link
                )
        # once the file has been processed the proceessed check box is marked automatically
        # to ensure the file is not picked up next time an upload is commited.
        new_file.processed = True
        new_file.save()
    return render(request, 'upload/upload.html', {'form': form, })
# --- ---


def upload_by_scrape(request):
    if request.method == "POST":
        user_agent = request.POST['user_agent']
        # print(user_agent)
        # ============== LISTS ==============
        links_list = []
        book_list = []
        genre_list = []
        all_genres = []

        # ============== WEBSCRAPING FOR URLS ==============
        # User agent must be supplied on page.
        headers = {
            'User-Agent': user_agent}

        for page_number in range(0, 2):
            url = f'https://www.waterstones.com/campaign/new-books/sort/pub-date-desc/page/{page_number}'
            page = requests.get(url, headers=headers)
            # print(page.status_code)
            soup = BeautifulSoup(page.text, 'lxml')
            # print(soup.title.text)
            books = soup.find_all('div', {
                'class': 'title-wrap'})
            # print(len(books))
            # print(type(books))
            for items in books:
                book_url = 'https://www.waterstones.com' + \
                    items.find(
                        'a', {'class': 'title link-invert dotdotdot'})['href']
                links_list.append(book_url)
        # print(links_list)
        # print(len(links_list))

        # ============== WEBSCRAPING FOR BOOK INFO ==============
        # for link in links_list:
        # url = link
        url = links_list[1]
        page = requests.get(url, headers=headers)
        # print(page.status_code)
        soup = BeautifulSoup(page.text, 'lxml')
        book_info = []
        print(soup.title.text)

        # == Title ==
        title = soup.find(
            'span', {'class': 'book-title'}).text
        book_info.append(title)
        # print(title)

        # == Author ==
        author = soup.find(
            'span', {'itemprop': 'author'}).text
        book_info.append(author)
        # print(author)

        # == Synopsis ==
        synopsis = soup.find(
            'div', {'id': 'scope_book_description'})
        unwanted = synopsis.find('strong')
        if unwanted:
            unwanted.extract()
        else:
            None
        # print(synopsis.text.strip())
        book_info.append(synopsis.text.strip().replace('\n', ' '))

        # == Publish Date ==
        publish_date = soup.find(
            'meta', {'itemprop': 'datePublished'})['content']
        book_info.append(publish_date)
        # print(publish_date)

        # == Genre ==
        genre = soup.find(
            'div', {'class': 'breadcrumbs span12'})
        unwanted = (genre.find('strong'))
        unwanted.extract()
        unwanted = (genre.find('br'))
        unwanted.extract()
        genre = genre.text.strip()
        remove_list = ['&', '\n', '>']
        for i in remove_list:
            genre = genre.replace(i, ',')
        genre = genre.split(',')
        genre = [items.strip().replace(' ', '').lower() for items in genre]
        genre_list.append(genre)
        # if 'travel' in genre:
        # print('oui madam')
        book_info.append(' '.join(genre))

        # == Link ==
        link = url
        # print(link)
        book_info.append(link)

        # == Image ==
        img = soup.find('img', {'itemprop': 'image'})['src']
        book_info.append(img)
        # print(img)
        '''
        Book.objects.create(
            title=book_info[0],
            author=book_info[1],
            synopsis=book_info[2],
            publish_date=book_info[3],
            genre=book_info[4],
            purchase_link=book_info[5],
            img_link=book_info[6],
        )
        '''
        messages.success(request, ('The Database has been updated'))
        return render(request, 'synopsis/home.html', {})
    else:
        return render(request, 'upload/upload.html', {})
