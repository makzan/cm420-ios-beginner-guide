from lxml import html
from lxml import etree



css_content = open("output/reader.css").read()
js_content = open("reader.js").read()



# print( title )

# content = list(map( lambda x: x.decode_contents(formatter="html"), content_tree ))

book_setions = []

section_titles = ["Table of Content"]

files_to_read = open("book-sections.txt").read().split("\n")

for file_to_read in files_to_read:

    html_content = open("Manuscripts/%s.html" % file_to_read, encoding='utf-8').read()


    dom_tree = html.fromstring(html_content)

    title = dom_tree.xpath('//h1[@class="title"]/text()')[0]
    content_tree = dom_tree.xpath('//div[@class="formatted_content"]/div')

    section_titles.append(title);

    # content = "<section href='#' v-show='showing==\"%s\"'><h1>%s</h1>\n" % (title, title)
    content = "<book-section :showing='showing' title='%s'>" % title
    for node in content_tree:
        content += etree.tostring(node, pretty_print=True, encoding='unicode').replace("bc-attachment", "div").replace("<div/>","")
    content += "</book-section>"

    book_setions.append(content)



# table of content
toc_content = "<ol class='toc'>"
for title in section_titles:
    toc_content += "<li><a href='#' @click=\"showing='" + title + "'\">" + title + "</a></li>"
toc_content += "</ol>"

book_setions.insert(0, "<section v-show='showing==\"Table of Content\"'>%s</section>" % toc_content)

# print( book_setions )


output_content = "<!DOCTYPE html>\n<meta charset='utf-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1'>"
output_content += "<title>iOS App 開發入門</title>"
output_content += "<link rel='stylesheet' href='reader.css'>"
# output_content += "<style>" + css_content + "</style>\n"
output_content += "<div id='book'><header><h1>iOS App 開發入門</h1></header><div class='main-area'><main>\n<div class='section-content'>" + '\n'.join(book_setions) + "</div></main>" + toc_content + "</div></div><script src='https://unpkg.com/vue@2.5.17/dist/vue.js'></script><script>" + js_content + "</script>"

open("output/index.html", 'w').write(output_content)





