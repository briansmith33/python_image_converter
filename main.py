from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QFormLayout, QBoxLayout, QWidget, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
import sys
import os


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.screen = app.desktop()
        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.widget = QWidget(self)
        self.widget.setLayout(self.mainLayout)
        self.setFixedWidth(500)
        self.setWindowIcon(QIcon(os.path.join(os.path.expanduser('~'), 'Pictures', 'icons', '1216670_128.ico')))
        self.setStyleSheet('background-color: #222222;')
        self.formLayout = QFormLayout()

        self.file = None
        self.format = "jpg"
        self.size = 128

        self.setWindowTitle("Image Converter")

        self.msg_label = QLabel('')
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.msg_label.setStyleSheet('font-weight: bold; padding: 20px; word-wrap: break-word; color: #bbbbbb; font-size: 16px;')
        self.msg_label.hide()

        choose_btn = QPushButton()
        choose_btn.setText("Choose Image")
        choose_btn.setCursor(QCursor(Qt.PointingHandCursor))
        choose_btn.setStyleSheet('padding: 10px; font-weight: bold; margin-bottom: 10px; color: #bbbbbb;')
        choose_btn.clicked.connect(self.dialog)

        self.ext_select = QComboBox()
        self.ext_select.setStyleSheet('padding: 10px; font-weight: bold; margin-bottom: 10px; background-color: #bbbbbb;')
        self.format_list = ["Format", "png", "gif", "jpg", "jpeg", "JPEG", "ico", "bmp", "tiff", "tif", "WebP"]
        self.ext_select.addItems(self.format_list)
        self.ext_select.currentIndexChanged.connect(self.format_change)

        self.size_select = QComboBox()
        self.size_select.setStyleSheet('padding: 10px; font-weight: bold; margin-bottom: 10px; background-color: #bbbbbb;')
        self.size_list = ["Size", "512", "256", "128", "64", "32"]
        self.size_select.addItems(self.size_list)
        self.size_select.currentIndexChanged.connect(self.size_change)

        convert_btn = QPushButton()
        convert_btn.setText("Convert")
        convert_btn.setCursor(QCursor(Qt.PointingHandCursor))
        convert_btn.setStyleSheet('padding: 10px; font-weight: bold; margin-bottom: 10px; color: #bbbbbb;')
        convert_btn.clicked.connect(self.convert)

        self.formLayout.addRow(self.msg_label)
        self.formLayout.addRow(choose_btn)
        self.formLayout.addRow(self.ext_select)
        self.formLayout.addRow(self.size_select)
        self.mainLayout.addLayout(self.formLayout)
        self.formLayout.addRow(convert_btn)

        self.setCentralWidget(self.widget)
        self.show()

    def dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "Choose Image", os.path.join(os.path.expanduser('~'), 'Pictures'), "All Files (*);;PNG Files  (*.png);;GIF Files (*.gif);;JPEG Files (*.jpg; *.jpeg; *.JPEG);;ICO Files (*.ico);;BMP Files (*.bmp);;TIF Files (*.tiff; *.tif);;WebP Files (*.WebP)")
        if check:
            self.file = file
            self.msg_label.setText(self.file)
            self.msg_label.show()

    def format_change(self):
        format_index = self.ext_select.currentIndex()
        self.format = self.format_list[format_index]

    def size_change(self):
        size_index = self.size_select.currentIndex()
        self.size = int(self.size_list[size_index])

    def convert(self):
        try:
            file_name = self.file.split('.')[0]
            img = Image.open(self.file)
            orig_width = img.size[0]
            orig_height = img.size[1]
            scale = self.size / orig_width
            width = self.size
            height = int(orig_height*scale)
            img.resize((width, height))
            need_to_convert = ["jpg", "jpeg", "JPEG"]
            if self.format in need_to_convert:
                img = img.convert('RGB')
            img.save(f'{file_name}_{self.size}.{self.format}')
            self.msg_label.setText('Image successfully converted!')
            self.msg_label.show()
        except Exception as e:
            print(e)
            self.msg_label.setText('Image failed to convert!')
            self.msg_label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())

