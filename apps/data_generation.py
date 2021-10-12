from wordcloud import WordCloud
import matplotlib.pyplot as plt
from time import gmtime, strftime
from openpyxl import Workbook
from io import BytesIO
from flask import make_response,send_file
import os


def generate_cloud_image(data):
    """

    :param data:
    :return:
    """
    print(' here ')
    print(data)

    wordcloud = WordCloud(width=800, height=400,
                          background_color='white',
                          min_font_size=10).generate(' '.join(data))

    plt.figure(figsize=(10, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    file_name = "tweets_cloud"+str(strftime("%Y-%m-%d_%H_%M_%S", gmtime()))+'.png'
    path = "{}{}".format("apps/templates/reports/", file_name)
    plt.savefig(path)
    return path



def generate_excel_file(data):
    """
    :param data:list
    :return path:string
    """
    output = BytesIO()
    book = Workbook()
    sheet = book.active
    sheet.append(["text", "entities", "trend words"])
    for each in data:
        sheet.append([str(each.get('text',' ')), str(each.get('entities')),str(each.get("words"))])
    file_name = "Tweets"+ str(strftime("%Y-%m-%d_%H_%M_%S", gmtime()))+ '.xlsx'
    path = "{}{}".format("apps/templates/excel/",file_name)
    book.save(output)
    output = make_response(output.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    output.headers["Content-type"] = "application/force-download"
    return output