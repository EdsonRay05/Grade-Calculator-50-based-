import React, { useState } from 'react';

// Simple CSS-in-JS for layout and elements
const styles = {
  container: {
    maxWidth: '480px',
    margin: '40px auto',
    padding: '32px',
    background: '#f6f6f6',
    borderRadius: '10px',
    boxShadow: '0 2px 12px #ddd',
  },
  button: {
    margin: '10px 0',
    padding: '10px 22px',
    borderRadius: '5px',
    border: 'none',
    background: '#333',
    color: 'white',
    fontSize: '16px',
    cursor: 'pointer',
  },
  menuButton: {
    margin: '10px 0',
    padding: '8px 18px',
    borderRadius: '5px',
    border: 'none',
    background: '#1976d2',
    color: 'white',
    fontSize: '15px',
    cursor: 'pointer',
    width: '100%',
    textAlign: 'left',
  },
  input: {
    padding: '5px 12px',
    margin: '8px 0',
    fontSize: '15px',
    borderRadius: '4px',
    border: '1px solid #bbb',
    width: '100%',
  },
  label: {
    fontSize: '16px',
    marginBottom: '2px',
    display: 'block',
    fontWeight: 'bold',
  },
  section: {
    margin: '20px 0',
    padding: '18px',
    background: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 5px #eee',
  },
  result: {
    background: '#e3fcec',
    marginTop: '15px',
    padding: '15px',
    borderRadius: '8px',
    fontWeight: 'bold',
    color: '#126729',
  },
};

const round2 = (num) => Math.round(num * 100) / 100;

// Grading Scheme (50-based scale adjusted to 0-100)
function gradingScheme(grade) {
  const scaled = (grade - 50) * 2;
  if (scaled >= 94 && scaled <= 100) return 1.0;
  else if (scaled >= 88.5) return 1.25;
  else if (scaled >= 83) return 1.5;
  else if (scaled >= 77.5) return 1.75;
  else if (scaled >= 72) return 2.0;
  else if (scaled >= 65.5) return 2.25;
  else if (scaled >= 61) return 2.5;
  else if (scaled >= 55.5) return 2.75;
  else if (scaled >= 50) return 3.0;
  else return 5.0;
}

function PredictMajorExam() {
  const [desiredGrade, setDesiredGrade] = useState('');
  const [gradePeriod, setGradePeriod] = useState('Prelims');
  const [classStanding, setClassStanding] = useState('');
  const [prevGrade, setPrevGrade] = useState('');
  const [numQuestions, setNumQuestions] = useState('');
  const [result, setResult] = useState(null);

  React.useEffect(() => {
    if (
      !desiredGrade ||
      !classStanding ||
      !numQuestions ||
      (gradePeriod !== 'Prelims' && !prevGrade)
    ) {
      setResult(null);
      return;
    }
    const dg = parseFloat(desiredGrade);
    const cs = parseFloat(classStanding);
    const pg = parseFloat(prevGrade);
    const nq = parseInt(numQuestions, 10);

    let scoreNeeded = 0;

    if (gradePeriod === 'Prelims') {
      const prelimCS = cs * 0.5;
      const averageNeeded = dg - prelimCS;
      scoreNeeded = (averageNeeded / 0.5) * (nq / 100);
    } else if (gradePeriod === 'Midterms') {
      const midtermCS = cs * (1 / 3);
      const prelimG = pg * (1 / 3);
      const averageNeeded = dg - (midtermCS + prelimG);
      scoreNeeded = (averageNeeded / (1 / 3)) * (nq / 100);
    } else if (gradePeriod === 'Finals') {
      const finalCS = cs * (1 / 3);
      const midG = pg * (1 / 3);
      const averageNeeded = dg - (finalCS + midG);
      scoreNeeded = (averageNeeded / (1 / 3)) * (nq / 100);
    }
    setResult(`You need about ${round2(scoreNeeded)} out of ${nq} questions to reach grade ${dg}.`);
  }, [desiredGrade, classStanding, numQuestions, gradePeriod, prevGrade]);

  return (
    <div style={styles.section}>
      <h2>Predict Major Exam</h2>
      <label style={styles.label}>Desired Grade (50-100):</label>
      <input style={styles.input} type="number" value={desiredGrade} onChange={e => setDesiredGrade(e.target.value)} />
      <label style={styles.label}>Grade Period:</label>
      <select style={styles.input} value={gradePeriod} onChange={e => setGradePeriod(e.target.value)}>
        <option>Prelims</option>
        <option>Midterms</option>
        <option>Finals</option>
      </select>
      <label style={styles.label}>Class Standing % (0-100):</label>
      <input style={styles.input} type="number" value={classStanding} onChange={e => setClassStanding(e.target.value)} />
      {gradePeriod !== 'Prelims' && (
        <>
          <label style={styles.label}>Previous Grade (50-100):</label>
          <input style={styles.input} type="number" value={prevGrade} onChange={e => setPrevGrade(e.target.value)} />
        </>
      )}
      <label style={styles.label}>Number of Questions:</label>
      <input style={styles.input} type="number" value={numQuestions} onChange={e => setNumQuestions(e.target.value)} />
      {result && <div style={styles.result}>{result}</div>}
    </div>
  );
}

function CalculateOverallGrades() {
  const [gradeType, setGradeType] = useState('Preliminary');
  const [classStanding, setClassStanding] = useState('');
  const [examGrade, setExamGrade] = useState('');
  const [prevGrade, setPrevGrade] = useState('');
  const [result, setResult] = useState('');

  React.useEffect(() => {
    if (
      !classStanding ||
      !examGrade ||
      (gradeType !== 'Preliminary' && !prevGrade)
    ) {
      setResult('');
      return;
    }
    const cs = parseFloat(classStanding);
    const eg = parseFloat(examGrade);
    const pg = parseFloat(prevGrade);

    let rawGrade = 0;
    if (gradeType === 'Preliminary') {
      rawGrade = cs * 0.5 + eg * 0.5;
    } else if (gradeType === 'Mid-Term') {
      const partialMid = cs * 0.5 + eg * 0.5;
      rawGrade = partialMid * (2 / 3) + pg * (1 / 3);
    } else if (gradeType === 'Final') {
      const partialFinal = cs * 0.5 + eg * 0.5;
      rawGrade = partialFinal * (2 / 3) + pg * (1 / 3);
    }
    const adjustedGrade = (rawGrade / 2) + 50;
    const equivalent = gradingScheme(adjustedGrade);

    setResult(
      <div style={styles.result}>
        <div>Your {gradeType} grade: {round2(adjustedGrade)}</div>
        <div>Equivalent Grade: {equivalent.toFixed(2)}</div>
      </div>
    );
  }, [gradeType, classStanding, examGrade, prevGrade]);

  return (
    <div style={styles.section}>
      <h2>Calculate Overall Grades</h2>
      <label style={styles.label}>Grade Period:</label>
      <select style={styles.input} value={gradeType} onChange={e => setGradeType(e.target.value)}>
        <option>Preliminary</option>
        <option>Mid-Term</option>
        <option>Final</option>
      </select>
      <label style={styles.label}>Class Standing %:</label>
      <input style={styles.input} type="number" value={classStanding} onChange={e => setClassStanding(e.target.value)} />
      <label style={styles.label}>Exam Grade %:</label>
      <input style={styles.input} type="number" value={examGrade} onChange={e => setExamGrade(e.target.value)} />
      {(gradeType !== 'Preliminary') && (
        <>
          <label style={styles.label}>Previous Grade (50-100):</label>
          <input style={styles.input} type="number" value={prevGrade} onChange={e => setPrevGrade(e.target.value)} />
        </>
      )}
      {result}
    </div>
  );
}

function CalculateClassStanding() {
  const categories = ['quiz', 'assignment', 'seatwork', 'activity', 'laboratory', 'homework', 'recitation'];
  const [classStanding, setClassStanding] = useState(0);
  const [categoryIndex, setCategoryIndex] = useState(0);
  const [percentEquivalent, setPercentEquivalent] = useState('');
  const [numItems, setNumItems] = useState('');
  const [scores, setScores] = useState([]);
  const [result, setResult] = useState('');
  const [showForm, setShowForm] = useState(false);

  function handleStartCategory() {
    setShowForm(true);
    setPercentEquivalent('');
    setNumItems('');
    setScores([]);
    setResult('');
  }

  function handleScoresChange(idx, field, value) {
    const updated = scores.map((item, i) => (i === idx ? { ...item, [field]: value } : item));
    setScores(updated);
  }

  function handleNumItemsChange(val) {
    const n = parseInt(val, 10);
    setNumItems(n > 0 ? n : '');
    setScores(n > 0 ? Array(n).fill({ score: '', total: '' }) : []);
  }

  function calculateCategoryResult() {
    let totalPercent = 0;
    let valid = true;
    scores.forEach(({ score, total }) => {
      const s = parseFloat(score), t = parseFloat(total);
      if (isNaN(s) || isNaN(t) || s < 0 || t <= 0 || s > t) valid = false;
      totalPercent += (s / t) * 100;
    });
    if (!valid || scores.length === 0) {
      setResult('Please enter valid scores.');
      return;
    }
    const avgPercent = totalPercent / scores.length;
    const pe = parseFloat(percentEquivalent);
    if (isNaN(pe) || pe <= 0 || pe > 100) {
      setResult('Valid percent equivalent is 1-100.');
      return;
    }
    const finalCategoryScore = (avgPercent * pe) / 100;
    setResult(
      `Category "${categories[categoryIndex]}" average: ${round2(avgPercent)}%. Contribution: ${round2(finalCategoryScore)}%.`
    );
    setClassStanding(st => st + finalCategoryScore);
    setShowForm(false);
    setCategoryIndex(i => i + 1);
  }

  function reset() {
    setClassStanding(0);
    setCategoryIndex(0);
    setPercentEquivalent('');
    setNumItems('');
    setScores([]);
    setResult('');
    setShowForm(false);
  }

  return (
    <div style={styles.section}>
      <h2>Calculate Class Standing</h2>
      {!showForm && categoryIndex < categories.length && (
        <div>
          <b>Next: {categories[categoryIndex]}</b><br />
          <button style={styles.button} onClick={handleStartCategory}>Enter Data</button>
        </div>
      )}
      {!showForm && categoryIndex >= categories.length && (
        <div>
          <h3>Total Class Standing: {round2(classStanding)}%</h3>
          <button style={styles.button} onClick={reset}>Reset</button>
        </div>
      )}
      {showForm && (
        <div>
          <label style={styles.label}>Percent Equivalent:</label>
          <input style={styles.input} type="number" value={percentEquivalent} onChange={e => setPercentEquivalent(e.target.value)} />
          <label style={styles.label}>Number of Items:</label>
          <input style={styles.input} type="number" value={numItems} onChange={e => handleNumItemsChange(e.target.value)} />
          {scores.map((item, idx) => (
            <div key={idx}>
              <label style={styles.label}>Score {idx + 1}:</label>
              <input style={styles.input} type="number" value={item.score} onChange={e => handleScoresChange(idx, 'score', e.target.value)} />
              <label style={styles.label}>Total {idx + 1}:</label>
              <input style={styles.input} type="number" value={item.total} onChange={e => handleScoresChange(idx, 'total', e.target.value)} />
            </div>
          ))}
          <button style={styles.button} onClick={calculateCategoryResult}>Calculate Category</button>
          <button style={styles.button} onClick={() => { setShowForm(false); setCategoryIndex(idx => idx + 1); setResult(''); }}>Skip</button>
          {result && <div style={styles.result}>{result}</div>}
        </div>
      )}
    </div>
  );
}

function App() {
  const [page, setPage] = useState('menu');

  return (
    <div style={styles.container}>
      <h1 style={{ fontSize: '2.2rem', marginBottom: '14px' }}>Grade Calculator</h1>
      {page === 'menu' && (
        <>
          <button style={styles.menuButton} onClick={() => setPage('predict')}>[1] Predict Major Exam</button>
          <button style={styles.menuButton} onClick={() => setPage('overall')}>[2] Calculate Overall Grades</button>
          <button style={styles.menuButton} onClick={() => setPage('classStanding')}>[3] Calculate Class Standing</button>
        </>
      )}
      {page !== 'menu' && (
        <button style={styles.button} onClick={() => setPage('menu')}>← Back to Menu</button>
      )}
      {page === 'predict' && <PredictMajorExam />}
      {page === 'overall' && <CalculateOverallGrades />}
      {page === 'classStanding' && <CalculateClassStanding />}
    </div>
  );
}

export default App;
