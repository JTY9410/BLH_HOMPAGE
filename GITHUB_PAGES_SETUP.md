# GitHub Pages 설정 가이드

## 🔧 GitHub Pages 활성화 방법

### 1. GitHub 저장소 Settings 접근
1. [BLH_HOMPAGE 저장소](https://github.com/JTY9410/BLH_HOMPAGE) 방문
2. 상단 메뉴에서 **Settings** 클릭
3. 왼쪽 사이드바에서 **Pages** 클릭

### 2. GitHub Pages 설정
1. **Source** 섹션에서 **GitHub Actions** 선택
2. **Save** 버튼 클릭

### 3. 배포 확인
1. **Actions** 탭으로 이동
2. 최근 워크플로우 실행 상태 확인
3. 성공적으로 완료되면 Pages URL 생성됨

## 🌐 예상 배포 URL
```
https://jty9410.github.io/BLH_HOMPAGE/
```

## 🚨 문제 해결

### 배포 에러가 발생했던 이유:
- **원인**: Node.js 기반 워크플로우가 Python Flask 프로젝트에 잘못 적용됨
- **에러**: `KeyError: '__version__'` - 패키지 버전 정보 누락
- **해결**: Python 기반 워크플로우로 수정 및 최소 패키지 사용

### 수정된 내용:
1. ✅ **Python 3.11 환경** 설정
2. ✅ **최소 필수 패키지** 설치 (requirements-minimal.txt)
3. ✅ **정적 파일 생성** 프로세스 개선
4. ✅ **에러 복구 옵션** 추가
5. ✅ **동시 배포 방지** 설정

## 📋 다음 단계
1. GitHub Settings에서 Pages 활성화
2. 워크플로우 실행 완료 대기
3. 배포 URL 확인 및 테스트

## 📞 지원
문제가 지속되면 GitHub Actions 로그를 확인하거나 이슈를 생성해주세요.
