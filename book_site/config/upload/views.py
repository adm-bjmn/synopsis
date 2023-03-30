from django.shortcuts import render
from .forms import upload_form
from .models import csv_file
import csv
import requests
from synopsis.models import Book, Genre
import lxml
from bs4 import BeautifulSoup
from django.contrib import messages
import pandas as pd
from django.conf import settings

# Create your views here.


# --- Unused function ---
def backup_via_csv(request):
    ''' backup by csv presents the user with the csv form in order 
    to allow a manual uplad of data via CSV.
    The file is saved to the csv model and the database can be updated
    using the information within. This method has been removed in lieu
     of the new automatic update_by_scrape function.
    '''
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


def upload_by_scrape(request):  # approx 25 minutes
    ''' Upload by scrape employs a webscraping algorithm that scrapes 
    the popular bok sellers website www.waterstones.com
    The function visits the landing page of 600 new releases and gather 
    the information needed for the Books model in the synopsis app. 
    The data base is updated automatically as part of this function 
    and a CSV file is generated in order to allow for future download
    of all book information for data analysis etc.
    '''
    if request.method == "POST":
        # a user agent must be supplied by the user.
        user_agent = request.POST['user_agent']
        # all books are deleted prior to populating the
        # database with new information.
        Book.objects.all().delete()
        # print(user_agent)
        # ============== LISTS ==============
        links_list = []
        book_list = []
        genre_list = []
        all_genres = []

        # ============== WEBSCRAPING FOR URLS ==============
        headers = {
            'User-Agent': user_agent}

        for page_number in range(0, 26):
            ''' scraper visits the new realases page and gathers urls for 600 new books.
            '''
            url = f'https://www.waterstones.com/campaign/new-books/sort/pub-date-desc/page/{page_number}'
            page = requests.get(url, headers=headers)
            print(page.status_code)
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
        print(len(links_list))

        # ============== WEBSCRAPING FOR BOOK INFO ==============
        for link in links_list:
            ''' for all the links in the previously populated links list the 
            scraper will visit the link to the books info page on 
            waterstones.com, strip the relevant information and create 
            a book info list. The list is then used to create a new book
            object by indexing the information from the book list. 
            in some cases the informatiuon must be cleaned before the 
            book object can be created in order to ensure that the information
            in the fields is uniform accross all book objects.
            '''
            url = link
            # url = links_list[14]
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
            book_info.append(genre)

            # == Link ==
            link = url
            # print(link)
            book_info.append(link)

            # == Image ==
            img = soup.find('img', {'itemprop': 'image'})['src']
            book_info.append(img)
            # print(img)
            print(book_info)
            book_list.append(book_info)

            # == ADD BOOK TO DATABASE ==
            # update genres
            all_genres = {}
            for obj in Genre.objects.all():
                all_genres[obj.genre] = obj.id

            book = Book.objects.create(
                title=book_info[0],
                author=book_info[1],
                publish_date=book_info[3],
                synopsis=book_info[2],
                purchase_link=book_info[5],
                img_link=book_info[6],)
            book.genre.set(
                [all_genres.get(i) for i in book_info[4] if i in all_genres.keys()])
        print(all_genres)
        generate_csv(book_list)
        messages.success(request, ('The Database has been updated'))
        return render(request, 'synopsis/home.html', {})
    else:
        return render(request, 'upload/upload.html', {})


def generate_csv(book_list):
    ''' Generate CSV creates a csv file with all information from 
    the webscraper that has been used to create book objects. 
    The CSV file excludes the member related fields such as 
    liked_by and sen_by as theses are deemed irrelevant for 
    the purpose of this function.
    '''
    columns = ['title', 'author', 'publish_date',
               'synopsis', 'genre', 'purchase_link', 'img_link']
    date = datetime.now().date()
    df = pd.DataFrame(book_list, columns=columns)
    print(df.head())
    new_file = df.to_csv(f'{settings.MEDIA_ROOT}/{date}.csv',
                         encoding='utf-8', index=False)
    # add to csv models
    csv_file.objects.create(
        file_name=f'{date}.csv', file_processed=True)
    return None  # nothing to return.
