# 🚀 BLH COMPANY 자동 배포 프로세스

## 📋 배포 순서

프로그램이 수정되면 다음 순서로 자동 배포됩니다:

```
1️⃣ Docker 배포 → 2️⃣ GitHub 푸시 → 3️⃣ Vercel 배포
```

## 🛠️ 배포 방법

### 방법 1: 전체 자동 배포 (권장)

```bash
./deploy.sh "커밋 메시지"
```

**예시:**
```bash
./deploy.sh "🎨 홈페이지 디자인 업데이트"
./deploy.sh "🐛 버그 수정 및 성능 개선"
./deploy.sh "✨ 새로운 기능 추가"
```

### 방법 2: 빠른 배포

```bash
./quick-deploy.sh "커밋 메시지"
```

**예시:**
```bash
./quick-deploy.sh "빠른 수정"
./quick-deploy.sh  # 기본 메시지 사용
```

### 방법 3: 수동 배포

```bash
# 1단계: Docker
docker-compose down
docker-compose up -d --build

# 2단계: GitHub
git add .
git commit -m "업데이트 메시지"
git push origin main

# 3단계: Vercel
vercel --prod --yes
```

## 📊 배포 단계별 상세 설명

### 1️⃣ Docker 배포

**목적**: 로컬 개발 환경에서 테스트
**과정**:
1. 기존 컨테이너 중지 및 제거
2. 새로운 이미지 빌드
3. 컨테이너 시작
4. 헬스체크 수행

**확인 방법**:
- `http://localhost` 접속
- `docker-compose ps` 상태 확인

### 2️⃣ GitHub 푸시

**목적**: 소스코드 버전 관리 및 백업
**과정**:
1. 변경사항 스테이징 (`git add .`)
2. 커밋 생성 (`git commit`)
3. 원격 저장소 푸시 (`git push`)

**확인 방법**:
- GitHub 저장소에서 최신 커밋 확인
- Actions 탭에서 자동화 작업 확인

### 3️⃣ Vercel 배포

**목적**: 프로덕션 환경 배포
**과정**:
1. Vercel 로그인 상태 확인
2. 프로덕션 배포 실행
3. 배포 URL 생성

**확인 방법**:
- Vercel 대시보드에서 배포 상태 확인
- 배포된 URL에서 사이트 동작 확인

## 🔧 배포 스크립트 기능

### `deploy.sh` (전체 배포)

**특징**:
- ✅ 상세한 로그 출력
- ✅ 각 단계별 성공/실패 확인
- ✅ 에러 발생 시 중단
- ✅ 배포 완료 요약 제공
- ✅ 유용한 링크 제공

**사용 시나리오**:
- 중요한 업데이트
- 새로운 기능 배포
- 정식 릴리즈

### `quick-deploy.sh` (빠른 배포)

**특징**:
- ⚡ 빠른 실행
- ⚡ 간단한 출력
- ⚡ 기본 메시지 자동 생성

**사용 시나리오**:
- 빠른 수정사항
- 테스트 배포
- 개발 중 임시 배포

## 📁 배포 관련 파일 구조

```
/Users/USER/dev/blh/
├── deploy.sh              # 전체 자동 배포 스크립트
├── quick-deploy.sh         # 빠른 배포 스크립트
├── docker-compose.yml      # Docker 설정
├── Dockerfile             # Docker 이미지 설정
├── vercel.json            # Vercel 배포 설정
├── api/index.py           # Vercel 엔트리포인트
├── requirements-vercel.txt # Vercel 의존성
└── .vercelignore          # Vercel 제외 파일
```

## ⚠️ 주의사항

### Docker 배포
- 포트 80이 사용 중이면 배포 실패
- 이미지 빌드 시간이 소요될 수 있음

### GitHub 푸시
- 인터넷 연결 필요
- Git 인증 정보 필요
- 변경사항이 없으면 커밋 생략

### Vercel 배포
- Vercel 로그인 필요 (`vercel login`)
- 첫 배포 시 프로젝트 설정 필요
- 빌드 시간 소요 (1-3분)

## 🔍 문제 해결

### Docker 배포 실패
```bash
# 포트 확인
lsof -i :80

# 컨테이너 강제 제거
docker-compose down --volumes --remove-orphans
```

### GitHub 푸시 실패
```bash
# Git 상태 확인
git status

# 원격 저장소 확인
git remote -v
```

### Vercel 배포 실패
```bash
# 로그인 확인
vercel whoami

# 수동 로그인
vercel login
```

## 📈 배포 모니터링

### 로컬 환경 (Docker)
- **URL**: http://localhost
- **관리자**: http://localhost/admin/login
- **헬스체크**: http://localhost/health

### 프로덕션 환경 (Vercel)
- **대시보드**: https://vercel.com/dashboard
- **배포 로그**: Vercel 대시보드에서 확인
- **도메인**: 자동 생성 또는 커스텀 설정

## 🎯 배포 체크리스트

배포 전 확인사항:
- [ ] 코드 변경사항 테스트 완료
- [ ] Docker 로컬 테스트 통과
- [ ] 커밋 메시지 작성
- [ ] 중요 데이터 백업 (필요시)

배포 후 확인사항:
- [ ] Docker 컨테이너 정상 동작
- [ ] GitHub 최신 코드 반영
- [ ] Vercel 배포 성공
- [ ] 프로덕션 사이트 정상 동작

---

## 🚀 빠른 시작

1. **권한 설정** (최초 1회):
   ```bash
   chmod +x deploy.sh quick-deploy.sh
   ```

2. **배포 실행**:
   ```bash
   ./deploy.sh "업데이트 메시지"
   ```

3. **결과 확인**:
   - 로컬: http://localhost
   - 프로덕션: Vercel 대시보드에서 URL 확인

**🎉 이제 한 번의 명령어로 모든 환경에 자동 배포할 수 있습니다!**
