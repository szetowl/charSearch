import codecs

from flask import Blueprint, render_template, request
from .books import books, removeSpecialChar, getPageNo
views = Blueprint('views', __name__)

@views.route('/', methods=('GET','POST'))
def search():
    return render_template('home.html',books=books)

@views.route('/result', methods=('GET','POST'))
def result():
    error_message = ''
    input_string = request.form.get('search_string')
    #input_string ="瀚海風烟掃易空，玉關歸路幾時東？塞垣可是秋寒早，一夜清霜滿鏡中。"
        #白骨縱橫似亂麻，幾年桑梓變龍沙。只知河朔生靈盡，破屋疏煙卻數家！
        #"長安回望繡成堆，山頂千門次第開。一騎紅塵妃子笑，無人知是荔枝來。"
        #"十載飄然繩檢外，樽前自獻自爲酬。秋山春雨閒吟處，倚遍江南寺寺樓。"
        #"大羅天上神仙客，濯錦江頭花柳春。不為碧雞稱使者，唯令白鶴報鄉人。"
        #"沉舟側畔千帆過，病樹前頭萬木春。"
        #獨在異鄉爲異客，每逢佳節倍思親。遙知兄弟登高處，遍插茱萸少一人
        #"腰間寶劍七星文，臂上雕弓百戰勳。見說雲中擒黠虜，始知天上有將軍。"
        #"與君相見即相親，聞道君家在孟津。爲見行舟試借問，客中時有洛陽人。"
        #"漢家君臣歡宴終，高議雲臺論戰功。天子臨軒賜侯印，將軍佩出明光宮。"
    books_selected = request.form.getlist('books')
    if not input_string or not books_selected:
        error_message='請輸入所需資料'
        print(error_message)
        return render_template('home.html', books=books, error_message=error_message)

    else:
        search_string = removeSpecialChar(input_string)
        search_result = {}
        for searchTxt in search_string:
            # Loop through each chinese char= searchTxt
            search_result[searchTxt] = "| "
            for book in books:
                # Loop through all the books
                for book_selected in books_selected:
                    if book['id']== int(book_selected) :
                        #Loop through all selected books
                        content = (book['content'])
                        book_title = book['title']
                        start_page = book['startingPage']
                        if start_page >0:
                            i = content.find(searchTxt)
                            if i >= 0:
                                char_in_page = book['chInPage']
                                search_result[searchTxt] += book_title + " P." + str(getPageNo(i + 1, start_page, char_in_page)) + " |  "
                        elif start_page==0:
                            search_result[searchTxt] += book_title
                            for pageContent in content:
                                if pageContent.find(searchTxt)>-1:
                                    search_result[searchTxt] += " P." + str(
                                        (content.index(pageContent)+1)) + "   "

        result_string=""
        print_string = ""
        for pair in search_result.items():
            result_string += pair[0] + " : " + pair[1]+"\n"
            if pair[1] != "| ":
                print_string +=pair[0] + " : " + pair[1]+"\n"

        # for HTML display result.txt
        f = codecs.open('resultTXT.txt', 'w', encoding='utf-8')
        f.write(result_string)
        f.close()

        # no blank line for printTXT.txt  used the file to print PDF
        g = codecs.open('printTXT.txt', 'w', encoding='utf-8')
        g.write(print_string)
        g.close()

        return render_template('result.html',search_result=search_result,search_string=search_string)
