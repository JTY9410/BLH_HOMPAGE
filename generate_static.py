#!/usr/bin/env python3
"""
Netlify용 정적 사이트 생성기
Flask 애플리케이션을 정적 HTML 파일로 변환
"""

import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

def create_static_site():
    """Flask 템플릿을 정적 HTML로 변환"""
    
    # 출력 디렉토리 생성
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # static 파일 복사
    static_src = Path("static")
    static_dst = dist_dir / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dst)
    
    # Jinja2 환경 설정
    env = Environment(loader=FileSystemLoader('templates'))
    
    # 기본 컨텍스트 데이터
    context = {
        'url_for': lambda endpoint, **kwargs: get_static_url(endpoint, **kwargs),
        'request': type('Request', (), {'url': 'https://blhcompany.netlify.app'})()
    }
    
    # 페이지별 데이터
    pages = {
        'index.html': {
            'template': 'index.html',
            'context': {**context, 'title': 'BLH COMPANY - AI 기반 모빌리티 솔루션'}
        },
        'landing.html': {
            'template': 'landing.html', 
            'context': {**context, 'title': 'BLH COMPANY - Welcome'}
        },
        'services.html': {
            'template': 'services.html',
            'context': {**context, 'title': 'Services - BLH COMPANY'}
        },
        'about.html': {
            'template': 'about.html',
            'context': {**context, 'title': 'About - BLH COMPANY'}
        },
        'contact.html': {
            'template': 'contact.html',
            'context': {**context, 'title': 'Contact - BLH COMPANY'}
        },
        'notices.html': {
            'template': 'notices.html',
            'context': {
                **context, 
                'title': 'Notices - BLH COMPANY',
                'notices': get_sample_notices()
            }
        }
    }
    
    # HTML 파일 생성
    for output_file, page_data in pages.items():
        try:
            template = env.get_template(page_data['template'])
            html_content = template.render(**page_data['context'])
            
            output_path = dist_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Generated: {output_file}")
            
        except Exception as e:
            print(f"⚠️ Error generating {output_file}: {e}")
            # 기본 HTML 생성
            create_fallback_html(dist_dir / output_file, output_file)
    
    # 필수 파일들 확인 및 생성
    ensure_required_files(dist_dir)
    
    print(f"\n🎉 정적 사이트 생성 완료!")
    print(f"📁 Output directory: {dist_dir.absolute()}")
    print(f"🌐 Ready for Netlify deployment!")

def get_static_url(endpoint, **kwargs):
    """정적 파일 URL 생성"""
    if endpoint == 'static':
        filename = kwargs.get('filename', '')
        return f"/static/{filename}"
    return "#"

def get_sample_notices():
    """샘플 공지사항 데이터"""
    return [
        {
            'id': 1,
            'title': 'BLH COMPANY 웹사이트 리뉴얼 완료',
            'content': 'AI 기반 모빌리티 솔루션을 소개하는 새로운 웹사이트가 완성되었습니다.',
            'created_at': '2025-09-29',
            'author': 'BLH COMPANY'
        },
        {
            'id': 2,
            'title': 'EV 진단 서비스 출시',
            'content': 'BLE 기반 OBD-II 진단기를 활용한 전기차 배터리 진단 서비스가 시작됩니다.',
            'created_at': '2025-09-28',
            'author': 'BLH COMPANY'
        }
    ]

def create_fallback_html(file_path, filename):
    """기본 HTML 파일 생성"""
    title = filename.replace('.html', '').title()
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - BLH COMPANY</title>
    <link href="https://cdn.tailwindcss.com" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="min-h-screen flex items-center justify-center">
        <div class="text-center">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">BLH COMPANY</h1>
            <h2 class="text-2xl text-gray-600 mb-8">{title}</h2>
            <p class="text-gray-500 mb-8">AI 기반 모빌리티 솔루션</p>
            <a href="/" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                홈으로 돌아가기
            </a>
        </div>
    </div>
</body>
</html>"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 Created fallback: {filename}")

def ensure_required_files(dist_dir):
    """필수 파일들 확인 및 생성"""
    
    # _redirects 파일 생성 (Netlify용)
    redirects_content = """# Netlify redirects
/  /index.html  200
/landing  /landing.html  200
/services  /services.html  200
/about  /about.html  200
/contact  /contact.html  200
/notices  /notices.html  200
"""
    
    with open(dist_dir / "_redirects", 'w') as f:
        f.write(redirects_content)
    
    # robots.txt
    if not (dist_dir / "robots.txt").exists():
        robots_content = """User-agent: *
Allow: /

Sitemap: https://blhcompany.netlify.app/sitemap.xml
"""
        with open(dist_dir / "robots.txt", 'w') as f:
            f.write(robots_content)
    
    # sitemap.xml
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://blhcompany.netlify.app/</loc>
        <lastmod>2025-09-29</lastmod>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://blhcompany.netlify.app/landing</loc>
        <lastmod>2025-09-29</lastmod>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://blhcompany.netlify.app/services</loc>
        <lastmod>2025-09-29</lastmod>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://blhcompany.netlify.app/about</loc>
        <lastmod>2025-09-29</lastmod>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://blhcompany.netlify.app/contact</loc>
        <lastmod>2025-09-29</lastmod>
        <priority>0.7</priority>
    </url>
</urlset>"""
    
    with open(dist_dir / "sitemap.xml", 'w') as f:
        f.write(sitemap_content)
    
    print("✅ Required files created")

if __name__ == "__main__":
    create_static_site()
