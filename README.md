# BLH COMPANY - AI 기반 모빌리티 솔루션

BLH COMPANY는 AI와 모빌리티 기술을 융합하여 중고차 산업의 디지털 전환을 선도하는 혁신적인 벤처기업입니다.

## 🚀 주요 서비스

### 1. 온라인 경매 및 공매 운영
- 부산 기반 C2B 온라인 경매 플랫폼
- 공공기관 및 법인 차량 대상 공매 시스템
- AI 기반 자동차 시세 분석 프로그램

### 2. EV 진단 활성화 및 사전 고장 진단 플랫폼
- BLE 기반 OBD-II 진단기 활용
- 전기차 배터리 상태 실시간 측정
- AI 기반 고장 패턴 사전 예측

### 3. 빅데이터 기반 가격 산정 시스템
- 국토부, 조합, 보험사, 플랫폼 데이터 통합
- 회귀분석 및 GBM 알고리즘 활용
- 예측 오차율 ±2.5% 이내

### 4. 탁송 관재시스템 및 ERP
- GPS 기반 실시간 위치 추적
- 통합 회계 처리 시스템
- 업무 처리 속도 50% 개선

## 🛠 기술 스택

- **Backend**: Python 3.11, Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Containerization**: Docker
- **Deployment**: Nginx

## 📋 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/blh_homepage.git
cd blh_homepage
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
python app.py
```

### 5. Docker를 사용한 실행
```bash
docker-compose up -d
```

## 🌐 접속 정보

- **로컬 개발**: http://localhost:5000
- **Docker**: http://localhost:80

## 📁 프로젝트 구조

```
blh_homepage/
├── app.py                 # Flask 애플리케이션 메인 파일
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 이미지 설정
├── docker-compose.yml    # Docker Compose 설정
├── nginx.conf            # Nginx 설정
├── static/               # 정적 파일
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML 템플릿
│   ├── admin/
│   └── *.html
└── ssl/                  # SSL 인증서 (운영환경)
```

## 🎯 주요 기능

- **반응형 웹 디자인**: 모든 디바이스에서 최적화된 사용자 경험
- **모던 UI/UX**: Bootstrap 5와 커스텀 CSS를 활용한 세련된 디자인
- **관리자 시스템**: 공지사항 관리 기능
- **문의 시스템**: 고객 문의 접수 및 처리
- **SEO 최적화**: 검색 엔진 최적화된 구조

## 📞 연락처

- **회사명**: 주식회사 비엘에이치컴퍼니
- **대표자**: 홍독경, 정태영
- **주소**: 부산시 해운대 우동 1436 카이저빌 613호
- **이메일**: info@blhcompany.com
- **전화**: 051-123-4567

## 📄 라이선스

이 프로젝트는 BLH COMPANY의 소유입니다.

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면 이슈를 생성하거나 풀 리퀘스트를 보내주세요.

---

**BLH COMPANY** - AI 기반 모빌리티 솔루션으로 중고차 거래의 새로운 기준을 제시합니다.