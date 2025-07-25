import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import numpy as np

# 한글 폰트 설정 개선
def setup_korean_font():
    """한글 폰트 설정"""
    try:
        # Windows의 경우
        import platform
        if platform.system() == 'Windows':
            plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
        else:
            # macOS, Linux의 경우
            plt.rcParams['font.family'] = ['AppleGothic', 'Nanum Gothic', 'DejaVu Sans']
        
        plt.rcParams['axes.unicode_minus'] = False
        print("✅ 한글 폰트 설정 완료")
    except Exception as e:
        print(f"⚠️ 한글 폰트 설정 실패: {e}")
        # 기본 설정으로 대체
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False

# DB 파일 경로 (상대경로로 수정)
DB_PATH = './14-dbms/students-csv.db'

# 1. SQLite DB에서 데이터 읽기
def load_students_from_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM students', conn)
    conn.close()
    return df

def clean_grade_data(df):
    """학년 데이터 정리"""
    # grade 컬럼에서 중복된 '학년' 제거
    df['grade_clean'] = df['grade'].str.replace('학년', '').str.strip()
    df['grade_num'] = pd.to_numeric(df['grade_clean'], errors='coerce')
    return df

def visualize_data(df):
    """데이터 시각화 함수"""
    # 데이터 정리
    df = clean_grade_data(df)
    
    # 전체 그래프 스타일 설정
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 2x2 서브플롯 생성
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Student Data Analysis Visualization', fontsize=16, fontweight='bold')
    
    # 1. 학년별 학생 수 막대 차트
    grade_counts = df['grade_num'].value_counts().sort_index()
    axes[0, 0].bar(grade_counts.index, grade_counts.values, color='skyblue', alpha=0.7)
    axes[0, 0].set_title('Students by Grade', fontweight='bold')
    axes[0, 0].set_xlabel('Grade')
    axes[0, 0].set_ylabel('Number of Students')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # 막대 위에 숫자 표시
    for i, v in enumerate(grade_counts.values):
        axes[0, 0].text(grade_counts.index[i], v + 0.1, str(v), 
                       ha='center', va='bottom', fontweight='bold')
    
    # 2. 나이 분포 히스토그램
    axes[0, 1].hist(df['age'], bins=8, color='lightcoral', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Age Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Number of Students')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # 3. 학년별 나이 평균 막대 차트
    age_by_grade = df.groupby('grade_num')['age'].mean().sort_index()
    axes[1, 0].bar(age_by_grade.index, age_by_grade.values, color='lightgreen', alpha=0.7)
    axes[1, 0].set_title('Average Age by Grade', fontweight='bold')
    axes[1, 0].set_xlabel('Grade')
    axes[1, 0].set_ylabel('Average Age')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # 막대 위에 평균값 표시
    for i, v in enumerate(age_by_grade.values):
        axes[1, 0].text(age_by_grade.index[i], v + 0.1, f'{v:.1f}', 
                       ha='center', va='bottom', fontweight='bold')
    
    # 4. 학년별 나이 분포 박스플롯
    sns.boxplot(data=df, x='grade_num', y='age', ax=axes[1, 1])
    axes[1, 1].set_title('Age Distribution by Grade (Boxplot)', fontweight='bold')
    axes[1, 1].set_xlabel('Grade')
    axes[1, 1].set_ylabel('Age')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    # 레이아웃 조정
    plt.tight_layout()
    plt.show()
    
    # 추가 상세 분석 차트
    create_additional_charts(df)

def create_additional_charts(df):
    """추가 상세 분석 차트"""
    # 성별이 있다면 성별 분석도 추가
    if 'gender' in df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Gender-based Analysis', fontsize=14, fontweight='bold')
        
        # 성별 분포
        gender_counts = df['gender'].value_counts()
        axes[0].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
                   colors=['lightblue', 'lightpink'])
        axes[0].set_title('Gender Distribution')
        
        # 성별-학년별 분포
        gender_grade = pd.crosstab(df['grade_num'], df['gender'])
        gender_grade.plot(kind='bar', ax=axes[1], color=['lightblue', 'lightpink'])
        axes[1].set_title('Gender Distribution by Grade')
        axes[1].set_xlabel('Grade')
        axes[1].set_ylabel('Number of Students')
        axes[1].legend(title='Gender')
        axes[1].tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        plt.show()
    
    # 나이와 학년의 상관관계 산점도
    plt.figure(figsize=(8, 6))
    plt.scatter(df['grade_num'], df['age'], alpha=0.6, s=50, color='purple')
    plt.title('Correlation between Grade and Age', fontweight='bold')
    plt.xlabel('Grade')
    plt.ylabel('Age')
    plt.grid(True, alpha=0.3)
    
    # 추세선 추가
    valid_data = df[['grade_num', 'age']].dropna()
    if len(valid_data) > 1:
        z = np.polyfit(valid_data['grade_num'], valid_data['age'], 1)
        p = np.poly1d(z)
        plt.plot(valid_data['grade_num'], p(valid_data['grade_num']), "r--", alpha=0.8, linewidth=2)
    plt.show()

def print_detailed_analysis(df):
    """상세 분석 결과 출력"""
    df = clean_grade_data(df)
    
    print('\n' + '='*50)
    print('📊 Detailed Data Analysis Results')
    print('='*50)
    
    print(f'📈 Total Students: {len(df)} students')
    print(f'📚 Grade Range: Grade {df["grade_num"].min()} ~ Grade {df["grade_num"].max()}')
    print(f'👶 Age Range: {df["age"].min()} ~ {df["age"].max()} years old')
    print(f'📊 Average Age: {df["age"].mean():.1f} years old')
    
    print('\n📋 Detailed Info by Grade:')
    grade_analysis = df.groupby('grade_num').agg({
        'age': ['count', 'mean', 'min', 'max']
    }).round(1)
    grade_analysis.columns = ['Students', 'Avg_Age', 'Min_Age', 'Max_Age']
    print(grade_analysis)
    
    if 'gender' in df.columns:
        print('\n👥 Gender Distribution:')
        print(df['gender'].value_counts())

def main():
    # 한글 폰트 설정
    setup_korean_font()
    
    try:
        # 데이터 불러오기
        df = load_students_from_db()
        print('=== Full Dataset ===')
        print(df)
        print(f'\nData Shape: {df.shape}')
        print(f'Columns: {list(df.columns)}')

        # 기본 분석
        print('\n=== Basic Statistical Analysis ===')
        print('\nTotal Students:', len(df))
        print('\nStudents by Grade:')
        print(df['grade'].value_counts().sort_index())
        print('\nAge Statistics:')
        print(df['age'].describe())
        print('\nAverage Age by Grade:')
        grade_age = df.groupby('grade')['age'].mean().round(1)
        print(grade_age)
        
        # 상세 분석 출력
        print_detailed_analysis(df)
        
        # 데이터 시각화
        print('\n📈 Generating data visualization...')
        visualize_data(df)
        
    except FileNotFoundError:
        print(f"❌ Database file not found: {DB_PATH}")
        print("Please check if 'students-csv.db' file exists in the current directory.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    main()