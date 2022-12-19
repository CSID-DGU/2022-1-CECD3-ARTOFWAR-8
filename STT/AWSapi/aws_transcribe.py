from urllib import request
from ast import literal_eval
import boto3
from botocore.config import Config
from analysis_text import analysisVIDText
from dotenv import load_dotenv
import os 

# load .env
load_dotenv()

bucket = os.environ.get('BUCKET_NAME')

def transcribe(vid_title):
    file_nm = vid_title

    # Config 설정
    vid_config = Config(
    	region_name = 'us-west-1',
        signature_version = 'v4',
        retries={
        	'max_attempts':5,
            'mode':'standard'
        	}
        )

    # Transcribe 실행
    transcribe =boto3.client('transcribe', config=vid_config)
    # s3에 업로드한 파일
    job_uri = 'http://{}.s3-website-us-west-1.amazonaws.com/{}'.format(bucket,file_nm)  # job의 파일 위치 링크 형식에 맞춤
    transcribe.start_transcription_job(
        TranscriptionJobName=file_nm,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='ko-KR',
        Settings={
            'ShowSpeakerLabels' : True, # 화자분리 기능 True or False
            'MaxSpeakerLabels' : 2 # 화자수
        }
    )

    # Transcribe job 작업이 끝나면 결과값 불러옴
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=file_nm)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            break

    save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

     # 웹서버 결과
    load = request.urlopen(save_json_uri)
    confirm = load.status
    rst = load.read().decode('utf-8')

    # 문자열을 딕셔너리로 변환
    transcribe_text = literal_eval(rst)['results']['transcripts'][0]['transcript']

    # 확인
    print(transcribe_text)

    # Job 삭제하기
    del_transcribe =boto3.client('transcribe', config=vid_config)
    res = del_transcribe.delete_transcription_job(
    TranscriptionJobName = file_nm
    )

    res['ResponseMetadata']['HTTPStatusCode'] == '200'
    return analysisVIDText(transcribe_text)
