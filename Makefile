# BLH COMPANY 자동 배포 Makefile

.PHONY: help deploy deploy-quick deploy-docker deploy-github deploy-vercel start stop restart logs status health clean

# 기본 타겟
.DEFAULT_GOAL := help

# 색상 정의
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

## 도움말 표시
help:
	@echo "$(BLUE)🚀 BLH COMPANY 배포 명령어$(NC)"
	@echo ""
	@echo "$(GREEN)배포 명령어:$(NC)"
	@echo "  make deploy         - 전체 자동 배포 (Docker → GitHub → Vercel)"
	@echo "  make deploy-quick   - 빠른 배포"
	@echo "  make deploy-docker  - Docker만 배포"
	@echo "  make deploy-github  - GitHub만 푸시"
	@echo "  make deploy-vercel  - Vercel만 배포"
	@echo ""
	@echo "$(GREEN)Docker 관리:$(NC)"
	@echo "  make start          - Docker 컨테이너 시작"
	@echo "  make stop           - Docker 컨테이너 중지"
	@echo "  make restart        - Docker 컨테이너 재시작"
	@echo "  make logs           - Docker 로그 보기"
	@echo "  make status         - Docker 상태 확인"
	@echo "  make health         - 헬스체크"
	@echo ""
	@echo "$(GREEN)기타:$(NC)"
	@echo "  make clean          - 정리 작업"
	@echo "  make help           - 이 도움말 표시"

## 전체 자동 배포 (Docker → GitHub → Vercel)
deploy:
	@echo "$(BLUE)🚀 전체 자동 배포 시작...$(NC)"
	@./deploy.sh "🔄 Makefile을 통한 자동 배포 $(shell date '+%Y-%m-%d %H:%M:%S')"

## 빠른 배포
deploy-quick:
	@echo "$(BLUE)⚡ 빠른 배포 시작...$(NC)"
	@./quick-deploy.sh "⚡ 빠른 업데이트 $(shell date '+%Y-%m-%d %H:%M:%S')"

## Docker 배포
deploy-docker:
	@echo "$(BLUE)🐳 Docker 배포 시작...$(NC)"
	@docker-compose down
	@docker-compose up -d --build
	@echo "$(GREEN)✅ Docker 배포 완료$(NC)"

## GitHub 푸시
deploy-github:
	@echo "$(BLUE)📤 GitHub 푸시 시작...$(NC)"
	@git add .
	@git commit -m "🔄 Makefile을 통한 업데이트 $(shell date '+%Y-%m-%d %H:%M:%S')" || echo "변경사항 없음"
	@git push origin main
	@echo "$(GREEN)✅ GitHub 푸시 완료$(NC)"

## Vercel 배포
deploy-vercel:
	@echo "$(BLUE)🌐 Vercel 배포 시작...$(NC)"
	@if command -v vercel >/dev/null 2>&1; then \
		if vercel whoami >/dev/null 2>&1; then \
			vercel --prod --yes; \
			echo "$(GREEN)✅ Vercel 배포 완료$(NC)"; \
		else \
			echo "$(YELLOW)⚠️  Vercel 로그인 필요: vercel login$(NC)"; \
		fi; \
	else \
		echo "$(YELLOW)⚠️  Vercel CLI 설치 필요: npm install -g vercel$(NC)"; \
	fi

## Docker 컨테이너 시작
start:
	@echo "$(BLUE)🚀 Docker 컨테이너 시작...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✅ 컨테이너 시작 완료$(NC)"

## Docker 컨테이너 중지
stop:
	@echo "$(BLUE)🛑 Docker 컨테이너 중지...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✅ 컨테이너 중지 완료$(NC)"

## Docker 컨테이너 재시작
restart:
	@echo "$(BLUE)🔄 Docker 컨테이너 재시작...$(NC)"
	@docker-compose restart
	@echo "$(GREEN)✅ 컨테이너 재시작 완료$(NC)"

## Docker 로그 보기
logs:
	@echo "$(BLUE)📋 Docker 로그 보기...$(NC)"
	@docker-compose logs -f

## Docker 상태 확인
status:
	@echo "$(BLUE)📊 Docker 상태 확인...$(NC)"
	@docker-compose ps

## 헬스체크
health:
	@echo "$(BLUE)🏥 헬스체크 실행...$(NC)"
	@if curl -f http://localhost/health >/dev/null 2>&1; then \
		echo "$(GREEN)✅ 헬스체크 통과$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  헬스체크 실패$(NC)"; \
	fi

## 정리 작업
clean:
	@echo "$(BLUE)🧹 정리 작업 시작...$(NC)"
	@docker-compose down --volumes --remove-orphans
	@docker system prune -f
	@echo "$(GREEN)✅ 정리 작업 완료$(NC)"

# 커밋 메시지와 함께 배포
deploy-with-message:
	@read -p "커밋 메시지를 입력하세요: " msg; \
	./deploy.sh "$$msg"
