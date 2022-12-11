#settings.py 바탕 test_runner.py 로 테스트
#python manage.py test app --settings='app.settings_test' 
from app.settings import *

TEST_RUNNER = 'app.test_runner.TestRunner'