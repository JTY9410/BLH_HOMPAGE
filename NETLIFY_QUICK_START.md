# ⚡ Netlify 빠른 배포 가이드

## 🚀 3분만에 배포하기

### ✅ 1단계: Netlify 접속 및 연동
```
1. https://netlify.com 방문
2. "Login with GitHub" 클릭
3. "New site from Git" 선택
4. "GitHub" 선택
5. "JTY9410/BLH_HOMPAGE" 저장소 선택
```

### ✅ 2단계: 빌드 설정
```
Build command: python3 generate_static.py
Publish directory: dist
```

### ✅ 3단계: 배포 시작
```
"Deploy site" 클릭 → 자동 빌드 시작
```

## 📋 모든 준비 완료!

### 🎯 준비된 파일들
- ✅ **netlify.toml**: 자동 배포 설정
- ✅ **generate_static.py**: HTML 변환 스크립트  
- ✅ **requirements-netlify.txt**: 빌드 패키지
- ✅ **dist/**: 정적 사이트 (테스트 완료)

### 🌐 예상 배포 결과
```
🌍 배포 URL: https://[random-name].netlify.app
또는 커스텀: https://blhcompany.netlify.app

📄 페이지들:
- / (메인 페이지)
- /landing (랜딩 페이지) 
- /services (서비스 소개)
- /about (회사 소개)
- /contact (문의하기)
- /notices (공지사항)
```

### ⚡ 빌드 시간
- **첫 배포**: 2-3분
- **재배포**: 30초-1분

## 🔧 고급 설정 (선택사항)

### 커스텀 도메인
```
Site settings → Domain management → Add custom domain
```

### 폼 제출 활성화
```html
<!-- contact.html 폼에 추가 -->
<form data-netlify="true" name="contact">
```

## 🎉 완료!
모든 설정이 완료되어 즉시 배포 가능한 상태입니다!
