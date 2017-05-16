from bs4 import BeautifulSoup
import urllib.request
import psycopg2
import time

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


conection = psycopg2.connect(database="d8uqfr9b0s558k", user="almadmldqqdyxj", password="908fadd1cc02984877396b7cdf9593f83a484a43ba7563b852bfd80f3facd8f8", host="ec2-54-225-107-107.compute-1.amazonaws.com", port="5432")



def conectionDB(book):
    if book != []:
        print(book)
        price = book[2]
        price = price[:-1]
        price = int(float(price))
        nPages = book[3]
        nPages = nPages[:-6]
        nPages = int(nPages)
        conection = psycopg2.connect(database="d8uqfr9b0s558k", user="almadmldqqdyxj", password="908fadd1cc02984877396b7cdf9593f83a484a43ba7563b852bfd80f3facd8f8", host="ec2-54-225-107-107.compute-1.amazonaws.com", port="5432")
        objQuery = conection.cursor()
        objQuery.execute(
                'INSERT INTO bookTable (Author, Name, Price, nPages, Bookbinding, Editorial, Language, ISBN) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);',
                (book[0], book[1], price, nPages, book[4], book[5], book[6], book[7]))

        objQuery.execute(
            'SELECT Author, Name, Price, nPages, Bookbinding, Editorial, Language, ISBN FROM bookTable;')
        #registro = objQuery.fetchall()
        #print.pprint(registro)
        objQuery.execute(
            'INSERT INTO auditoria(ID, Date, PageID, Registros, Estado, Errores) VALUES(%s, %s, %s, %s, %s, %s);',
            (book[7], time.strftime("%d/%m/%y"),"www.casadellibro.com", count,"finalizado", "no"))

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

def crearTablas():
    cur = conection.cursor()

    cur.execute('''CREATE TABLE Auditoria
       (ID TEXT     NOT NULL,
        PageID TEXT NOT NULL,
        Date TEXT NOT NULL,
        Errores TEXT NOT NULL,
        Estado TEXT NOT NULL,
        Registros INT NOT NULL);''')

    cur.execute('''CREATE TABLE bookTable
       (Author TEXT NOT NULL,
        Name TEXT NOT NULL,
        Price INT NOT NULL, 
        nPages INT NOT NULL,
        Bookbinding TEXT NOT NULL,
        Editorial TEXT NOT NULL,
        Language TEXT NOT NULL,
        ISBN TEXT NOT NULL);''')
    print("Table created successfully")

    conection.commit()
    conection.close()


#---------------------------------------------------------



crearTablas()

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