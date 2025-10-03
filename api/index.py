import os
import sys

# Vercel 환경 설정
os.environ['VERCEL'] = '1'

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Flask 앱 import
from app import app

# Vercel expects the WSGI application to be named 'app'
if __name__ == "__main__":
    app.run(debug=False)
