from celery import shared_task
from django.template import base
from core.models import Videoinfo,Userinfo
import time,json,os.path
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError
import datetime
import requests

#   유해 동영상 이미지 필터링
@shared_task
def classify_video(storage_key,image):
    try:
        # storage_key 데이터와 동영상 썸네일 이미지 유무 STT 서버 요청 전송
        if image==0:
            data = requests.post('http://172.31.11.209:5000/classify', data={'title':storage_key,'image':'None'}).json() # 동영상 썸네일 이미지 없음
        else:
            data = requests.post('http://172.31.11.209:5000/classify', data={'title':storage_key,'image':''}).json() # 동영상 썸네일 이미지 존재

        video = Videoinfo.objects.filter(storage_key=storage_key) # storage_key 데이터와 함께 STT 서버 요청 전송
        if image==0:
            video.update(image_ext="jpeg" )#동영상 썸네일 이미지 확장자 추가
        video.update(
            status= 0 if float(data['ratio']) <= 0.1 else 1, # 동영상 상태 저장 - 유해성 10% 이하:중립 / 이상: 유해
            status_detail=int(data['ratio']*100), # 유해성 비율 저장
            image=1,# 동영상 썸네일 이미지 생성 여부 저장
        )
        return True
    except response.raise_for_status():# 200 OK 코드가 아닌 경우 에러 발동
        return False

#   유해 동영상 음성 필터링 + 동영상 소개문 작성 + 주요 단어 키워드 저장
@shared_task
def analysis_video(storage_key):
    try:
        video = Videoinfo.objects.get(storage_key=storage_key) # storage_key 데이터와 함께 STT 서버 요청 전송
        if video.status==0: #유해 이미지 없음
            response = requests.post('http://44.196.228.195:5000/analysis', data={'title':storage_key}) # storage_key 데이터 STT 서버 요청 전송
            data=response.json() # json response일 경우 딕셔너리 타입으로 바로 변환

            video.status=data['harmful'] # 전달 받은 해당 동영상 상태 갱신
            if video.status==0:#중립 동영상일 경우만 소개문 작문
                # 동영상 카테고리에 따른 동영상 소개문 작문
                introduction=video.name+'에 대한 동영상입니다.\n'
                if video.subclass=="참여 유도":
                    introduction+="동영상을 보고 참여 해봐요.\n"
                if video.subclass=="정보 제공":
                    introduction+="같이 동영상을 보고 알아봐요.\n"
                
                for i in data['keywords']:
                    introduction+=" #"+str(i)
                video.introduction=introduction
                video.save()
            
            # 주요 단어 키워드 저장
            #dynamodb=boto3.resource('dynamodb') # AWS dynamodb 연결
            #table=dynamodb.Table('vid_keyword')
            #table.put_item(
                #Item={
                    #'vid_title':storage_key, # 동영상 storage_key
                    #'keyword':response['keywords']  # 동영상 주요 단어
                    #})
        return True
        
    except FileNotFoundError:
        return False
    except response.raise_for_status():# 200 OK 코드가 아닌 경우 에러 발동
        return False

#   s3 스토리지의 데이터 삭제
@shared_task
def delete_s3_video(storage_key):
    s3 = boto3.client('s3', aws_access_key_id=settings.ACCESS_KEY,  # AWS s3 스토리지 연결
                      aws_secret_access_key=settings.SECRET_KEY)
    try:        
        video = Videoinfo.objects.get(storage_key=storage_key)   # storage_key에 해당하는 동영상 데이터 DB에서 추출
        filename, fileExtension = os.path.splitext(storage_key) # 동영상 데이터 파일 이름과 파일 확장자 분리
        image_storage_key='image_'+filename+'.'+str(video.image_ext) #   해당 동영상 썸네일 이미지 storage_key 생성

        # s3 스트리지의 데이터 삭제
        s3.delete_object(Bucket=settings.BUCKET_NAME, Key=storage_key)  # 동영상 삭제
        s3.delete_object(Bucket=settings.BUCKET_NAME, Key=image_storage_key)    # 이미지 삭제

        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False
