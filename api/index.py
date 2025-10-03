import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from app import app
    
    # Vercel 환경 변수 설정
    os.environ['VERCEL'] = '1'
    
    # 데이터베이스 초기화 (Vercel 환경에서)
    if os.environ.get('VERCEL'):
        from app import init_db
        init_db()
    
except ImportError as e:
    print(f"Import error: {e}")
    # 기본 Flask 앱 생성 (fallback)
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "BLH COMPANY - Server Error"

# Vercel expects the WSGI application to be named 'app'
if __name__ == "__main__":
    app.run(debug=False)
