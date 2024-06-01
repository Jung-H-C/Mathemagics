import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import pytesseract
import sympy as sp
import cv2
from PIL import Image

# Tesseract 경로 설정 (필요시)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    
    def processImage(self, filePath):
        # OpenCV로 이미지 읽기
        image = cv2.imread(filePath)
        
        # 그레이스케일로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 임계값 처리
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # OCR로 텍스트 추출
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        self.resultLabel.setText(f'Recognized Text: {text}')
        
        # 수학 문제 풀이
        try:
            solution = sp.sympify(text)
            self.resultLabel.setText(f'Result: {solution}')
        except Exception as e:
            self.resultLabel.setText(f'Error: {str(e)}')
        
        # 이미지 표시
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(qImg))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathSolverApp()
    ex.show()
    sys.exit(app.exec_())

