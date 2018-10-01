from lxml import html
from lxml import etree
import tomd


css_content = open("output/reader.css").read()
js_content = open("reader.js").read()

header_content = open("header.html").read()
footer_content = open("footer.html").read()


book_summary = open("book-summary.txt").read()




# print( title )

# content = list(map( lambda x: x.decode_contents(formatter="html"), content_tree ))



book_setions = []

section_titles = ["Table of Content"]

files_to_read = open("book-sections.txt").read().split("\n")

# HTML eBook
for file_to_read in files_to_read:

    html_content = open("Manuscripts/%s.html" % file_to_read, encoding='utf-8').read()


    dom_tree = html.fromstring(html_content)

    title = dom_tree.xpath('//h1[@class="title"]/text()')[0]
    content_tree = dom_tree.xpath('//div[@class="formatted_content"]')

    section_titles.append(title);

    content = "<book-section title='%s' :showing='showing' :next='this.next' :prev='this.prev'>" % title
    # print(content_tree)
    for node in content_tree:
        # print(node)
        # print(etree.tostring(node, pretty_print=True, encoding='unicode'))
        content += etree.tostring(node, pretty_print=True, encoding='unicode').replace("bc-attachment", "div").replace("<div/>","").replace("src=", "data-src=").replace("./../../Attachments", "./images").replace("./../Attachments", "./images").replace("<pre>","<pre><code>").replace("</pre>","</code></pre>").replace(".PNG",".jpg").replace(".png",".jpg").replace(".jpeg",".jpg")
    content += "</book-section>"

    book_setions.append(content)

js_titles = "var titles=['" + "','".join(section_titles) + "'];"

# table of content
toc_content = "<ol class='toc'>"
for title in section_titles:
    toc_content += "<li><a href='#/" + title + "' @click=\"showing='" + title + "'\">" + title + "</a></li>"
toc_content += "</ol>"

book_setions.insert(0, "<section v-show='showing==\"Table of Content\"'>%s%s</section>" % (book_summary, toc_content) )


output_content = header_content + '\n'.join(book_setions) + "</div></main><aside id='toc' v-show='showing!=\"Table of Content\"'>" + toc_content + "</aside></div></div><script>" + js_titles + "</script>" + footer_content

open("output/index.html", 'w').write(output_content)



# Markdown
markdown_sections = []
markdown_sections.append("<section><h1>iOS App 開發入門</h1>%s</section>" % book_summary)
for file_to_read in files_to_read:

    html_content = open("Manuscripts/%s.html" % file_to_read, encoding='utf-8').read()


    dom_tree = html.fromstring(html_content)

    title = dom_tree.xpath('//h1[@class="title"]/text()')[0]
    content_tree = dom_tree.xpath('//div[@class="formatted_content"]')


    content = "<section><h1>%s</h1>" % title
    # print(content_tree)
    for node in content_tree:
        # print(node)
        # print(etree.tostring(node, pretty_print=True, encoding='unicode'))
        content += etree.tostring(node, pretty_print=True, encoding='unicode').replace("bc-attachment", "div").replace("<div/>","").replace("./../../Attachments", "images").replace("./../Attachments", "images").replace("<pre>","<pre><code>").replace("</pre>","</code></pre>").replace(".PNG",".jpg").replace(".png",".jpg").replace(".jpeg",".jpg")
    content += "</section>"

    markdown_sections.append(content)

output_content = '\n\n'.join(markdown_sections)

open("output/book-content.md", 'w').write(output_content)




