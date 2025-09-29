# BLH COMPANY Docker 배포 가이드

## 🚀 성공적으로 Docker로 컨테이너화 완료!

### 현재 실행 중인 서비스
- **웹 애플리케이션**: http://localhost:8000
- **Nginx 프록시**: http://localhost:80
- **Redis 캐시**: localhost:6379

### 서비스 상태 확인
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs web
docker-compose logs nginx
docker-compose logs redis

# 헬스체크
curl http://localhost:8000/health
curl http://localhost:8000/
```

## Docker Hub 업로드 방법

### 1. Docker Hub에 로그인
```bash
docker login
```

### 2. 이미지 태그 변경
```bash
# 기존 이미지를 Docker Hub 레포지토리로 태그
docker tag blh-company:latest YOUR_DOCKERHUB_USERNAME/blh-company:latest
docker tag blh-company:latest YOUR_DOCKERHUB_USERNAME/blh-company:v1.0.0
```

### 3. Docker Hub에 업로드
```bash
# latest 태그 업로드
docker push YOUR_DOCKERHUB_USERNAME/blh-company:latest

# 버전 태그 업로드
docker push YOUR_DOCKERHUB_USERNAME/blh-company:v1.0.0
```

## 운영 서버 배포

### 1. 운영 서버에서 실행
```bash
# 프로덕션 환경으로 실행
docker-compose -f docker-compose.prod.yml up -d

# 또는 Docker Hub 이미지 사용
docker run -d \
  --name blh-company \
  -p 8000:5000 \
  -e FLASK_ENV=production \
  YOUR_DOCKERHUB_USERNAME/blh-company:latest
```

### 2. Nginx 프록시와 함께 실행
```bash
# 전체 스택 실행 (웹앱 + Nginx + Redis)
docker-compose up -d
```

## 환경 변수 설정

프로덕션 환경에서 다음 환경 변수들을 설정하세요:

```bash
# .env 파일 생성
echo "FLASK_ENV=production" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "DATABASE_URL=sqlite:///blh_company.db" >> .env
echo "REDIS_URL=redis://redis:6379/0" >> .env
```

## 도메인 연결 및 SSL 설정

### 1. 도메인 DNS 설정
```
A 레코드: yourdomain.com → 서버IP
A 레코드: www.yourdomain.com → 서버IP
```

### 2. SSL 인증서 설정 (Let's Encrypt)
```bash
# Certbot 설치 및 인증서 발급
sudo apt update
sudo apt install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 백업 및 모니터링

### 데이터베이스 백업
```bash
# SQLite 데이터베이스 백업
docker exec blh-web-1 sqlite3 /app/blh_company.db .dump > backup_$(date +%Y%m%d).sql
```

### 로그 모니터링
```bash
# 실시간 로그 확인
docker-compose logs -f web

# 에러 로그만 확인
docker-compose logs web | grep ERROR
```

## 업데이트 배포

### 새 버전 배포
```bash
# 새 이미지 빌드
docker build -t blh-company:v1.1.0 .

# 태그 및 업로드
docker tag blh-company:v1.1.0 YOUR_DOCKERHUB_USERNAME/blh-company:v1.1.0
docker push YOUR_DOCKERHUB_USERNAME/blh-company:v1.1.0

# 서비스 업데이트 (무중단 배포)
docker-compose pull
docker-compose up -d
```

## 성능 최적화

### 1. 리소스 제한 설정
```yaml
# docker-compose.yml에 추가
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

### 2. Redis 캐시 설정
```python
# Flask 앱에서 Redis 캐시 활용
import redis
r = redis.Redis(host='redis', port=6379, db=0)
```

## 보안 설정

### 1. 방화벽 설정
```bash
# UFW 방화벽 설정
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. Docker 보안
```bash
# 비특권 사용자로 컨테이너 실행 (이미 적용됨)
# 네트워크 격리
# 시크릿 관리
```

## 트러블슈팅

### 컨테이너 재시작
```bash
docker-compose restart web
docker-compose restart nginx
```

### 로그 수집
```bash
# 모든 서비스 로그
docker-compose logs --tail=100

# 특정 서비스 로그
docker-compose logs web --tail=50
```

### 데이터베이스 문제 해결
```bash
# 컨테이너 내부 접속
docker exec -it blh-web-1 /bin/bash

# SQLite 데이터베이스 확인
sqlite3 /app/blh_company.db ".tables"
```

---

## 🎉 축하합니다!

BLH COMPANY 웹사이트가 성공적으로 Docker로 컨테이너화되어 실행 중입니다!

**접속 주소**: 
- 메인 사이트: http://localhost:8000
- 헬스체크: http://localhost:8000/health
- 관리자: http://localhost:8000/admin/notices

**다음 단계**:
1. 도메인 구매 및 연결
2. SSL 인증서 설정
3. 운영 서버에 배포
4. 모니터링 설정
