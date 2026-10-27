import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

const resourceOptions = ['Laptop', 'Internet', 'Books', 'Paid Courses', 'Free Courses', 'Mentor', 'None']
const constraintOptions = ['College', 'Job', 'Budget', 'Slow Internet', 'Family Responsibilities', 'None']
const intensityOptions = [
  'Low — 30 min/day',
  'Medium — 1 hour/day',
  'High — 2–3 hours/day',
  'Very High — 4+ hours/day',
]
const experienceOptions = ['Beginner', 'Intermediate', 'Advanced']
const planFields = [
  ['goal_summary', 'Your goal'],
  ['learning_path', 'Learning path'],
  ['weekly_roadmap', 'Four-week roadmap'],
  ['recommended_resources', 'Recommended resources'],
  ['practice_strategy', 'Practice strategy'],
  ['milestones', 'Milestones'],
  ['expected_outcome', 'Expected outcome'],
]
const checkpointStatuses = [
  ['not_started', 'Not started'],
  ['in_progress', 'In progress'],
  ['completed', 'Completed'],
]

function getErrorMessage(error) {
  const status = error?.response?.status
  const detail = error?.response?.data?.detail
  if (status === 429) {
    return 'The AI service is temporarily rate-limited. Wait a little before trying again; your saved roadmap is not deleted.'
  }
  if (status === 503) {
    return 'The AI service is temporarily unavailable. Please wait a moment and try again.'
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item.message || JSON.stringify(item)).join(' ')
  }
  if (typeof detail === 'string') return detail
  if (detail) return JSON.stringify(detail)
  if (!error?.response) {
    return 'Could not reach the Instincts AI backend. Start FastAPI in the backend folder and try again.'
  }
  return error?.response?.data?.message || error?.message || 'Something went wrong. Please try again.'
}

function planGoal(planData, fallback = '') {
  return fallback || planData?.goal || planData?.plan?.goal_summary || ''
}

async function fetchPlanContext(planData, goal) {
  if (!planData?.plan_id) return { checkpoints: [], resources: null, progress: null }
  const resolvedGoal = planGoal(planData, goal) || 'learning'
  const results = await Promise.allSettled([
    axios.get(`${API_URL}/api/checkpoints/${planData.plan_id}`),
    axios.get(`${API_URL}/api/resources`, { params: { goal: resolvedGoal } }),
    axios.get(`${API_URL}/api/solution-progress/${planData.plan_id}`),
  ])
  return {
    checkpoints: results[0].status === 'fulfilled' && Array.isArray(results[0].value.data)
      ? results[0].value.data : [],
    resources: results[1].status === 'fulfilled' ? results[1].value.data : null,
    progress: results[2].status === 'fulfilled' ? results[2].value.data : null,
  }
}

function resourceHref(resource) {
  const value = String(resource || '').trim()
  if (/^https?:\/\//i.test(value)) return value
  const match = value.match(/(?:www\.)?(?:[a-z0-9-]+\.)+[a-z]{2,}(?:\/[a-z0-9_./?=&%#-]*)?/i)
  if (match) return `https://${match[0].replace(/[.,;:!?]+$/, '')}`
  return `https://www.google.com/search?q=${encodeURIComponent(value)}`
}

function formatDate(value) {
  if (!value) return 'Time unavailable'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString()
}

function prettyLabel(value) {
  return String(value || '').replaceAll('_', ' ').replace(/^./, (character) => character.toUpperCase())
}

// Render the Markdown subset returned by the plan API without adding a dependency.
function renderPlanContent(value) {
  const normalized = String(value || '')
    .replace(/\\([#*+-])/g, '$1')
    .replace(/\\-/g, '-')
    .replace(/\r\n/g, '\n')
    .trim()
  if (!normalized) return null

  const lines = normalized.split('\n')
  const blocks = []
  let paragraph = []
  let listItems = []
  let blockIndex = 0

  const flushParagraph = () => {
    if (!paragraph.length) return
    blocks.push(<p key={`p-${blockIndex++}`}>{paragraph.join(' ')}</p>)
    paragraph = []
  }
  const flushList = () => {
    if (!listItems.length) return
    blocks.push(
      <ul key={`ul-${blockIndex++}`}>
        {listItems.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}
      </ul>,
    )
    listItems = []
  }

  lines.forEach((line) => {
    const text = line.trim()
    if (!text) {
      flushParagraph()
      flushList()
      return
    }
    const heading = text.match(/^#{1,4}\s+(.+)$/)
    if (heading) {
      flushParagraph()
      flushList()
      blocks.push(<h4 key={`h-${blockIndex++}`}>{heading[1]}</h4>)
      return
    }
    const bullet = text.match(/^[-*+]\s+(.+)$/)
    if (bullet) {
      flushParagraph()
      listItems.push(bullet[1])
      return
    }
    flushList()
    paragraph.push(text)
  })
  flushParagraph()
  flushList()
  return <div className="plan-content">{blocks}</div>
}

function App() {
  const [form, setForm] = useState({
    goal: '',
    resources: [],
    intensity: intensityOptions[1],
    constraints: [],
    experience: experienceOptions[0],
  })
  const [planData, setPlanData] = useState(null)
  const [checkpoints, setCheckpoints] = useState([])
  const [resourceData, setResourceData] = useState(null)
  const [resourceTopic, setResourceTopic] = useState('')
  const [progress, setProgress] = useState(null)
  const [topic, setTopic] = useState('')
  const [task, setTask] = useState('')
  const [solution, setSolution] = useState('')
  const [evaluation, setEvaluation] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [submittingPlan, setSubmittingPlan] = useState(false)
  const [submittingSolution, setSubmittingSolution] = useState(false)
  const [loadingResources, setLoadingResources] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [updatingCheckpoint, setUpdatingCheckpoint] = useState(null)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  useEffect(() => {
    let active = true
    async function loadLatestPlan() {
      try {
        const response = await axios.get(`${API_URL}/api/latest-plan`)
        if (!active || !response.data) return
        const savedGoal = window.localStorage.getItem('instincts_ai_goal') || response.data.goal || response.data.plan?.goal_summary || ''
        const restoredPlan = { ...response.data, goal: savedGoal }
        setPlanData(restoredPlan)
        setForm((current) => ({ ...current, goal: savedGoal }))
        // Keep this blank so resource searches can focus on a specific concept.
        setResourceTopic('')
        const context = await fetchPlanContext(restoredPlan, savedGoal)
        if (!active) return
        setCheckpoints(context.checkpoints)
        setResourceData(context.resources)
        setProgress(context.progress)
      } catch (requestError) {
        if (active && requestError?.response?.status !== 404) setError(getErrorMessage(requestError))
      } finally {
        if (active) setLoading(false)
      }
    }
    loadLatestPlan()
    return () => { active = false }
  }, [])

  function updateForm(event) {
    const { name, value, checked, type } = event.target
    if (type === 'checkbox') {
      setForm((current) => {
        const selected = current[name]
        let next
        if (value === 'None') next = checked ? ['None'] : []
        else next = checked
          ? [...selected.filter((item) => item !== 'None'), value]
          : selected.filter((item) => item !== value)
        return { ...current, [name]: next }
      })
      return
    }
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmitPlan(event) {
    event.preventDefault()
    setSubmittingPlan(true)
    setError('')
    setNotice('')
    try {
      const payload = {
        ...form,
        resources: form.resources.length ? form.resources : ['None'],
        constraints: form.constraints.length ? form.constraints : ['None'],
      }
      const response = await axios.post(`${API_URL}/api/generate-plan`, payload)
      const createdPlan = { ...response.data, goal: form.goal }
      setPlanData(createdPlan)
      window.localStorage.setItem('instincts_ai_goal', form.goal)
      setResourceTopic('')
      setTopic('')
      setTask('')
      setSolution('')
      setEvaluation(null)
      setHistory([])
      const context = await fetchPlanContext(createdPlan, form.goal)
      setCheckpoints(context.checkpoints)
      setResourceData(context.resources)
      setProgress(context.progress)
      setNotice('Your roadmap is saved. Choose a resource, practice a task, and track your own progress.')
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmittingPlan(false)
    }
  }

  async function updateCheckpoint(checkpointId, status) {
    setError('')
    setNotice('')
    setUpdatingCheckpoint(checkpointId)
    try {
      const response = await axios.patch(`${API_URL}/api/checkpoints/${checkpointId}`, { status })
      setCheckpoints((current) => current.map((checkpoint) => checkpoint.id === checkpointId
        ? { ...checkpoint, status: response.data.status }
        : checkpoint))
      setNotice('Checkpoint status saved.')
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setUpdatingCheckpoint(null)
    }
  }

  async function refreshResources(event) {
    event.preventDefault()
    setError('')
    setLoadingResources(true)
    try {
      const goal = planGoal(planData, form.goal) || 'learning'
      const params = { goal }
      if (resourceTopic.trim()) params.topic = resourceTopic.trim()
      const response = await axios.get(`${API_URL}/api/resources`, { params })
      setResourceData(response.data)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setLoadingResources(false)
    }
  }

  async function refreshHistory(planId, selectedTopic) {
    if (!planId || !selectedTopic.trim()) return
    setLoadingHistory(true)
    try {
      const response = await axios.get(`${API_URL}/api/solution-history/${planId}`, {
        params: { topic: selectedTopic.trim() },
      })
      setHistory(Array.isArray(response.data) ? response.data : [])
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setLoadingHistory(false)
    }
  }

  async function loadHistory() {
    setError('')
    await refreshHistory(planData?.plan_id, topic)
  }

  async function submitSolution(event) {
    event.preventDefault()
    if (!planData?.plan_id) {
      setError('Generate a learning roadmap before submitting a practice attempt.')
      return
    }
    setError('')
    setNotice('')
    setSubmittingSolution(true)
    try {
      const response = await axios.post(`${API_URL}/api/evaluate-solution`, {
        plan_id: planData.plan_id,
        topic: topic.trim(),
        task: task.trim(),
        solution: solution.trim(),
      })
      setEvaluation(response.data)
      const [historyResult, progressResult] = await Promise.allSettled([
        axios.get(`${API_URL}/api/solution-history/${planData.plan_id}`, { params: { topic: topic.trim() } }),
        axios.get(`${API_URL}/api/solution-progress/${planData.plan_id}`),
      ])
      if (historyResult.status === 'fulfilled') setHistory(historyResult.value.data)
      if (progressResult.status === 'fulfilled') setProgress(progressResult.value.data)
      setNotice('Attempt saved. Review the feedback, improve your own solution, and submit again when ready.')
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmittingSolution(false)
    }
  }

  function startNewPlan() {
    setPlanData(null)
    setCheckpoints([])
    setResourceData(null)
    setProgress(null)
    setEvaluation(null)
    setHistory([])
    setResourceTopic('')
    setTopic('')
    setTask('')
    setSolution('')
    setError('')
    setNotice('')
  }

  const searchTopic = resourceTopic.trim() || planData?.grounded_domain || planGoal(planData, form.goal) || 'learning resources'
  const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(`${searchTopic} tutorial` )}`
  const summarySearchUrl = `https://www.google.com/search?q=${encodeURIComponent(`${searchTopic} learning summary`)}`

  if (loading) {
    return <main className="shell"><p className="loading">Connecting to your learning space…</p></main>
  }

  return (
    <main className="shell">
      <header className="site-header">
        <a className="brand" href="#top" aria-label="Instincts AI home">
          <img src="/favicon.svg" alt="" className="brand-mark" />
          <span>INSTINCTS <strong>AI</strong></span>
        </a>
        <span className="header-note">A learning companion built around your effort</span>
      </header>

      <section className="hero" id="top">
        <p className="eyebrow">PERSONALIZED LEARNING, WITHOUT SPOON-FEEDING</p>
        <h1>Make your effort<br /><em>move you forward.</em></h1>
        <p className="intro">Build a roadmap around your goals, learn from trusted resources, and see your understanding improve one attempt at a time.</p>
        <div className="feature-strip">
          <span><b>01</b> Personal roadmap</span>
          <span><b>02</b> Guided practice</span>
          <span><b>03</b> Progress by mastery</span>
        </div>
      </section>

      {error && <div className="alert alert-error" role="alert"><strong>Something needs attention</strong><span>{error}</span></div>}
      {notice && <div className="alert alert-success" role="status">{notice}</div>}

      {!planData ? (
        <section className="surface profile-surface">
          <div className="section-heading">
            <p className="eyebrow">START WITH YOUR CONTEXT</p>
            <h2>Build your <em>learning roadmap.</em></h2>
            <p>Tell Instincts AI what you want to achieve and what your current situation allows.</p>
          </div>
          <form className="plan-form" onSubmit={handleSubmitPlan}>
            <label className="field"><span>What do you want to learn?</span><textarea name="goal" value={form.goal} onChange={updateForm} placeholder="For example: learn Python for data analysis or prepare for DSA interviews…" minLength={2} maxLength={300} required /></label>
            <fieldset><legend>Resources you can use</legend><p className="field-help">Select everything available to you, or choose None.</p><div className="options">{resourceOptions.map((option) => <label className="option" key={option}><input type="checkbox" name="resources" value={option} checked={form.resources.includes(option)} onChange={updateForm} /><span>{option}</span></label>)}</div></fieldset>
            <div className="form-row">
              <label className="field"><span>Study intensity</span><select name="intensity" value={form.intensity} onChange={updateForm}>{intensityOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
              <label className="field"><span>Current experience</span><select name="experience" value={form.experience} onChange={updateForm}>{experienceOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
            </div>
            <fieldset><legend>Constraints to plan around</legend><p className="field-help">These help the roadmap fit your real schedule and resources.</p><div className="options">{constraintOptions.map((option) => <label className="option" key={option}><input type="checkbox" name="constraints" value={option} checked={form.constraints.includes(option)} onChange={updateForm} /><span>{option}</span></label>)}</div></fieldset>
            <button className="button button-primary" type="submit" disabled={submittingPlan}>{submittingPlan ? 'Building your roadmap…' : 'Build my learning roadmap'} <span aria-hidden="true">→</span></button>
          </form>
        </section>
      ) : (
        <div className="workspace">
          <section className="surface roadmap-surface">
            <div className="section-heading section-heading-row">
              <div><p className="eyebrow">YOUR ROADMAP</p><h2>One clear next step<br /><em>at a time.</em></h2></div>
              <button type="button" className="button button-secondary" onClick={startNewPlan}>New roadmap</button>
            </div>
            {planData.profile_vector && <div className="profile-metrics" aria-label="Computed learning profile values">
              {Object.entries(planData.profile_vector).map(([key, value]) => <div className="metric" key={key}><span>{prettyLabel(key)}</span><strong>{Number(value).toFixed(2)}</strong><div className="metric-track"><span style={{ width: `${Math.max(0, Math.min(1, Number(value))) * 100}%` }} /></div></div>)}
            </div>}
            {planData.grounded_domain && <p className="domain-note">Resource domain matched: <strong>{prettyLabel(planData.grounded_domain)}</strong></p>}
            <div className="plan-sections">{planFields.map(([field, label]) => <section className="plan-section" key={field}><h3>{label}</h3>{renderPlanContent(planData.plan?.[field] || 'This section was not returned for the current plan.')}</section>)}</div>
            <section className="checkpoints">
              <div className="section-heading"><p className="eyebrow">SMALL STEPS ADD UP</p><h3>Roadmap checkpoints</h3><p>Mark milestones based on your own work.</p></div>
              {checkpoints.length === 0 ? <p className="empty-state">No milestones were returned for this plan.</p> : checkpoints.map((checkpoint) => <div className="checkpoint" key={checkpoint.id}>
                <p>{checkpoint.text}</p><div className="status-options" role="group" aria-label={`Status for ${checkpoint.text}`}>
                  {checkpointStatuses.map(([status, label]) => <label key={status} className={checkpoint.status === status ? 'selected' : ''}><input type="radio" name={`checkpoint-${checkpoint.id}`} value={status} checked={checkpoint.status === status} disabled={updatingCheckpoint === checkpoint.id} onChange={() => updateCheckpoint(checkpoint.id, status)} /><span>{label}</span></label>)}
                </div>
              </div>)}
            </section>
          </section>

          <section className="surface resources-surface">
            <div className="section-heading"><p className="eyebrow">LEARN FROM THE RIGHT SOURCES</p><h2>Guided <em>practice.</em></h2><p>Choose a concept you are studying. Instincts AI points you to resources; you remain responsible for the learning.</p></div>
            <form className="resource-search" onSubmit={refreshResources}>
              <label className="field"><span>Topic or related concept</span><input value={resourceTopic} onChange={(event) => setResourceTopic(event.target.value)} placeholder="For example: Power BI dashboards or SQL joins" maxLength={200} /></label>
              <button type="submit" className="button button-secondary" disabled={loadingResources}>{loadingResources ? 'Finding resources…' : 'Find resources'}</button>
            </form>
            {resourceData ? <div className="resource-results">
              {resourceData.domain && <p className="resource-domain">Curated category: <strong>{prettyLabel(resourceData.domain)}</strong></p>}
              {!resourceData.grounded && <p className="field-help">{resourceData.note || 'These search links are suggestions, not verified curated resources.'}</p>}
              {Array.isArray(resourceData.resources) && resourceData.resources.length > 0 ? <ul className="resource-list">{resourceData.resources.map((item, index) => <li key={`${item}-${index}`}><a href={resourceHref(item)} target="_blank" rel="noreferrer">{item}<span aria-hidden="true"> ↗</span></a></li>)}</ul> : <p className="empty-state">No curated resources matched. Use the search links below to explore this topic.</p>}
              <div className="search-links">
                <a className="resource-link-card" href={youtubeSearchUrl} target="_blank" rel="noreferrer"><span className="resource-link-icon">▶</span><span><strong>YouTube tutorials</strong><small>Search {searchTopic} tutorials.</small></span><span aria-hidden="true">↗</span></a>
                <a className="resource-link-card" href={summarySearchUrl} target="_blank" rel="noreferrer"><span className="resource-link-icon">≡</span><span><strong>Topic summaries</strong><small>Review key ideas about {searchTopic}.</small></span><span aria-hidden="true">↗</span></a>
              </div>
            </div> : <p className="empty-state">Resource suggestions will appear here when available.</p>}
          </section>

          <section className="surface practice-surface">
            <div className="section-heading"><p className="eyebrow">YOUR WORK, YOUR PROGRESS</p><h2>Practice and <em>improve.</em></h2><p>Take a task from the resource you are studying, write your own attempt, and review feedback. Instincts AI does not generate the exercise for you.</p></div>
            <form className="practice-form" onSubmit={submitSolution}>
              <label className="field"><span>Topic</span><input value={topic} onChange={(event) => setTopic(event.target.value)} placeholder="For example: SQL joins" maxLength={200} required /></label>
              <label className="field"><span>Practice task or question</span><textarea value={task} onChange={(event) => setTask(event.target.value)} placeholder="Paste or summarize the task you chose from your learning resource…" maxLength={4000} required /></label>
              <label className="field"><span>Your solution or explanation</span><textarea className="solution-input" value={solution} onChange={(event) => setSolution(event.target.value)} placeholder="Write what you understand so far. Partial attempts are welcome…" maxLength={20000} required /></label>
              <div className="practice-actions"><button type="submit" className="button button-primary" disabled={submittingSolution}>{submittingSolution ? 'Reviewing your attempt…' : 'Evaluate my attempt'} <span aria-hidden="true">→</span></button><button type="button" className="text-button" onClick={loadHistory} disabled={!topic.trim() || loadingHistory}>{loadingHistory ? 'Loading history…' : 'Load previous attempts'}</button></div>
            </form>
            {evaluation && <div className="evaluation-card" aria-live="polite">
              <div className="evaluation-topline"><div><p className="eyebrow">LATEST EVALUATION</p><h3>{evaluation.mastered ? 'Topic mastered' : 'Keep building your understanding'}</h3></div><div className="score-circle"><strong>{evaluation.percentage ?? Math.round(Number(evaluation.score) * 100)}%</strong><span>correctness estimate</span></div></div>
              <div className="score-track"><span style={{ width: `${Math.max(0, Math.min(100, Number(evaluation.percentage ?? Number(evaluation.score) * 100)))}%` }} /></div>
              <p className="feedback-text">{evaluation.feedback}</p>
              <div className="attempt-stats"><span>Attempt <strong>{evaluation.attempt_count}</strong></span><span>Best score <strong>{Math.round(Number(evaluation.best_score) * 100)}%</strong></span><span>Score <strong>{Number(evaluation.score).toFixed(2)} / 1.00</strong></span></div>
              <p className="field-help">Scores are AI-generated estimates, not a guarantee of objective correctness. Use the feedback to make your own next revision.</p>
            </div>}
            <div className="history-section">
              <div className="section-heading compact-heading"><p className="eyebrow">YOUR REVISIONS</p><h3>Attempt history</h3></div>
              {history.length === 0 ? <p className="empty-state">After you submit an attempt, your saved revisions for this topic will appear here.</p> : <div className="history-list">{history.map((attempt, index) => <details className="history-item" key={attempt.submission_id || `${attempt.created_at}-${index}`}>
                <summary><span>Attempt {index + 1}</span><strong>{attempt.percentage ?? Math.round(Number(attempt.score) * 100)}%</strong><small>{formatDate(attempt.created_at)}</small></summary>
                <div className="history-detail"><p><strong>Your answer</strong></p><p className="preserve-lines">{attempt.solution}</p><p><strong>Feedback</strong></p><p>{attempt.feedback}</p></div>
              </details>)}</div>}
            </div>
          </section>

          <section className="surface progress-surface">
            <div className="section-heading"><p className="eyebrow">PROGRESS THAT MEANS SOMETHING</p><h2>Mastery, not just <em>activity.</em></h2><p>Progress reflects your strongest understanding of each topic, not simply how many submissions you make.</p></div>
            {progress ? <>
              <div className="progress-summary"><div className="progress-stat"><strong>{progress.total_topics_attempted ?? 0}</strong><span>Topics attempted</span></div><div className="progress-stat"><strong>{progress.total_solution_attempts ?? 0}</strong><span>Solutions submitted</span></div><div className="progress-stat"><strong>{progress.mastered_topics ?? 0}</strong><span>Topics mastered</span></div></div>
              {progress.topics?.length ? <div className="topic-progress-list">{progress.topics.map((item) => <article className="topic-progress" key={item.topic}>
                <div className="topic-progress-heading"><div><h3>{item.topic}</h3><p>{item.attempt_count} {item.attempt_count === 1 ? 'attempt' : 'attempts'} · latest {Math.round(Number(item.latest_score) * 100)}%</p></div><span className={`mastery-tag ${item.mastered ? 'mastery-tag-done' : ''}`}>{item.mastered ? 'Mastered' : 'In progress'}</span></div>
                <div className="score-track"><span style={{ width: `${Math.max(0, Math.min(100, Number(item.best_score) * 100))}%` }} /></div><p className="field-help">Best score: {Math.round(Number(item.best_score) * 100)}% · Last attempt: {formatDate(item.last_attempt_at)}</p>
              </article>)}</div> : <p className="empty-state">No solution attempts have been recorded for this roadmap yet.</p>}
            </> : <p className="empty-state">Submit your first practice attempt to start building your mastery record.</p>}
          </section>
        </div>
      )}
      <footer className="site-footer"><span>INSTINCTS AI</span><p>Your effort compounds when it's directed well.</p></footer>
    </main>
  )
}

export default App
