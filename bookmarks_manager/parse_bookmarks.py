import sys
import json
import html
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
# Function to parse and categorize bookmarks


def parse_and_categorize_bookmarks():
    with open('./YOUR_BOOKMARKS_HTML_FILE', 'r', encoding='utf-8') as file:
        bookmarks_html = file.read()

    soup = BeautifulSoup(bookmarks_html, 'html.parser')
    bookmarks = []

    for bookmark in soup.find_all('a'):
        title = html.unescape(bookmark.text)
        url = bookmark.get('href')
        bookmarks.append({'title': title, 'url': url})

    # Categorization logic
        categories = {
            'Education': ['education', 'learn', 'course', 'courses', 'tutorial', 'resource', 'how to', 'guide', 'guides', 'documentation', 'docs', 'documentation', 'manual', 'manuals', 'textbook', 'textbooks', 'ebook', 'ebooks', 'research', 'research paper', 'research papers', 'paper', 'papers', 'study', 'studies', 'study guide', 'study guides', 'study material', 'study materials', 'study resources', 'study resource', 'study materials', 'study material', 'study resources', 'study resource', 'study notes', 'study note', 'study aids', 'study aid', 'study tools', 'study tool', 'study websites', 'study website', 'study apps', 'study app', 'study software', 'study program', 'udemy', 'lynda', 'freecodecamp', 'odin', 'online learning', 'knowledge'],
            'Inspiration': ['inspiration', 'css', 'awwwards', 'design inspiration', 'creative', 'artistic'],
            'Music': ['music', 'songs', 'albums', 'artists', 'bands', 'genres', 'lyrics', 'concerts', 'playlist', 'music streaming', 'music production', 'music theory'],
            'Movies': ['movies', 'action', 'comedy', 'drama', 'film', 'cinema', 'movie reviews', 'movie recommendations'],
            'Anime': ['anime', 'manga', 'otaku', 'anime series', 'anime movies', 'anime recommendations'],
            'Technology': ['technology', 'programming', 'coding', 'software', 'development', 'web development', 'data science', 'machine learning', 'artificial intelligence', 'tech news', 'tech tutorials', 'tech reviews'],
            'Food': ['food', 'recipes', 'cooking', 'restaurant', 'cuisine', 'baking', 'cooking', 'recipes', 'baking', 'cooking tips', 'culinary', 'food blogs', 'food videos', 'food photography'],
            'Art': ['art', 'painting', 'drawing', 'photography', 'sculpture', 'design', 'art history', 'art techniques', 'art galleries'],
            'Science': ['science', 'biology', 'chemistry', 'physics', 'astronomy', 'geology', 'scientific research', 'scientific discoveries'],
            'DIY': ['diy', 'do it yourself', 'crafts', 'home improvement', 'handmade', 'diy projects', 'diy tutorials'],
            'Gaming': ['gaming', 'video games', 'game development', 'esports', 'game reviews', 'game streaming', 'gameplay videos'],
            'Books': ['books', 'reading', 'literature', 'novels', 'book recommendations', 'book reviews', 'book clubs'],
            'Coding': ['coding', 'programming', 'web development', 'software development', 'coding tutorials', 'coding challenges', 'coding communities'],
            'Design': ['design', 'graphic design', 'web design', 'user interface', 'design inspiration', 'design tools', 'design resources'],
            'Cybersecurity': ['cybersecurity', 'network security', 'information security', 'cyber threats', 'cyber defense', 'cybersecurity news'],
            'Psychology': ['psychology', 'mental health', 'behavioral science', 'cognitive psychology', 'psychological research', 'psychological studies'],
            'Uncategorized': []
        }

    categorized_bookmarks = {category: [] for category in categories.keys()}
    for bookmark in bookmarks:
        added = False
        title_words = set(bookmark['title'].lower().split())
        url_words = set(bookmark['url'].lower().split('/'))
        all_words = title_words.union(url_words)
        for category, keywords in categories.items():
            if any(keyword.lower() in all_words for keyword in keywords):
                categorized_bookmarks[category].append(bookmark)
                added = True
                break
        if not added:
            categorized_bookmarks['Uncategorized'].append(bookmark)

    return categorized_bookmarks
    cleaned_bookmarks = {}
    for category, bookmarks in categorized_bookmarks.items():
        unique_bookmarks = []
        bookmark_urls = set()
        for bookmark in bookmarks:
            url = bookmark['url']
            if url not in bookmark_urls:
                unique_bookmarks.append(bookmark)
                bookmark_urls.add(url)
        cleaned_bookmarks[category] = unique_bookmarks

    return cleaned_bookmarks

# Draggable QListWidget class


style_sheet = """
QListWidget {
    border: 1px solid gray;
    border-radius: 5px;
    background-color: white;
    font-size: 24px;
    color: #333;
}
QListWidget::item {
    padding: 5px;
    border-radius: 3px;
}
QListWidget::item:selected {
    background-color: #E0E0E0;
}
"""


class DraggableListWidget(QListWidget):
    def __init__(self, category, app, parent=None):
        super().__init__(parent)
        self.category = category
        self.app = app
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setStyleSheet(style_sheet)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = [url.toString() for url in event.mimeData().urls()]
        for url in urls:
            bookmark = {
                'title': '',
                'url': url
            }
            item = QListWidgetItem(url)
            item.setData(1000, url)
            self.addItem(item)
        event.accept()
        pass

# Main PyQt5 application class


class BookmarkApp(QMainWindow):
    def __init__(self, categorized_bookmarks):
        super().__init__()
        self.setWindowTitle('Bookmark Organizer')
        self.setGeometry(300, 300, 700, 500)
        self.categorized_bookmarks = categorized_bookmarks
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        # Horizontal layout for category buttons
        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        # Bookmark list is initially empty
        self.bookmarkList = QListWidget()

        # Create a button for each category and add it to the buttonLayout
        for category in self.categorized_bookmarks.keys():
            btn = QPushButton(category)
            btn.clicked.connect(
                lambda checked, category=category: self.displayBookmarksForCategory(category))
            buttonLayout.addWidget(btn)

        # Add the bookmark list to the main layout
        mainLayout.addWidget(self.bookmarkList)

        # Create a central widget, set the layout, and set it as the central widget
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def displayBookmarksForCategory(self, category):
        # Clear the current list
        self.bookmarkList.clear()

        # Add bookmarks from the selected category to the list
        for bookmark in self.categorized_bookmarks[category]:
            item = QListWidgetItem(bookmark['title'])
            item.setData(1000, bookmark['url'])
            self.bookmarkList.addItem(item)

    def save_bookmarks(self):
        with open('categorized_bookmarks.json', 'w', encoding='utf-8') as f:
            json.dump(self.categorized_bookmarks, f,
                      ensure_ascii=False, indent=4)


def main():
    categorized_bookmarks = parse_and_categorize_bookmarks()
    app = QApplication(sys.argv)
    ex = BookmarkApp(categorized_bookmarks)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
