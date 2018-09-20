import urllib
import urllib.request as urllib2 
import nyt_lib
import threading
import feedcontroller as fc
from queue import Queue
from PyQt5 import QtCore, QtWidgets, QtGui
from time import strftime

# -*- coding: utf-8 -*-
articles = fc.fill_feed_list() ### Gets our feed array, TODO: Turn this into queue to
                               ### use threading later.

threads_number = 8

articles_queue = Queue()
articles_with_image = Queue()

for arti in articles:
    articles_queue.put(arti)

class Main(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.section_map = nyt_lib.getAMap()
        self.screen_rect = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.screen_width = self.screen_rect.width()
        self.screen_height= self.screen_rect.height()
        #self.image_url = self.section_map["results"][0]["multimedia"][0]["url"]
        #print(self.image_url)
        #assert False, "Testing Image URL"
        
        self.initUI()
    def initUI(self):
        box_v = QtWidgets.QVBoxLayout() 
        main_layout = QtWidgets.QVBoxLayout() 
        self.setBackgroundRole(QtGui.QPalette.Light)
        self.setStyleSheet("color: white")
        news_box = QtWidgets.QGroupBox()
        scroll_area = QtWidgets.QScrollArea() 
        #scroll_area.setBackgroundRole(QtGui.QPalette.Dark)

        working_threads = []
        
        while not articles_queue.empty(): 
            arti = articles_queue.get()
            image_grabber = threading.Thread(target=self.get_image_thread, args=(arti, box_v))
            working_threads.append(image_grabber)
            image_grabber.start()
            #article_box.resize(self.screen_width)

        # Wait until all threads are done.
        for thread in working_threads:
            thread.join()
        # Note: Actually articles_with_image also contains articles WITHOUT images ...
        while not articles_with_image.empty():
            arti = articles_with_image.get()

            article_box = QtWidgets.QGroupBox()# Select the appropiate class hier
            article_layout = QtWidgets.QHBoxLayout() # article's internal Layout for
                                                        # the article_box (use setLayout)
            article_textpart = QtWidgets.QGroupBox() # Box for only the text part
            textpart_layout = QtWidgets.QVBoxLayout() 

            iml1 = QtWidgets.QLabel(self)
            pmap = QtGui.QPixmap()

            if arti.image_bytes:
                pmap.loadFromData(arti.image_bytes, "JPG")
                iml1.setPixmap(pmap)
                article_layout.addWidget(iml1)
            else:
                print("Image of {}, has no image url.".format(arti))
                iml1 = None
                pmap = None

            #Create article's text elements.
            article_title = QtWidgets.QLabel(arti.title)
            article_title.setStyleSheet("QLabel {color: black}")
            article_description = QtWidgets.QLabel(arti.description)
            article_url= QtWidgets.QLabel(arti.url)
            # Setup url display to be clickable and to behave like an hyperlink.
            article_url.setTextFormat(QtCore.Qt.RichText)
            article_url.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
            article_url.setOpenExternalLinks(True)

            textpart_layout.addWidget(article_title)
            textpart_layout.addWidget(article_description)
            textpart_layout.addWidget(article_url)

            article_textpart.setLayout(textpart_layout) # add layout to the texpart box
            #article_textpart.setBackgroundRole(QtGui.QPalette.Light)
            article_textpart.setStyleSheet("QGroupBox {background-color: blue}")
            article_layout.addWidget(article_textpart) # Add layout  to article layout to the right side of the image label.

            article_box.setLayout(article_layout)
            article_box.setStyleSheet("QGroupBox {background-color: brown}")

            box_v.addWidget(article_box)


            news_box.setLayout(box_v)
            scroll_area.setWidget(news_box)
            scroll_area.setWidgetResizable(True)
            main_layout.addWidget(scroll_area)
            self.setLayout(main_layout)
            #self.resize(pmap.width(),pmap.height())
    def get_image_thread(self, arti, box_v):
        
        if arti.image_url: ### Because some articles do not have images .
            ### Need to add some threading here to improve download speed here
            arti.image_bytes = get_response_bytes(arti.image_url)

        articles_with_image.put(arti)





#--------------Window settings------------------
        #self.showMaximized()
        self.setEnabled(True) # When True the Widget handles mouse and keyboard events
        self.setWindowTitle("News Feed")

#--------------Slots ---------------------------
    #Slot : Callback function for a given event


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

def get_response_bytes(url):
    headers = {}
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
    headers["User-Agent"] = user_agent
    opener = urllib2.build_opener()
    request = urllib2.Request(url, headers = headers)
    return opener.open(request).read() # Returns raw bytes

if __name__ == "__main__":
    main()



