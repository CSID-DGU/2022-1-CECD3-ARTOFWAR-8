from urllib import request
from ast import literal_eval
import boto3
from botocore.config import Config
from analysis_text import analysisVIDText

bucket = 'cecd3'   # cecd3 버킷에서 실행

def transcribe(vid_title):
    file_nm = vid_title

    # Transcribe를 위한 Config 설정
    vid_config = Config(
    	region_name = 'us-east-1',
        signature_version = 'v4',
        retries={
        	'max_attempts':5,
            'mode':'standard'
        	}
        )

    # Transcribe 실행
    transcribe =boto3.client('transcribe', config=vid_config)
    # s3에 저장된 동영상 파일 로드
    job_uri = 'https://{}.s3.amazonaws.com/{}.mp4'.format(bucket,file_nm)   # 생성된 job의 링크 형식에 맞춤
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
            json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            break

    json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

     # 웹서버 결과
    load = request.urlopen(save_json_uri)
    confirm = load.status
    rst = load.read().decode('utf-8')

    # 문자열을 딕셔너리
    transcribe_res = literal_eval(rst)['results']['transcripts'][0]['transcript']

    # 확인
    print(transcribe_res)

    # Job 삭제하기
    del_transcribe =boto3.client('transcribe', config=vid_config)
    restext = del_transcribe.delete_transcription_job(
    TranscriptionJobName = file_nm
    )

    restext['ResponseMetadata']['HTTPStatusCode'] == '200'
    return analysisVIDText(transcribe_res)


#임시로 직접 제목 입력
if __name__ == '__main__':
    transcribe("elder")
