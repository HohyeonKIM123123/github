# Daily automated tasks scheduler
import schedule
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_utils import DatabaseManager
from modules.loan_logic import LoanManager
from modules.email_notifier import EmailNotifier
from modules.report_generator import ReportGenerator

class DailyTaskScheduler:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
        self.db_manager = DatabaseManager(db_path)
        self.loan_manager = LoanManager(self.db_manager)
        self.email_notifier = EmailNotifier()
        self.report_generator = ReportGenerator(self.db_manager)
    
    def send_overdue_notifications(self):
        """연체 도서 알림 발송"""
        print(f"[{datetime.now()}] 연체 알림 작업 시작")
        
        try:
            overdue_loans = self.loan_manager.get_overdue_loans()
            
            if not overdue_loans:
                print("연체된 도서가 없습니다.")
                return
            
            # 회원별로 연체 도서 그룹화
            member_overdue = {}
            for loan in overdue_loans:
                member_id = loan['member_id']
                if member_id not in member_overdue:
                    member_overdue[member_id] = {
                        'name': loan['name'],
                        'email': loan['email'],
                        'books': []
                    }
                member_overdue[member_id]['books'].append(loan)
            
            # 알림 발송
            success_count = 0
            for member_data in member_overdue.values():
                if self.email_notifier.send_overdue_notification(
                    member_data['email'],
                    member_data['name'],
                    member_data['books']
                ):
                    success_count += 1
            
            print(f"연체 알림 발송 완료: {success_count}/{len(member_overdue)}명")
            
        except Exception as e:
            print(f"연체 알림 작업 실패: {e}")
    
    def generate_daily_summary(self):
        """일일 요약 보고서 생성"""
        print(f"[{datetime.now()}] 일일 요약 보고서 생성 시작")
        
        try:
            # 연체 현황 요약
            overdue_summary = self.report_generator.get_overdue_summary()
            
            # 오늘의 대출/반납 통계
            today = datetime.now().strftime('%Y-%m-%d')
            today_stats_query = """
            SELECT 
                COUNT(CASE WHEN loan_date = ? THEN 1 END) as today_loans,
                COUNT(CASE WHEN return_date = ? THEN 1 END) as today_returns
            FROM loans
            """
            today_stats = self.db_manager.execute_query(today_stats_query, (today, today))[0]
            
            # 요약 정보 출력
            print("=== 일일 요약 보고서 ===")
            print(f"오늘 대출: {today_stats['today_loans']}건")
            print(f"오늘 반납: {today_stats['today_returns']}건")
            print(f"총 연체: {overdue_summary['total_overdue']}건")
            print(f"연체 회원: {overdue_summary['affected_members']}명")
            print("=====================")
            
        except Exception as e:
            print(f"일일 요약 보고서 생성 실패: {e}")
    
    def cleanup_old_data(self):
        """오래된 데이터 정리"""
        print(f"[{datetime.now()}] 데이터 정리 작업 시작")
        
        try:
            # 1년 이상 된 반납 완료 대출 기록 아카이브
            archive_query = """
            UPDATE loans 
            SET status = 'archived' 
            WHERE status = 'returned' 
            AND return_date < date('now', '-1 year')
            """
            archived_count = self.db_manager.execute_update(archive_query)
            
            print(f"아카이브된 대출 기록: {archived_count}건")
            
        except Exception as e:
            print(f"데이터 정리 작업 실패: {e}")
    
    def start_scheduler(self):
        """스케줄러 시작"""
        print("도서관 일일 작업 스케줄러 시작")
        
        # 매일 오전 9시에 연체 알림 발송
        schedule.every().day.at("09:00").do(self.send_overdue_notifications)
        
        # 매일 오후 6시에 일일 요약 보고서 생성
        schedule.every().day.at("18:00").do(self.generate_daily_summary)
        
        # 매주 일요일 자정에 데이터 정리
        schedule.every().sunday.at("00:00").do(self.cleanup_old_data)
        
        # 테스트용: 즉시 실행
        print("초기 작업 실행 중...")
        self.generate_daily_summary()
        
        # 스케줄러 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크

def main():
    scheduler = DailyTaskScheduler()
    
    # 명령행 인자 처리
    if len(sys.argv) > 1:
        if sys.argv[1] == "overdue":
            scheduler.send_overdue_notifications()
        elif sys.argv[1] == "summary":
            scheduler.generate_daily_summary()
        elif sys.argv[1] == "cleanup":
            scheduler.cleanup_old_data()
        else:
            print("사용법: python daily_tasks.py [overdue|summary|cleanup]")
    else:
        # 스케줄러 모드로 실행
        scheduler.start_scheduler()

if __name__ == "__main__":
    main()