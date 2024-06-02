# Mathemagics

<p align="center">
  <img src="https://github.com/Jung-H-C/Mathemagics/assets/101037538/b9fc0156-1d7b-4609-b321-3d4b591b81ed.png" width="200" height="200"/>
  <br>
  chatgpt 4o의 도움을 받았습니다.
</p>

수학과 마술의 합성어 (Math + Magics)<br>
구글링을 해본 결과 이미 여러 곳에서 사용중인 네임이어서 슬펐지만 이 program이 그 취지에 가장 잘 맞게 사용된 사례라고 단언합니다.

# Idea?

최근들어 종이와 연필대신 아이패드와 애플펜슬을 가지고 공부를 하는 시대가 도래했습니다.
필기를 하는 용도에 있어서 편리한 인터페이스와 좋은 필기감을 가진 "태블릿"의 사용 빈도가 점차 늘고 있으며 확실히 편리한 기술이 많이 내장되어 있어 기존의 종이-연필 필기 방식보다 좋은 효율성을 보여줍니다.
하지만 이와중에도 한가지 연구가 뎌디다고 생각한 분야는 바로 "필체 인식 기술"입니다.

제가 개발한 "Mathemagics"는 시간의 효율을 중요시 생각하는 오늘 날, 누구나 귀찮아하는 계산기를 사용해야하는 수식을 AI가 인지하여 계산해주면 어떨까 하는 idea에서 착안했습니다.

유독 필체 인식을 응용한 기술은 연구가 느린것 같은데, 현재 개발된 기술가지고 충분히 상용화할 수 있지 않을까 하는 생각으로 프로그램을 제작해보게 되었습니다.

# Results
[![Video Label](https://github.com/Jung-H-C/Mathemagics/assets/101037538/228c4cb4-6639-494f-a70c-cbec3e0c5101)](https://www.youtube.com/watch?v=yZZM25ATnuE)
Click시 영상이 재생됩니다.

# Validation Data
![capture_01](https://github.com/Jung-H-C/Mathemagics/assets/101037538/f4e30346-b1d6-4c41-b4b9-a1b301bc6dc2) | ![capture_02](https://github.com/Jung-H-C/Mathemagics/assets/101037538/bacf7ae1-a882-4055-af02-061f30b16d85)
# Difficulties
이상과 달리 프로그래밍에 어려움을 겪는 저는 많은 것을 포기해야 했습니다.
원래 떠올린 "Tablet에서 바로 적용할 수 있는 필체 인식기술" 대신 Concept만 가지고 Windows Application으로 해당 Logic만 구현 하는 것으로 눈을 낮춰서 목표를 재설정했습니다.
가장 공들인 부분은 "미분 기호"를 인식하여 미분을 처리하는 모델을 만드는 것이었지만,
제가 사용한 Google의 Vision API는 수학 용어가 아닌 일반 text에만 중점이 맞춰져 있었고
이외에도 pytesseract 모듈이나 keras 모델을 다 시도해봤으나 실제 data로 했을 경우 필체 인식 성능이 좋지 않았습니다.

# 핵심 기술

![image](https://github.com/Jung-H-C/Mathemagics/assets/101037538/bcfe8037-a441-4cb0-afc3-802e684a9456)
우선 Google Cloud에서 제공하는 Vision API를 사용했습니다.

![image](https://github.com/Jung-H-C/Mathemagics/assets/101037538/6f917655-f635-4c38-a828-cb8ccd1826a3)
OpenCV로 파일을 읽어들어와 필체 인식 모델을 사용하여 필체 이미지를 text로 변환했습니다.

![image](https://github.com/Jung-H-C/Mathemagics/assets/101037538/9befe3c0-bd7b-4b84-a436-51a65f729252)
추출한 text를 수학 식으로 변환하기 위한 refine_text함수를 이와 같이 정의하고 python 내장 eval()함수를 통해 수식을 풀이하는 logic 구현

![image](https://github.com/Jung-H-C/Mathemagics/assets/101037538/88729ea2-bbf9-4b2b-a305-db347f029af7)
프로그램 안에 파일 탐색기 layout을 넣어 이전에 load한 사진을 저장해 손쉽게 불러올 수 있게끔 함.
