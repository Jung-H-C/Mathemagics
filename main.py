import sys
import os
from google.cloud import vision

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTextEdit, QFileSystemModel, QTreeView
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QModelIndex
import cv2
import shutil


# Json Key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\XOTOURLLIFE\Desktop\json_key\mathemagics-425113-4c56defec84b.json'

# Google Cloud Vision API 클라이언트 설정
client = vision.ImageAnnotatorClient()

WatchedOpening = False

# class SplashScreen(QSplashScreen):
#     def __init__(self, gif_path):
#         # Create a QLabel with the QMovie as its content
#         splash_pix = QPixmap()
#         super().__init__(splash_pix)
#         self.movie = QMovie(gif_path)
#         self.setMovie(self.movie)
#         self.movie.start()

#     def setMovie(self, movie):
#         self.movie = movie
#         self.movie.setParent(self)
#         self.movie.frameChanged.connect(self.repaint)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         pixmap = self.movie.currentPixmap()
#         painter.drawPixmap(0, 0, pixmap)
    
class MathSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
   
    def initUI(self):
        self.setWindowTitle('Mathemagics')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('./mathemagics/source/mathemagics_icon.jpg'))
 
        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet('background-color: gray;')

        app_icon = QPixmap('./mathemagics/source/mathemagics_width_icon.png')
        self.icon_label.setAlignment(Qt.AlignCenter)
        app_icon = app_icon.scaledToHeight(100, Qt.SmoothTransformation)
        self.icon_label.setPixmap(app_icon)

        self.label = QLabel('미리 보기', self)
        self.label.setGeometry(150, 50, 500, 300)

        self.imageLabel = QLabel('이미지가 불러와지지 않았습니다.', self)
        self.imageLabel.setGeometry(150, 50, 500, 300)
        self.imageLabel.setFont(QFont('Helvetica', 12))
        self.imageLabel.setStyleSheet('color: black; background-color: yellow; padding: 30px; border: 4px solid black; border-radius: 4px;')

        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.label2 = QLabel('라이브러리', self)
        self.model =  QFileSystemModel()
        self.model.setRootPath('./mathemagics/source/saved')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('./mathemagics/source/saved'))
        self.tree.clicked.connect(self.onFileClicked)

        
        self.resultLabel = QTextEdit('Result: ', self)
        self.resultLabel.setReadOnly(True)
        self.resultLabel.setGeometry(150, 400, 100, 50)
        
        self.button = QPushButton('Load Image', self)
        self.button.setGeometry(150, 500, 100, 50)
        self.button.clicked.connect(self.loadImage)
        
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.resultLabel)
        self.layout.addWidget(self.button)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    
    # def RunAnimation(self, Gif_path, duration):
    #     self.movie = QMovie(Gif_path)
    #     self.movie.setScaledSize(QSize(800, 600))
    #     self.Frame.setMovie(self.movie)
    #     self.movie.start()

    #     timer = QTimer(self)
    #     timer.singleShot(duration, self.Frame.clear)

    def loadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.showImage(fileName)
            self.processImage(fileName)
            destination = './mathemagics/source/saved/' + os.path.basename(fileName)
            shutil.copy2(fileName, destination)
    
    def onFileClicked(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        # self.showImage(file_path)
        # self.processImage(file_path)

        if file_path.lower().endswith(('.jpg')):
            self.showImage(file_path)
            self.processImage(file_path)
    

    def showImage(self, fileName):
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(500, 300, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)

    def processImage(self, fileName):
        # OpenCV로 이미지 읽기
        image = cv2.imread(fileName)
        success, encoded_image = cv2.imencode('.jpg', image)
        if not success:
            raise Exception('Image encoding failed')    
        content = encoded_image.tobytes()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if response.error.message:
                raise Exception(f'{response.error.message}')

        result = (texts[0].description).replace('\n', '') if texts else ""
        answer = self.math_function(result)
        self.resultLabel.setText(f"Result: {answer}")
    
    def math_function(self, text):
        """Converts recognized text to LaTeX code."""
        refined_text = self.refine_text(text)
        try:
            answer = str(eval(refined_text))
        except Exception as e:
            answer = "제대로 된 수식을 입력해주세요."
        output = text + "\n" + answer
        return output
    
    def refine_text(self, text):
        """Refines the recognized text."""
        refined_text = text.replace(" ", "")
        refined_text = refined_text.replace("=", "")
        refined_text = refined_text.replace("x", "*")
        refined_text = refined_text.replace("X", "*")
        refined_text = refined_text.replace("−", "-")
        refined_text = refined_text.replace("÷", "/")
        return refined_text



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # opening = SplashScreen('./mathemagics/source/animation.gif')
    # opening.show()

    # def start_app():
    #     opening.close()
    #     main_window = MathSolverApp()
    #     main_window.show()

    # QTimer.singleShot(2000, start_app)
    ex = MathSolverApp()
    ex.show()
    sys.exit(app.exec_())

