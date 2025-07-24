-- 데이터베이스 >테이블 >행record > 열 column
-- mydb.db         users       번호 이름 주소
--                 items       1. 홍갈동 서울   
--                 orders      2. 홍동동 시얼

--코멘트 주석
-- 대문자 : SQL 예약어
-- 소문자 : 사용자 변수

            

-- 테이블 생성
create table student(

    id INTEGER PRIMARY KEY AUTOINCREMENT,   --DB 인덱스 (학번,이나 주민번호가 아님), AUTOINCREMENT 1씩 자동 증가  
    name TEXT NOT NULL, --WHEN you INSERT, if its null there is error 
    age INTEGER NOT null,
    grade TEXT NOT NULL,
    -- TIMESTAMP : 날짜시간, DATE  두개중 사용하면댐 
    profile_img TEXT, --myprofile_202507241929.png


    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP






);  --여러줄을 쓸 때 개별로 실행되게 함.

-- 데이터 (레코드, 행) 추가
-- id: 자동증가, created_at : 기본값
INSERT INTO student (name, age, grade)
VALUES ('홍길동', 30, 'A+')
SELECT * FROM student;

-- 전체검색
    -- * : 모든 컬럼을 출력하라
