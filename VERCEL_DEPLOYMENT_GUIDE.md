# 🚀 BLH COMPANY Vercel 자동 배포 가이드

## 📋 배포 준비 완료 상태

✅ **Vercel 설정 파일 생성 완료**
- `vercel.json`: 서버리스 함수 설정
- `api/index.py`: Vercel 엔트리포인트
- `requirements-vercel.txt`: 최소 의존성 패키지
- `.vercelignore`: 불필요한 파일 제외

✅ **Flask 애플리케이션 최적화 완료**
- 메모리 데이터베이스 지원 (Vercel 환경)
- 데이터베이스 연결 헬퍼 함수 추가
- 환경별 데이터베이스 초기화
- 서버리스 환경 호환성 개선

✅ **GitHub 푸시 완료**
- 모든 설정 파일이 GitHub에 업로드됨
- 자동 배포 준비 완료

## 🌐 Vercel 웹 배포 방법 (권장)

### 1단계: Vercel 계정 생성 및 GitHub 연동

1. **Vercel 웹사이트 접속**: https://vercel.com
2. **GitHub로 로그인**: "Continue with GitHub" 클릭
3. **GitHub 계정 연동**: 권한 승인

### 2단계: 프로젝트 Import

1. **New Project 클릭**
2. **GitHub 저장소 선택**: `JTY9410/BLH_HOMPAGE` 선택
3. **Import 클릭**

### 3단계: 배포 설정 확인

Vercel이 자동으로 다음 설정을 감지합니다:
- **Framework Preset**: Other
- **Build Command**: (자동 감지)
- **Output Directory**: (자동 감지)
- **Install Command**: `pip install -r requirements-vercel.txt`

### 4단계: 환경 변수 설정 (선택사항)

필요시 다음 환경 변수를 추가:
- `VERCEL`: `1`
- `FLASK_ENV`: `production`

### 5단계: Deploy 클릭

- **Deploy** 버튼 클릭
- 자동 빌드 및 배포 시작
- 완료 시 배포 URL 제공

## 🔧 CLI를 통한 배포 방법 (대안)

터미널에서 다음 명령어 실행:

```bash
# Vercel 로그인
vercel login

# 프로젝트 배포
vercel --prod
```

## 📊 배포 후 확인사항

### ✅ 정상 작동 확인
- [ ] 메인 페이지 로드
- [ ] 관리자 로그인 (`/admin/login`)
- [ ] 공지사항 페이지
- [ ] 정적 파일 (이미지, CSS, JS)

### ⚠️ 주의사항

1. **데이터베이스**: Vercel에서는 메모리 데이터베이스 사용
   - 서버 재시작 시 데이터 초기화됨
   - 영구 데이터 저장이 필요한 경우 외부 DB 연동 필요

2. **파일 업로드**: 서버리스 환경에서는 파일 업로드 제한
   - 이미지 등은 정적 파일로만 제공

3. **세션 관리**: 서버리스 환경에서 세션 유지 제한
   - 관리자 로그인 상태가 일정 시간 후 초기화될 수 있음

## 🎯 배포 완료 후 예상 URL

배포 완료 시 다음과 같은 URL이 제공됩니다:
- **프로덕션 URL**: `https://blh-homepage-xxxx.vercel.app`
- **커스텀 도메인**: 설정 가능

## 🔄 자동 배포 설정

GitHub에 푸시할 때마다 자동으로 Vercel에 배포됩니다:
1. GitHub에 코드 푸시
2. Vercel이 자동으로 감지
3. 자동 빌드 및 배포
4. 새로운 버전 배포 완료

## 📞 지원

배포 과정에서 문제가 발생하면:
1. Vercel 대시보드에서 빌드 로그 확인
2. GitHub 저장소의 Actions 탭 확인
3. 필요시 설정 파일 수정 후 재배포

---

**🎉 모든 설정이 완료되었습니다! Vercel 웹사이트에서 간단히 배포를 완료하세요.**
