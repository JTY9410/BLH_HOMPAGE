#!/bin/bash

# 🚀 BLH COMPANY 자동 배포 스크립트
# 순서: Docker → GitHub → Vercel

set -e  # 에러 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# 배너 출력
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 BLH COMPANY 자동 배포                    ║"
echo "║                                                              ║"
echo "║  순서: 1️⃣ Docker → 2️⃣ GitHub → 3️⃣ Vercel                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 커밋 메시지 입력받기
if [ -z "$1" ]; then
    echo -e "${YELLOW}커밋 메시지를 입력하세요:${NC}"
    read -r COMMIT_MESSAGE
else
    COMMIT_MESSAGE="$1"
fi

if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="🔄 자동 배포 업데이트 $(date '+%Y-%m-%d %H:%M:%S')"
fi

log_info "커밋 메시지: $COMMIT_MESSAGE"
echo ""

# =============================================================================
# 1단계: Docker 배포
# =============================================================================
log_step "1️⃣ Docker 배포 시작..."

log_info "Docker 컨테이너 중지 및 제거..."
if docker-compose down; then
    log_success "Docker 컨테이너 중지 완료"
else
    log_warning "Docker 컨테이너 중지 실패 (이미 중지된 상태일 수 있음)"
fi

log_info "Docker 이미지 빌드 및 컨테이너 시작..."
if docker-compose up -d --build; then
    log_success "Docker 배포 완료"
else
    log_error "Docker 배포 실패"
    exit 1
fi

log_info "Docker 컨테이너 상태 확인..."
sleep 5
docker-compose ps

log_info "Docker 헬스체크..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    log_success "Docker 헬스체크 통과"
else
    log_warning "Docker 헬스체크 실패 - 계속 진행합니다"
fi

echo ""

# =============================================================================
# 2단계: GitHub 배포
# =============================================================================
log_step "2️⃣ GitHub 배포 시작..."

log_info "Git 상태 확인..."
git status --porcelain

log_info "변경사항을 Git에 추가..."
if git add .; then
    log_success "Git add 완료"
else
    log_error "Git add 실패"
    exit 1
fi

log_info "Git 커밋..."
if git commit -m "$COMMIT_MESSAGE"; then
    log_success "Git 커밋 완료"
elif git diff --cached --quiet; then
    log_warning "변경사항이 없어 커밋하지 않음"
else
    log_error "Git 커밋 실패"
    exit 1
fi

log_info "GitHub에 푸시..."
if git push origin main; then
    log_success "GitHub 푸시 완료"
else
    log_error "GitHub 푸시 실패"
    exit 1
fi

echo ""

# =============================================================================
# 3단계: Vercel 배포
# =============================================================================
log_step "3️⃣ Vercel 배포 시작..."

log_info "Vercel CLI 버전 확인..."
if command -v vercel &> /dev/null; then
    VERCEL_VERSION=$(vercel --version)
    log_info "Vercel CLI 버전: $VERCEL_VERSION"
else
    log_error "Vercel CLI가 설치되지 않았습니다"
    log_info "다음 명령어로 설치하세요: npm install -g vercel"
    exit 1
fi

log_info "Vercel 로그인 상태 확인..."
if vercel whoami &> /dev/null; then
    VERCEL_USER=$(vercel whoami)
    log_success "Vercel 로그인됨: $VERCEL_USER"
    
    log_info "Vercel 프로덕션 배포..."
    if vercel --prod --yes; then
        log_success "Vercel 배포 완료"
    else
        log_error "Vercel 배포 실패"
        exit 1
    fi
else
    log_warning "Vercel에 로그인되지 않음"
    log_info "수동으로 Vercel 웹사이트에서 배포하거나 'vercel login' 명령어를 실행하세요"
    log_info "Vercel 웹 배포: https://vercel.com/dashboard"
fi

echo ""

# =============================================================================
# 배포 완료 요약
# =============================================================================
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 배포 완료!                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log_success "✅ Docker: http://localhost"
log_success "✅ GitHub: https://github.com/JTY9410/BLH_HOMPAGE"

if vercel whoami &> /dev/null; then
    log_success "✅ Vercel: 배포 완료 (URL은 Vercel 대시보드에서 확인)"
else
    log_info "⏳ Vercel: 수동 배포 필요 (https://vercel.com/dashboard)"
fi

echo ""
log_info "배포 시간: $(date '+%Y-%m-%d %H:%M:%S')"
log_info "커밋 메시지: $COMMIT_MESSAGE"

echo ""
echo -e "${BLUE}🔗 유용한 링크:${NC}"
echo "   • 로컬 사이트: http://localhost"
echo "   • 관리자 페이지: http://localhost/admin/login"
echo "   • GitHub 저장소: https://github.com/JTY9410/BLH_HOMPAGE"
echo "   • Vercel 대시보드: https://vercel.com/dashboard"

echo ""
echo -e "${GREEN}🎯 배포가 성공적으로 완료되었습니다!${NC}"
