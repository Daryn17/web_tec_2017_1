from bs4 import BeautifulSoup
import urllib.request
import psycopg2
import pprint

#--------------------------------------------------------------------------

author = ""
name = ""
price = 0
nWebsites = 0
bookbinding = ""
editorial = ""
language = ""
ISBN = 0
book = []

#---------------------------------------------------------------------------

def dropDB():
    conection = psycopg2.connect("dbname='webScraping' user='postgres' host='localhost' password='123'")
    objQuery = conection.cursor()
    objQuery.execute('DELETE FROM public."bookTable";')
    conection.commit()
    objQuery.close()
    conection.close()


def conectionDB(book):
    if book != []:
        print(book)
        price = book[2]
        price = price[:-1]
        price = int(float(price))
        nPages = book[3]
        nPages = nPages[:-6]
        nPages = int(nPages)
        conection = psycopg2.connect("dbname='webScraping' user='postgres' host='localhost' password='123'")
        objQuery = conection.cursor()
        objQuery.execute(
                'INSERT INTO public."bookTable"("Author", "Name", "Price", "nPages", "Bookbinding", "Editorial", "Language", "ISBN") VALUES(%s, %s, %s, %s, %s, %s, %s, %s);',
                (book[0], book[1], price, nPages, book[4], book[5], book[6], int(book[7])))

        objQuery.execute(
            'SELECT "Author", "Name", "Price", "nPages", "Bookbinding", "Editorial", "Language", "ISBN" FROM public."bookTable";')
        registro = objQuery.fetchall()
        #pprint.pprint(registro)
        conection.commit()
        objQuery.close()
        conection.close()

def cutText(cadena):
    canFin = 0
    cantCant = 0
    for i in cadena:
        cantCant += 1
        if canFin == 1:
            book.append(cadena[cantCant:])
            break
        elif i == ":":
            canFin += 1

#---------------------------------------------------------------------------





source = urllib.request.urlopen('https://www.casadellibro.com/libros').read()
soup = BeautifulSoup(source, 'html.parser')

bookSquares = soup.find_all('a', attrs={"class": "title-link"})
count = 0
for bookSquare in bookSquares:
    count += 1
    bookWebsite = "https://www.casadellibro.com" + bookSquare["href"]
    source = urllib.request.urlopen(bookWebsite).read()
    soup = BeautifulSoup(source, 'html.parser')
    name = soup.find('h1', attrs={"class": "book-header-2-title"})
    authorTemp = soup.find('h2', attrs={"class": "book-header-2-subtitle"})

    try:
        author = authorTemp.get_text().strip().split("\r")[0]
        book.append(author)
        book.append(name.get_text().strip())
    except:
        name = "Paso"

    if name != "Paso":
        price = soup.find('p', attrs={"class": "priceOriginal"})
        book.append(price.get_text().strip())

        bookInformation = soup.findChild('ul', attrs={"class": "list07"}).get_text()
        information = bookInformation.split("\n")
        cant = 1
        while cant < 6:
            cutText(information[cant])
            cant += 1
        print("---------------------------------------------------------------------")
    if count < 42:
        conectionDB(book)
    else:
        break
    book = []
print(str(count))