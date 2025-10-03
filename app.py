from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
import hashlib

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'blh_company_secret_key_2025'  # 세션 관리를 위한 시크릿 키

# 정적 파일 라우트 추가
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# SEO 라우트
@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# 헬스체크 엔드포인트
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# 데이터베이스 초기화
def init_db():
    # Vercel 환경에서는 메모리 데이터베이스 사용
    db_path = ':memory:' if os.environ.get('VERCEL') else 'blh_company.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 회사 정보 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ceo TEXT NOT NULL,
            capital TEXT NOT NULL,
            address TEXT NOT NULL,
            business_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 서비스 문의 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            service_type TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 공지사항 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'BLH COMPANY',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_published BOOLEAN DEFAULT 1,
            view_count INTEGER DEFAULT 0,
            priority INTEGER DEFAULT 0
        )
    ''')
    
    # 관리자 계정 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # 회사 정보 삽입
    cursor.execute('''
        INSERT OR IGNORE INTO company_info 
        (name, ceo, capital, address, business_type) 
        VALUES (?, ?, ?, ?, ?)
    ''', (
        '주식회사 비엘에이치컴퍼니',
        '홍독경, 정태영',
        '1억원',
        '부산시 해운대 우동 1436 카이저빌 613호',
        '소프트웨어 개발 및 공급업, 데이터 서비스업, 자동차 관련 서비스업'
    ))
    
    # 샘플 공지사항 삽입
    sample_notices = [
        ('EV 진단 솔루션 2.0 출시', 
         '더욱 정확하고 빠른 전기차 진단을 위한 새로운 버전이 출시되었습니다.\n\n주요 개선사항:\n- 진단 정확도 99.5% 향상\n- 실시간 배터리 상태 모니터링\n- AI 기반 고장 예측 기능 강화\n- 사용자 인터페이스 개선\n\n자세한 내용은 고객센터로 문의해주세요.', 
         'BLH COMPANY', 1, 1),
        ('모빌리티 혁신상 수상', 
         'BLH COMPANY가 AI 기반 모빌리티 솔루션으로 2025 모빌리티 혁신상을 수상했습니다.\n\n수상 내용:\n- AI 기반 중고차 가격 산정 시스템\n- 전기차 진단 기술 혁신\n- 빅데이터 활용한 시장 분석\n- 투명하고 효율적인 거래 플랫폼\n\n앞으로도 더 나은 서비스로 고객 여러분께 다가가겠습니다.', 
         'BLH COMPANY', 1, 2),
        ('대형 딜러와 파트너십 체결', 
         '국내 주요 중고차 딜러와의 전략적 파트너십을 체결했습니다.\n\n파트너사:\n- 현대자동차 중고차 사업부\n- 기아자동차 중고차 사업부\n- SK엔카\n- 카마스터\n\n이번 파트너십을 통해 더욱 안정적이고 신뢰할 수 있는 서비스를 제공할 수 있게 되었습니다.', 
         'BLH COMPANY', 1, 0),
        ('서비스 점검 안내', 
         '더 나은 서비스를 위한 시스템 점검을 실시합니다.\n\n점검 일시: 2025년 10월 1일 (화) 02:00 ~ 06:00\n점검 내용: 서버 업그레이드 및 성능 최적화\n\n점검 시간 동안 서비스 이용이 제한될 수 있습니다.\n불편을 드려 죄송합니다.', 
         'BLH COMPANY', 1, 0)
    ]
    
    for notice in sample_notices:
        cursor.execute('''
            INSERT OR IGNORE INTO notices (title, content, author, is_published, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', notice)
    
    # 기본 관리자 계정 생성 (bhl / bhl1004)
    admin_password_hash = hashlib.sha256('bhl1004'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO admin_users (username, password_hash)
        VALUES (?, ?)
    ''', ('bhl', admin_password_hash))
    
    conn.commit()
    conn.close()

# 관리자 로그인 확인 함수
def check_admin_login():
    return 'admin_logged_in' in session and session['admin_logged_in']

# 관리자 로그인 데코레이터
# 데이터베이스 연결 헬퍼 함수
def get_db_connection():
    db_path = ':memory:' if os.environ.get('VERCEL') else 'blh_company.db'
    return sqlite3.connect(db_path)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not check_admin_login():
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# 한국어 라우트 정의
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/landing')
def landing_page():
    return render_template('landing.html')

# 영문 라우트 정의
@app.route('/en')
def index_en():
    return render_template('index_en.html')

@app.route('/en/services')
def services_en():
    return render_template('services_en.html')

@app.route('/en/about')
def about_en():
    return render_template('about_en.html')

@app.route('/en/investors')
def investors_en():
    return render_template('investors_en.html')

@app.route('/en/contact')
def contact_en():
    return render_template('contact_en.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/notices')
def notices():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 공지사항 목록 조회 (최신순)
    cursor.execute('''
        SELECT id, title, author, created_at, view_count, priority
        FROM notices 
        WHERE is_published = 1 
        ORDER BY priority DESC, created_at DESC
    ''')
    notices = cursor.fetchall()
    
    conn.close()
    return render_template('notices.html', notices=notices)

@app.route('/notices/<int:notice_id>')
def notice_detail(notice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 공지사항 상세 조회
    cursor.execute('''
        SELECT id, title, content, author, created_at, updated_at, view_count
        FROM notices 
        WHERE id = ? AND is_published = 1
    ''', (notice_id,))
    notice = cursor.fetchone()
    
    if notice:
        # 조회수 증가
        cursor.execute('''
            UPDATE notices 
            SET view_count = view_count + 1 
            WHERE id = ?
        ''', (notice_id,))
        conn.commit()
    
    conn.close()
    
    if notice:
        return render_template('notice_detail.html', notice=notice)
    else:
        return "공지사항을 찾을 수 없습니다.", 404

# 관리자 로그인 페이지
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM admin_users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        admin = cursor.fetchone()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            
            # 마지막 로그인 시간 업데이트
            cursor.execute('''
                UPDATE admin_users 
                SET last_login = CURRENT_TIMESTAMP 
                WHERE username = ?
            ''', (username,))
            conn.commit()
            
            flash('로그인 성공!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('아이디 또는 비밀번호가 잘못되었습니다.', 'error')
        
        conn.close()
    
    return render_template('admin/login.html')

# 관리자 로그아웃
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('admin_login'))

# 관리자 대시보드
@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 통계 정보 조회
    cursor.execute('SELECT COUNT(*) FROM notices')
    total_notices = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM notices WHERE is_published = 1')
    published_notices = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM inquiries')
    total_inquiries = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(view_count) FROM notices')
    total_views = cursor.fetchone()[0] or 0
    
    # 최근 공지사항 5개
    cursor.execute('''
        SELECT id, title, created_at, view_count, is_published
        FROM notices 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    recent_notices = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total_notices': total_notices,
        'published_notices': published_notices,
        'total_inquiries': total_inquiries,
        'total_views': total_views
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_notices=recent_notices)

@app.route('/admin/notices')
@admin_required
def admin_notices():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 모든 공지사항 조회 (관리자용)
    cursor.execute('''
        SELECT id, title, author, created_at, is_published, view_count, priority
        FROM notices 
        ORDER BY priority DESC, created_at DESC
    ''')
    notices = cursor.fetchall()
    
    conn.close()
    return render_template('admin/notices.html', notices=notices)

@app.route('/admin/notices/new', methods=['GET', 'POST'])
@admin_required
def new_notice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author', 'BLH COMPANY')
        is_published = 'is_published' in request.form
        priority = int(request.form.get('priority', 0))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notices (title, content, author, is_published, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, author, is_published, priority))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_notices'))
    
    return render_template('admin/new_notice.html')

@app.route('/admin/notices/<int:notice_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_notice(notice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form.get('author', 'BLH COMPANY')
        is_published = 'is_published' in request.form
        priority = int(request.form.get('priority', 0))
        
        cursor.execute('''
            UPDATE notices 
            SET title = ?, content = ?, author = ?, is_published = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, author, is_published, priority, notice_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_notices'))
    
    # 공지사항 조회
    cursor.execute('SELECT * FROM notices WHERE id = ?', (notice_id,))
    notice = cursor.fetchone()
    conn.close()
    
    if notice:
        return render_template('admin/edit_notice.html', notice=notice)
    else:
        return "공지사항을 찾을 수 없습니다.", 404

@app.route('/admin/notices/<int:notice_id>/delete', methods=['POST'])
@admin_required
def delete_notice(notice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM notices WHERE id = ?', (notice_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_notices'))

@app.route('/api/inquiry', methods=['POST'])
def submit_inquiry():
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO inquiries (name, email, phone, company, service_type, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data.get('phone', ''),
            data.get('company', ''),
            data['service_type'],
            data['message']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '문의가 성공적으로 전송되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'})

@app.route('/api/company-info')
def get_company_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM company_info LIMIT 1')
    info = cursor.fetchone()
    conn.close()
    
    if info:
        return jsonify({
            'name': info[1],
            'ceo': info[2],
            'capital': info[3],
            'address': info[4],
            'business_type': info[5]
        })
    return jsonify({'error': '회사 정보를 찾을 수 없습니다.'})

# Vercel 환경에서는 애플리케이션 로드 시 데이터베이스 초기화
if os.environ.get('VERCEL'):
    init_db()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
