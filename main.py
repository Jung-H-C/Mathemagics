import sys
import os
from google.cloud import vision

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sympy as sp
import cv2
from PIL import Image


# 환경 변수 설정 (다운로드한 JSON 키 파일의 경로를 입력해)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\XOTOURLLIFE\Desktop\json_key\mathemagics-425113-4c56defec84b.json'

# Google Cloud Vision API 클라이언트 설정
client = vision.ImageAnnotatorClient()


class MathSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Handwritten Math Solver')
        self.setGeometry(100, 100, 800, 600)
        
        self.label = QLabel(self)
        self.label.setGeometry(150, 50, 500, 300)
        
        self.resultLabel = QTextEdit('Result: ', self)
        self.resultLabel.setReadOnly(True)
        self.resultLabel.setGeometry(150, 400, 500, 50)
        
        self.button = QPushButton('Load Image', self)
        self.button.setGeometry(150, 500, 100, 50)
        self.button.clicked.connect(self.loadImage)
        
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.resultLabel)
        self.layout.addWidget(self.button)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def loadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.processImage(fileName)

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
        latex = self.convert_to_latex(result)
        self.resultLabel.setText(f"Result: {latex}")
    
    def convert_to_latex(self, text):
        """Converts recognized text to LaTeX code."""
        # 간단한 예제로서 변환 과정이 복잡할 수 있음
        # 여기서는 단순히 인식된 텍스트를 반환
        # 실제 구현에서는 수식을 인식하고 LaTeX으로 변환하는 로직이 필요
        return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathSolverApp()
    ex.show()
    sys.exit(app.exec_())
