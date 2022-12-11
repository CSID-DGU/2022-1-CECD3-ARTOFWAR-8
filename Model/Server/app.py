from flask import Flask ,request  
from flask_restx import Api 
from classVID import predictVid

app = Flask(__name__)  # Flask 객체 선언
api = Api(app)  # Flask 객체에 Api 객체 등록

#동영상 유해성 판별 api
@app.route('/classify',methods=['POST'])
def classify():
    video_title=request.form.get('title') #동영상 제목 추출
    image=request.form.get('image')

    result = predictVid(video_title,image) #해당 동영상 유해성 판별
    return result #유해성 결과 반환

@app.route('/',methods=['POST'])
def classify2():
    video_title=request.form['title'] #동영상 제목 추출
    return str(video_title) #유해성 결과 반환


if __name__=='__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except:
        print('error')
