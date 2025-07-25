import React, { useState, useEffect } from "react";

// Supabase 클라이언트 설정 (실제 사용시 환경변수로 관리)
const SUPABASE_URL = "https://ilkcrfhdcwpvcpfxpvwu.supabase.co";
const SUPABASE_ANON_KEY = "Ysb_publishable_P0wO-JjK8txkGrMJSu2iPw_06p3aSSx";

// Supabase 클라이언트 모의 구현
const createSupabaseClient = (url, key) => {
  return {
    from: (table) => ({
      select: (columns = "*") => ({
        eq: (column, value) => ({
          single: () => Promise.resolve({ data: null, error: null }),
        }),
        then: (callback) => {
          // 모의 데이터 반환
          const mockData =
            table === "courses"
              ? [
                  {
                    id: "CS101",
                    name: "프로그래밍 기초",
                    professor: "김교수",
                    credits: 3,
                    time: "월수금 10:00-11:00",
                    capacity: 50,
                    enrolled: 35,
                  },
                  {
                    id: "CS201",
                    name: "자료구조",
                    professor: "이교수",
                    credits: 3,
                    time: "화목 13:00-14:30",
                    capacity: 40,
                    enrolled: 28,
                  },
                  {
                    id: "CS301",
                    name: "데이터베이스",
                    professor: "박교수",
                    credits: 3,
                    time: "월수 15:00-16:30",
                    capacity: 35,
                    enrolled: 32,
                  },
                  {
                    id: "MATH101",
                    name: "미적분학",
                    professor: "최교수",
                    credits: 3,
                    time: "화목금 09:00-10:00",
                    capacity: 60,
                    enrolled: 45,
                  },
                  {
                    id: "ENG101",
                    name: "영어회화",
                    professor: "Smith",
                    credits: 2,
                    time: "월수 11:00-12:00",
                    capacity: 25,
                    enrolled: 20,
                  },
                ]
              : table === "registrations"
              ? [
                  {
                    id: "1",
                    student_id: "student123",
                    course_id: "CS101",
                    created_at: "2024-07-25T10:00:00Z",
                    courses: {
                      id: "CS101",
                      name: "프로그래밍 기초",
                      professor: "김교수",
                      credits: 3,
                      time: "월수금 10:00-11:00",
                      capacity: 50,
                      enrolled: 35,
                    },
                  },
                ]
              : [];

          return callback(Promise.resolve({ data: mockData, error: null }));
        },
      }),
      insert: (data) => ({
        then: (callback) => callback(Promise.resolve({ data, error: null })),
      }),
      delete: () => ({
        eq: (column, value) => ({
          then: (callback) =>
            callback(Promise.resolve({ data: null, error: null })),
        }),
      }),
      update: (data) => ({
        eq: (column, value) => ({
          then: (callback) => callback(Promise.resolve({ data, error: null })),
        }),
      }),
    }),
    channel: (name) => ({
      on: (event, table, callback) => ({
        subscribe: () => {},
      }),
    }),
  };
};

const supabase = createSupabaseClient(SUPABASE_URL, SUPABASE_ANON_KEY);

interface Course {
  id: string;
  name: string;
  professor: string;
  credits: number;
  time: string;
  capacity: number;
  enrolled: number;
}

interface Registration {
  id?: string;
  student_id: string;
  course_id: string;
  created_at?: string;
}

const App: React.FC = () => {
  const [availableCourses, setAvailableCourses] = useState<Course[]>([]);
  const [registeredCourses, setRegisteredCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [studentId] = useState("student123"); // 실제로는 로그인 시스템에서 가져옴

  const MAX_COURSES = 8;

  // 데이터 로드
  useEffect(() => {
    loadCourses();
    loadRegistrations();
    setupRealtimeSubscription();
  }, []);

  const loadCourses = async () => {
    try {
      const { data, error } = await supabase.from("courses").select("*");

      if (error) throw error;
      setAvailableCourses(data || []);
    } catch (error) {
      console.error("과목 데이터 로드 실패:", error);
    }
  };

  const loadRegistrations = async () => {
    try {
      const { data, error } = await supabase
        .from("registrations")
        .select(
          `
          *,
          courses (*)
        `
        )
        .eq("student_id", studentId);

      if (error) throw error;

      const registered = (data || []).map((reg) => reg.courses);
      setRegisteredCourses(registered);
    } catch (error) {
      console.error("신청 과목 로드 실패:", error);
    } finally {
      setLoading(false);
    }
  };

  // 실시간 업데이트 구독
  const setupRealtimeSubscription = () => {
    const subscription = supabase
      .channel("course-changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "courses" },
        () => {
          loadCourses();
        }
      )
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "registrations" },
        () => {
          loadRegistrations();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  };

  // 수강신청
  const registerCourse = async (course: Course) => {
    if (registeredCourses.length >= MAX_COURSES) {
      alert(`최대 ${MAX_COURSES}개 과목까지만 신청 가능합니다.`);
      return;
    }

    if (registeredCourses.find((c) => c.id === course.id)) {
      alert("이미 신청한 과목입니다.");
      return;
    }

    if (course.enrolled >= course.capacity) {
      alert("수강인원이 초과되었습니다.");
      return;
    }

    try {
      setLoading(true);

      // 신청 테이블에 추가
      const { error: regError } = await supabase.from("registrations").insert({
        student_id: studentId,
        course_id: course.id,
      });

      if (regError) throw regError;

      // 수강인원 증가
      const { error: courseError } = await supabase
        .from("courses")
        .update({ enrolled: course.enrolled + 1 })
        .eq("id", course.id);

      if (courseError) throw courseError;

      // 로컬 상태 업데이트
      setRegisteredCourses([...registeredCourses, course]);
      setAvailableCourses(
        availableCourses.map((c) =>
          c.id === course.id ? { ...c, enrolled: c.enrolled + 1 } : c
        )
      );

      alert("수강신청이 완료되었습니다.");
    } catch (error) {
      console.error("수강신청 실패:", error);
      alert("수강신청에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // 수강신청 취소
  const cancelCourse = async (courseId: string) => {
    try {
      setLoading(true);

      // 신청 테이블에서 삭제
      const { error: regError } = await supabase
        .from("registrations")
        .delete()
        .eq("student_id", studentId)
        .eq("course_id", courseId);

      if (regError) throw regError;

      // 수강인원 감소
      const course = availableCourses.find((c) => c.id === courseId);
      if (course) {
        const { error: courseError } = await supabase
          .from("courses")
          .update({ enrolled: course.enrolled - 1 })
          .eq("id", courseId);

        if (courseError) throw courseError;
      }

      // 로컬 상태 업데이트
      setRegisteredCourses(registeredCourses.filter((c) => c.id !== courseId));
      setAvailableCourses(
        availableCourses.map((c) =>
          c.id === courseId ? { ...c, enrolled: c.enrolled - 1 } : c
        )
      );

      alert("수강신청이 취소되었습니다.");
    } catch (error) {
      console.error("수강신청 취소 실패:", error);
      alert("수강신청 취소에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const totalCredits = registeredCourses.reduce(
    (sum, course) => sum + course.credits,
    0
  );

  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#f5f5f5",
      padding: "20px",
      fontFamily: "Arial, sans-serif",
    },
    header: {
      textAlign: "center" as const,
      fontSize: "28px",
      fontWeight: "bold",
      marginBottom: "30px",
      color: "#333",
    },
    setupNotice: {
      backgroundColor: "#fff3cd",
      border: "1px solid #ffeaa7",
      borderRadius: "8px",
      padding: "15px",
      marginBottom: "20px",
      fontSize: "14px",
      color: "#856404",
    },
    statusBox: {
      backgroundColor: "white",
      borderRadius: "8px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      padding: "20px",
      marginBottom: "20px",
    },
    statusTitle: {
      fontSize: "18px",
      fontWeight: "600",
      marginBottom: "15px",
      color: "#555",
    },
    statusInfo: {
      display: "flex",
      gap: "30px",
      fontSize: "14px",
    },
    mainContent: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "20px",
    },
    sectionBox: {
      backgroundColor: "white",
      borderRadius: "8px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      padding: "20px",
    },
    sectionTitle: {
      fontSize: "18px",
      fontWeight: "600",
      marginBottom: "15px",
      color: "#555",
    },
    table: {
      width: "100%",
      borderCollapse: "collapse" as const,
      fontSize: "14px",
    },
    th: {
      textAlign: "left" as const,
      padding: "10px 5px",
      borderBottom: "2px solid #eee",
      fontWeight: "600",
      color: "#666",
    },
    thCenter: {
      textAlign: "center" as const,
      padding: "10px 5px",
      borderBottom: "2px solid #eee",
      fontWeight: "600",
      color: "#666",
    },
    td: {
      padding: "10px 5px",
      borderBottom: "1px solid #f0f0f0",
    },
    tdCenter: {
      padding: "10px 5px",
      borderBottom: "1px solid #f0f0f0",
      textAlign: "center" as const,
    },
    tr: {
      cursor: "pointer",
      opacity: loading ? 0.7 : 1,
    },
    button: {
      padding: "5px 12px",
      borderRadius: "4px",
      border: "none",
      fontSize: "12px",
      cursor: "pointer",
      fontWeight: "500",
      disabled: loading,
    },
    registerButton: {
      backgroundColor: "#007bff",
      color: "white",
    },
    disabledButton: {
      backgroundColor: "#ccc",
      color: "#666",
      cursor: "not-allowed",
    },
    cancelButton: {
      backgroundColor: "#dc3545",
      color: "white",
    },
    enrollmentFull: {
      color: "#dc3545",
    },
    enrollmentAvailable: {
      color: "#28a745",
    },
    emptyMessage: {
      textAlign: "center" as const,
      color: "#888",
      padding: "30px 0",
      fontStyle: "italic",
    },
    blueText: {
      color: "#007bff",
    },
    greenText: {
      color: "#28a745",
    },
    loadingOverlay: {
      position: "fixed" as const,
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: "rgba(0,0,0,0.3)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000,
    },
    loadingSpinner: {
      width: "40px",
      height: "40px",
      border: "4px solid #f3f3f3",
      borderTop: "4px solid #007bff",
      borderRadius: "50%",
      animation: "spin 1s linear infinite",
    },
  };

  if (loading && availableCourses.length === 0) {
    return (
      <div style={styles.container}>
        <div style={styles.loadingOverlay}>
          <div style={styles.loadingSpinner}></div>
        </div>
        <h1 style={styles.header}>데이터 로딩 중...</h1>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>

      <h1 style={styles.header}>수강신청 시스템 (Supabase 연동)</h1>

      <div style={styles.setupNotice}>
        <strong>📋 Supabase 설정 안내:</strong>
        <br />
        1. Supabase 프로젝트에서 다음 테이블들을 생성하세요:
        <br />• <code>courses</code>: id(text), name(text), professor(text),
        credits(int), time(text), capacity(int), enrolled(int)
        <br />• <code>registrations</code>: id(uuid), student_id(text),
        course_id(text), created_at(timestamp)
        <br />
        2. 코드 상단의 SUPABASE_URL과 SUPABASE_ANON_KEY를 실제 값으로
        변경하세요.
        <br />
        3. 현재는 모의 데이터로 동작합니다.
      </div>

      {/* 신청 현황 */}
      <div style={styles.statusBox}>
        <h2 style={styles.statusTitle}>신청 현황</h2>
        <div style={styles.statusInfo}>
          <span style={styles.blueText}>
            신청 과목: {registeredCourses.length}/{MAX_COURSES}개
          </span>
          <span style={styles.greenText}>총 학점: {totalCredits}학점</span>
          <span>학생 ID: {studentId}</span>
        </div>
      </div>

      <div style={styles.mainContent}>
        {/* 개설 과목 목록 */}
        <div style={styles.sectionBox}>
          <h2 style={styles.sectionTitle}>개설 과목 목록</h2>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>과목명</th>
                <th style={styles.th}>교수</th>
                <th style={styles.thCenter}>학점</th>
                <th style={styles.th}>시간</th>
                <th style={styles.thCenter}>인원</th>
                <th style={styles.thCenter}>신청</th>
              </tr>
            </thead>
            <tbody>
              {availableCourses.map((course) => (
                <tr
                  key={course.id}
                  style={styles.tr}
                  onMouseEnter={(e) =>
                    (e.currentTarget.style.backgroundColor = "#f8f9fa")
                  }
                  onMouseLeave={(e) =>
                    (e.currentTarget.style.backgroundColor = "transparent")
                  }
                >
                  <td style={{ ...styles.td, fontWeight: "500" }}>
                    {course.name}
                  </td>
                  <td style={styles.td}>{course.professor}</td>
                  <td style={styles.tdCenter}>{course.credits}</td>
                  <td style={styles.td}>{course.time}</td>
                  <td style={styles.tdCenter}>
                    <span
                      style={
                        course.enrolled >= course.capacity
                          ? styles.enrollmentFull
                          : styles.enrollmentAvailable
                      }
                    >
                      {course.enrolled}/{course.capacity}
                    </span>
                  </td>
                  <td style={styles.tdCenter}>
                    <button
                      onClick={() => registerCourse(course)}
                      disabled={
                        loading ||
                        !!registeredCourses.find((c) => c.id === course.id) ||
                        course.enrolled >= course.capacity
                      }
                      style={{
                        ...styles.button,
                        ...(loading ||
                        registeredCourses.find((c) => c.id === course.id) ||
                        course.enrolled >= course.capacity
                          ? styles.disabledButton
                          : styles.registerButton),
                      }}
                    >
                      {registeredCourses.find((c) => c.id === course.id)
                        ? "신청완료"
                        : loading
                        ? "처리중..."
                        : "신청"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* 신청한 과목 목록 */}
        <div style={styles.sectionBox}>
          <h2 style={styles.sectionTitle}>신청한 과목</h2>
          {registeredCourses.length === 0 ? (
            <p style={styles.emptyMessage}>신청한 과목이 없습니다.</p>
          ) : (
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>과목명</th>
                  <th style={styles.th}>교수</th>
                  <th style={styles.thCenter}>학점</th>
                  <th style={styles.th}>시간</th>
                  <th style={styles.thCenter}>취소</th>
                </tr>
              </thead>
              <tbody>
                {registeredCourses.map((course) => (
                  <tr
                    key={course.id}
                    style={styles.tr}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.backgroundColor = "#f8f9fa")
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.backgroundColor = "transparent")
                    }
                  >
                    <td style={{ ...styles.td, fontWeight: "500" }}>
                      {course.name}
                    </td>
                    <td style={styles.td}>{course.professor}</td>
                    <td style={styles.tdCenter}>{course.credits}</td>
                    <td style={styles.td}>{course.time}</td>
                    <td style={styles.tdCenter}>
                      <button
                        onClick={() => cancelCourse(course.id)}
                        disabled={loading}
                        style={{
                          ...styles.button,
                          ...(loading
                            ? styles.disabledButton
                            : styles.cancelButton),
                        }}
                      >
                        {loading ? "처리중..." : "취소"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
