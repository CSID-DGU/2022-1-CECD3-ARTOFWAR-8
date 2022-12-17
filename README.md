# 2022-1-CECD3-ARTOFWAR-8
동국대학교 컴퓨터공학종합설계, 손자병법팀
# 건강행동 촉진형 메타 노인복지관 창작물 관리 시스템
고령자 누구나 사용 가능한 비대면 24시간 복지관 서비스를 제공하는 어플리케이션의 창작물의 업로드 및 관리 시스템 \
메타 복지관 창작물 분류 및 키워드를 포함하는 창작물 업로드 시스템 + 메타 복지관에 업로드된 창작물을 관리 시스템
## 팀원 구성
컴퓨터공학과 2018112019 고가현 \
컴퓨터공학과 2018112045 이초록 \
컴퓨터공학과 2019111993 박지은 \
컴퓨터공학과 2019112005 진하빈
## 개발 환경 및 오픈소스 활용
- Python 3.7.13
- Tensorflow 2.8.2
- Keras 2.8.0 

## 시스템 구성도
![image](https://user-images.githubusercontent.com/62590665/206746998-5e0071bd-81a2-4007-bb74-070bac1a9047.png)
1) 사용자 페이지 
    1-1. 동영상 업로드: 동영상 업로드 요청이 들어오면 유해성 판단과 소개문을 작문
    - 업로드된 동영상의 유해 이미지 포함 여부 확인 
    - 업로드된 동영상의 음성을 텍스트로 변환 
    - 변환된 텍스트에서 유해 단어 포함 여부 확인 
    - 변환된 텍스트에서 주요단어 추출 및 주요단어를 통한 소개문 작문 
    1-2. 동영상 관리: 업로드한 동영상 관리 
    - 업로드된 동영상의 세부 정보를 수정 
    - 업로드된 동영상의 삭제 
    - 유해 동영상으로 판별된 경우 이에 대한 문의 작성 
    ![image](https://user-images.githubusercontent.com/45120083/208053261-9481ceaa-62c7-4825-b207-a6abdcadb064.png)
  
2) 관리자 페이지 : 사용자의 유해동영상에 대한 문의 내역 확인 및 동영상 관리 
    - 사용자가 작성한 문의 확인 및 답변 

      ![image](https://user-images.githubusercontent.com/45120083/208053230-7e3e143a-7e55-42e3-88cb-bada4f5b540e.png)

## 프로젝트 주요 기능
### 유해 이미지 판별 모델
<img src="https://user-images.githubusercontent.com/45120083/174441411-b8009f60-c5e6-4197-8c69-bee00ab5561b.png" width="770" height="310"/>
<img src="https://user-images.githubusercontent.com/45120083/174442306-d6cdc822-1c67-482c-b6c5-b4f3d0761a36.png" width="770"/>
<img src="https://user-images.githubusercontent.com/45120083/174441514-23a655d2-1c0a-46cb-a8d6-39ad297a285d.png" width="770" height="270"/>

### 백엔드
![image](https://user-images.githubusercontent.com/45120083/208053483-d43f3508-8f79-47ae-8944-6e3a1247a6f2.png)
- 개발환경: docker container
- 웹 서버: Nginx
- 웹 프레임워크: django 
- reddis: 동영상 요청이 들어왔을 경우 작업을 스케줄링
- celery: 비동기적으로 동영상을 이용한 서버 통신

### 주요 단어 추출 및 유해 단어 필터링   
#### AWS Transcribe API를 이용
- AWS Transcribe 시 config 설정 값
region_name = 'us-east-1',
signature_version = 'v4',
retries={
  	'max_attempts':5,
    'mode':'standard'
}

##### 성능 확인
![image](https://user-images.githubusercontent.com/80958412/208253378-a9b1d2be-4132-4994-8569-50f85e7457fd.png)
![image](https://user-images.githubusercontent.com/80958412/208253397-1d4481dc-2f7f-4c57-b916-389405124bc7.png)

#### 동영상 길이 및 크기별 비교
![image](https://user-images.githubusercontent.com/80958412/208253444-cbe02109-d139-4ac1-9055-d5368007a356.png)
다음의 통계에 따라 100MB 이하의 동영상 파일만으로 제한한다.


## 문의
고가현 gahyun0527@dgu.ac.kr \
이초록 dlchfhr1211@dgu.ac.kr \
박지은 5656jieun@dgu.ac.kr \
진하빈 2019112005@dgu.ac.kr
