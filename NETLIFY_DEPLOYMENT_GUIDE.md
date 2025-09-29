# 🚀 Netlify 배포 가이드

## 📋 개요
BLH COMPANY 웹사이트를 Netlify를 통해 정적 사이트로 배포하는 완전한 가이드입니다.

## 🎯 준비 완료된 파일들

### 1. 핵심 배포 파일
- ✅ **netlify.toml**: Netlify 배포 설정 파일
- ✅ **generate_static.py**: Flask → 정적 HTML 변환 스크립트
- ✅ **requirements-netlify.txt**: Netlify 빌드용 최소 패키지

### 2. 자동 생성될 파일들
- **dist/**: 정적 사이트 빌드 결과물
- **_redirects**: Netlify 리다이렉트 규칙
- **robots.txt**: 검색엔진 크롤링 규칙
- **sitemap.xml**: 사이트맵

## 🔧 Netlify 배포 설정

### 방법 1: GitHub 연동 배포 (권장)

#### Step 1: Netlify 계정 생성
1. [Netlify.com](https://netlify.com) 방문
2. GitHub 계정으로 로그인

#### Step 2: 새 사이트 생성
1. "New site from Git" 클릭
2. "GitHub" 선택
3. `JTY9410/BLH_HOMPAGE` 저장소 선택

#### Step 3: 빌드 설정
```
Build command: python generate_static.py
Publish directory: dist
```

#### Step 4: 환경 변수 설정 (선택사항)
```
PYTHON_VERSION: 3.11
```

### 방법 2: 수동 배포

#### Step 1: 로컬에서 빌드
```bash
# 의존성 설치
pip install -r requirements-netlify.txt

# 정적 사이트 생성
python generate_static.py

# dist 폴더 확인
ls -la dist/
```

#### Step 2: Netlify 수동 배포
1. Netlify 대시보드에서 "Sites" 탭
2. "Deploy manually" 선택
3. `dist` 폴더를 드래그 앤 드롭

## 🌐 배포 후 설정

### 1. 커스텀 도메인 설정 (선택사항)
1. Site settings → Domain management
2. "Add custom domain" 클릭
3. 원하는 도메인 입력 (예: blhcompany.com)
4. DNS 설정 업데이트

### 2. HTTPS 설정
- Netlify에서 자동으로 Let's Encrypt SSL 인증서 제공
- "Force HTTPS" 옵션 활성화 권장

### 3. 폼 제출 설정 (문의하기 기능)
```html
<!-- contact.html에서 폼 설정 -->
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />
  <!-- 기존 폼 필드들 -->
</form>
```

## 📊 예상 배포 결과

### 배포 URL
```
https://[site-name].netlify.app
또는
https://[custom-domain].com
```

### 페이지 구조
```
https://yoursite.netlify.app/
├── / (index.html)
├── /landing (landing.html)
├── /services (services.html)
├── /about (about.html)
├── /contact (contact.html)
├── /notices (notices.html)
└── /static/ (CSS, JS, 이미지)
```

## 🔧 고급 설정

### 1. 빌드 훅 설정
- GitHub에 푸시할 때 자동 재배포
- Netlify에서 자동으로 감지 및 빌드

### 2. 성능 최적화
```toml
# netlify.toml에 이미 포함됨
[build.processing]
  skip_processing = false

# 캐싱 헤더 설정
[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000"
```

### 3. 보안 헤더
```toml
# netlify.toml에 이미 포함됨
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-XSS-Protection = "1; mode=block"
    # ... 기타 보안 헤더
```

## 🚨 주의사항

### 1. 동적 기능 제한
- Flask의 동적 기능은 정적 사이트에서 작동하지 않음
- 관리자 페이지는 정적 버전으로만 표시됨
- 실제 폼 제출은 Netlify Forms 기능 사용

### 2. 데이터베이스 기능
- SQLite 데이터는 정적 파일로 변환됨
- 실시간 데이터 업데이트 불가능
- 필요시 Headless CMS 연동 고려

### 3. 빌드 시간
- 초기 빌드: 1-3분
- 재배포: 30초-1분

## 🔄 배포 프로세스

### 자동 배포 (GitHub 연동)
```
1. 코드 변경 후 GitHub에 푸시
2. Netlify가 자동으로 감지
3. generate_static.py 실행
4. dist 폴더 빌드
5. 새 버전 자동 배포
```

### 수동 배포
```bash
# 1. 로컬 빌드
python generate_static.py

# 2. 빌드 확인
open dist/index.html

# 3. Netlify에 업로드
# (웹 인터페이스에서 dist 폴더 드래그 앤 드롭)
```

## ✅ 배포 체크리스트

- [ ] Netlify 계정 생성
- [ ] GitHub 저장소 연동
- [ ] 빌드 설정 구성
- [ ] 첫 배포 성공 확인
- [ ] 모든 페이지 접속 테스트
- [ ] 정적 파일 로딩 확인
- [ ] 모바일 반응형 테스트
- [ ] SEO 메타 태그 확인
- [ ] 성능 점수 측정
- [ ] 커스텀 도메인 설정 (선택)

## 📞 지원 및 문제 해결

### 빌드 실패 시
1. Netlify 빌드 로그 확인
2. requirements-netlify.txt 패키지 확인
3. generate_static.py 스크립트 테스트

### 페이지 로딩 실패 시
1. _redirects 파일 확인
2. netlify.toml 리다이렉트 규칙 확인
3. 정적 파일 경로 확인

---

## 🎉 완료!
모든 설정이 완료되면 BLH COMPANY 웹사이트가 Netlify에서 안정적으로 서비스됩니다.

**예상 배포 URL**: `https://blhcompany.netlify.app`
