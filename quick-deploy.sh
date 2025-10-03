#!/bin/bash

# 🚀 BLH COMPANY 빠른 배포 스크립트
# 사용법: ./quick-deploy.sh "커밋 메시지"

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 BLH COMPANY 빠른 배포 시작...${NC}"

# 커밋 메시지 설정
COMMIT_MESSAGE="${1:-🔄 빠른 업데이트 $(date '+%Y-%m-%d %H:%M:%S')}"

echo "📝 커밋 메시지: $COMMIT_MESSAGE"

# 1. Docker 재배포
echo "🐳 Docker 재배포..."
docker-compose down && docker-compose up -d --build

# 2. GitHub 푸시
echo "📤 GitHub 푸시..."
git add . && git commit -m "$COMMIT_MESSAGE" && git push origin main

# 3. Vercel 배포 (로그인된 경우에만)
echo "🌐 Vercel 배포 확인..."
if vercel whoami &> /dev/null; then
    echo "✅ Vercel 자동 배포..."
    vercel --prod --yes
else
    echo "⚠️  Vercel 수동 배포 필요: https://vercel.com/dashboard"
fi

echo -e "${GREEN}🎉 배포 완료!${NC}"
echo "🔗 로컬: http://localhost"
echo "🔗 GitHub: https://github.com/JTY9410/BLH_HOMPAGE"
