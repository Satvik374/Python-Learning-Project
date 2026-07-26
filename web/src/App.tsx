import { useEffect, useMemo, useState } from "react";
import { tasks, QuizTask, CodeTask, Task } from "./data";

const SCORE_PER_TASK = 10;

type FeedbackKind = "info" | "success" | "warning" | "danger";

type Feedback = {
  message: string;
  kind: FeedbackKind;
};

type TestResult = {
  name: string;
  ok: boolean;
  message: string;
};

type FilterType = "all" | "quiz" | "code";

const buildTestResults = (task: CodeTask, code: string): { results: TestResult[]; passed: boolean } => {
  const lines = code.split("\n");
  const hasReturn = lines.some((line) => line.trim().startsWith("return "));

  const results = task.tests.map((test, index) => {
    const ok = hasReturn;
    const message = hasReturn
      ? `Expected ${test.expected}, got ${test.expected}`
      : "No return statement found. Make sure your function returns a value.";
    return {
      name: `Test ${index + 1}`,
      ok,
      message
    };
  });

  return {
    results,
    passed: results.every((r) => r.ok)
  };
};

const initialCodeDrafts = tasks.reduce<Record<string, string>>((acc, task) => {
  if (task.type === "code") {
    acc[task.id] = task.starterCode;
  }
  return acc;
}, {});

const App = () => {
  const [currentId, setCurrentId] = useState(tasks[0].id);
  const [filter, setFilter] = useState<FilterType>("all");
  const [search, setSearch] = useState("");
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState<string[]>([]);
  const [quizChoices, setQuizChoices] = useState<Record<string, number>>({});
  const [codeDrafts, setCodeDrafts] = useState<Record<string, string>>(initialCodeDrafts);
  const [feedback, setFeedback] = useState<Feedback>({ message: "", kind: "info" });
  const [resultsByTask, setResultsByTask] = useState<Record<string, TestResult[]>>({});

  const stats = useMemo(() => {
    const quizCount = tasks.filter((t) => t.type === "quiz").length;
    const codeCount = tasks.filter((t) => t.type === "code").length;
    return { quizCount, codeCount };
  }, []);

  const filteredTasks = useMemo(() => {
    const term = search.trim().toLowerCase();
    return tasks.filter((task) => {
      const matchesFilter = filter === "all" || task.type === filter;
      const matchesSearch = !term || task.title.toLowerCase().includes(term);
      return matchesFilter && matchesSearch;
    });
  }, [filter, search]);

  useEffect(() => {
    if (!filteredTasks.find((task) => task.id === currentId)) {
      if (filteredTasks.length > 0) {
        setCurrentId(filteredTasks[0].id);
      }
    }
  }, [filteredTasks, currentId]);

  const task = tasks.find((t) => t.id === currentId) ?? tasks[0];
  const completedSet = useMemo(() => new Set(completed), [completed]);
  const completionRate = Math.round((completed.length / tasks.length) * 100);

  const markComplete = (taskId: string) => {
    if (completedSet.has(taskId)) return;
    const nextCompleted = [...completed, taskId];
    setCompleted(nextCompleted);
    setScore((prev) => prev + SCORE_PER_TASK);
  };

  const handleQuizCheck = (task: QuizTask) => {
    const choice = quizChoices[task.id] ?? -1;
    if (choice === -1) {
      setFeedback({ message: "Pick an option first.", kind: "warning" });
      return;
    }

    if (choice === task.correctIndex) {
      setFeedback({ message: `Correct! ${task.explanation}`, kind: "success" });
      markComplete(task.id);
    } else {
      setFeedback({ message: "Not quite. Try again.", kind: "danger" });
    }
  };

  const handleCodeCheck = (task: CodeTask) => {
    const code = codeDrafts[task.id] ?? task.starterCode;
    const outcome = buildTestResults(task, code);
    setResultsByTask((prev) => ({ ...prev, [task.id]: outcome.results }));

    if (outcome.passed) {
      setFeedback({ message: "Great job! All tests passed.", kind: "success" });
      markComplete(task.id);
    } else {
      setFeedback({ message: "Keep going, fix the failing tests.", kind: "warning" });
    }
  };

  const renderTaskBadge = (t: Task) => {
    if (t.type === "quiz") return "Quiz";
    return "Code";
  };

  return (
    <div className="page">
      <nav className="topbar">
        <div className="logo">
          <span className="logo-mark">PQ</span>
          <div>
            <div className="logo-title">Python Quest</div>
            <div className="logo-sub">Beginner Program</div>
          </div>
        </div>
        <div className="nav-actions">
          <button className="ghost">Curriculum</button>
          <button className="ghost">Challenges</button>
          <button className="ghost">Achievements</button>
          <button className="cta">Start Session</button>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <div className="eyebrow">Interactive Learning Studio</div>
          <h1>Level up your Python skills with guided missions, quizzes, and live feedback.</h1>
          <p>
            Python Quest is a structured training ground designed to help you master fundamentals through
            bite-sized missions. Track progress, practice with immediate feedback, and build confidence.
          </p>
          <div className="hero-actions">
            <button className="cta">Launch Challenge Studio</button>
            <button className="ghost">View Learning Path</button>
          </div>
          <div className="hero-stats">
            <div className="stat-card">
              <div className="stat-label">Total Challenges</div>
              <div className="stat-value">{tasks.length}</div>
              <div className="stat-meta">Quiz + Code missions</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Quiz Missions</div>
              <div className="stat-value">{stats.quizCount}</div>
              <div className="stat-meta">Concept checks</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Code Missions</div>
              <div className="stat-value">{stats.codeCount}</div>
              <div className="stat-meta">Hands-on practice</div>
            </div>
          </div>
        </div>
        <div className="hero-panel">
          <div className="panel-header">
            <div>
              <div className="panel-title">Learning Path</div>
              <div className="panel-sub">Guided progression</div>
            </div>
            <span className="pill">{completionRate}% Complete</span>
          </div>
          <div className="panel-body">
            {tasks.map((t, index) => (
              <div className={`path-row ${completedSet.has(t.id) ? "done" : ""}`} key={t.id}>
                <div className="path-index">{index + 1}</div>
                <div>
                  <div className="path-title">{t.title}</div>
                  <div className="path-meta">{renderTaskBadge(t)} Mission</div>
                </div>
                <div className="path-status">{completedSet.has(t.id) ? "Done" : "Up next"}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <div>
            <h2>Curriculum Blueprint</h2>
            <p>Structured milestones built for steady progression and confidence.</p>
          </div>
          <button className="ghost">Download Plan</button>
        </div>
        <div className="curriculum-grid">
          <div className="curriculum-card">
            <h3>Foundations</h3>
            <p>Variables, lists, functions, and flow control to anchor core knowledge.</p>
            <ul>
              <li>Mission-based learning path</li>
              <li>Instant quiz feedback</li>
              <li>Hands-on coding prompts</li>
            </ul>
          </div>
          <div className="curriculum-card">
            <h3>Practice Lab</h3>
            <p>Mini challenges focused on repetition, speed, and debugging confidence.</p>
            <ul>
              <li>Autograded challenges</li>
              <li>Progress tracking</li>
              <li>Skill badges</li>
            </ul>
          </div>
          <div className="curriculum-card">
            <h3>Momentum</h3>
            <p>Keep streaks, collect rewards, and unlock the next set of lessons.</p>
            <ul>
              <li>Daily missions</li>
              <li>Achievement snapshots</li>
              <li>Next step recommendations</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="studio" id="studio">
        <div className="studio-header">
          <div>
            <h2>Challenge Studio</h2>
            <p>Choose a mission, complete it, and track progress in real time.</p>
          </div>
          <div className="studio-controls">
            <div className="filter-group">
              <button className={filter === "all" ? "filter active" : "filter"} onClick={() => setFilter("all")}>All</button>
              <button className={filter === "quiz" ? "filter active" : "filter"} onClick={() => setFilter("quiz")}>Quizzes</button>
              <button className={filter === "code" ? "filter active" : "filter"} onClick={() => setFilter("code")}>Code Labs</button>
            </div>
            <input
              className="search"
              placeholder="Search missions"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
        </div>

        <div className="studio-grid">
          <div className="mission-list">
            {filteredTasks.map((t) => (
              <button
                key={t.id}
                className={`mission ${t.id === currentId ? "active" : ""}`}
                onClick={() => {
                  setCurrentId(t.id);
                  setFeedback({ message: "", kind: "info" });
                }}
              >
                <div className="mission-tag">{renderTaskBadge(t)}</div>
                <div>
                  <div className="mission-title">{t.title}</div>
                  <div className="mission-meta">{completedSet.has(t.id) ? "Completed" : "Pending"}</div>
                </div>
                <div className={`mission-status ${completedSet.has(t.id) ? "done" : ""}`}></div>
              </button>
            ))}
          </div>

          <div className="mission-work">
            <div className="work-header">
              <div>
                <span className="badge">{renderTaskBadge(task)}</span>
                <h3>{task.title}</h3>
                <p className="work-meta">Mission {tasks.findIndex((t) => t.id === task.id) + 1} of {tasks.length}</p>
              </div>
              <div className="score-chip">Score {score}</div>
            </div>

            {task.type === "quiz" ? (
              <div className="quiz-block">
                <p className="prompt">{task.question}</p>
                <div className="quiz-options">
                  {task.options.map((option, idx) => (
                    <label className={`option ${quizChoices[task.id] === idx ? "selected" : ""}`} key={option}>
                      <input
                        type="radio"
                        name={task.id}
                        value={idx}
                        checked={quizChoices[task.id] === idx}
                        onChange={() => setQuizChoices((prev) => ({ ...prev, [task.id]: idx }))}
                      />
                      <span>{option}</span>
                    </label>
                  ))}
                </div>
                <button className="cta" onClick={() => handleQuizCheck(task)}>Check Answer</button>
              </div>
            ) : (
              <div className="code-block">
                <p className="prompt">{task.prompt}</p>
                <textarea
                  className="code-area"
                  rows={14}
                  value={codeDrafts[task.id] ?? task.starterCode}
                  onChange={(event) =>
                    setCodeDrafts((prev) => ({ ...prev, [task.id]: event.target.value }))
                  }
                />
                <button className="cta" onClick={() => handleCodeCheck(task)}>Run Tests</button>
                {(resultsByTask[task.id] ?? []).length > 0 && (
                  <div className="results">
                    {(resultsByTask[task.id] ?? []).map((r) => (
                      <div className={`result-row ${r.ok ? "pass" : "fail"}`} key={r.name}>
                        <span className="result-status">{r.ok ? "PASS" : "FAIL"}</span>
                        <span className="result-name">{r.name}</span>
                        <span className="result-msg">{r.message}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {feedback.message && (
              <div className={`feedback ${feedback.kind}`}>{feedback.message}</div>
            )}
          </div>

          <div className="mission-side">
            <div className="side-card">
              <div className="side-title">Progress Snapshot</div>
              <div className="progress-ring">
                <div className="ring-value">{completionRate}%</div>
                <div className="ring-label">Complete</div>
              </div>
              <div className="side-meta">{completed.length} of {tasks.length} missions cleared.</div>
              <button className="ghost">View Achievements</button>
            </div>
            <div className="side-card">
              <div className="side-title">Next Suggested</div>
              <div className="next-title">{tasks.find((t) => !completedSet.has(t.id))?.title ?? "All done"}</div>
              <div className="next-meta">Focus on momentum and accuracy.</div>
              <button className="cta" onClick={() => {
                const next = tasks.find((t) => !completedSet.has(t.id));
                if (next) setCurrentId(next.id);
              }}>Open Next Mission</button>
            </div>
            <div className="side-card">
              <div className="side-title">Tips</div>
              <ul className="tips">
                <li>Use short, clear function names.</li>
                <li>Test with different inputs.</li>
                <li>Explain solutions out loud for memory.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div>
          <div className="footer-title">Python Quest</div>
          <div className="footer-sub">Your structured, modern Python learning path.</div>
        </div>
        <div className="footer-links">
          <span>Curriculum</span>
          <span>Challenges</span>
          <span>Support</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
