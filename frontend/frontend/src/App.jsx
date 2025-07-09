import { useState, useEffect } from 'react'
import { getProfile, login, logout, convertMeters } from './api'
import './index.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [meters, setMeters] = useState('')
  const [feet, setFeet] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProfile()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  const handleLogout = async () => {
    await logout()
    setUser(null)
    setFeet(null)
    setMeters('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setFeet(null)
    try {
      const data = await convertMeters(meters)
      setFeet(data.feet)
    } catch (err) {
      console.error("Fetch failed:", err)
      setError(err.message)
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="app-container">
      {user && (
        <header className="app-header">
          <h2>Meter to Feet Converter</h2>
          <div className="user-info">
            <img src={user.picture} alt="profile" />
            <div>
              <div className="welcome">Welcome!</div>
              <div className="user-name">{user.name}</div>
              <div className="user-email">{user.email}</div>
            </div>
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
          </div>
        </header>
      )}

      <main className="app-main">
        <div className="card">
          {!user ? (
            <>
              <h2>Conversion App</h2>
              <button className="login-btn" onClick={login}>Login with Google</button>
            </>
          ) : (
            <>
              <form onSubmit={handleSubmit}>
                <input
                  type="text"
                  value={meters}
                  onChange={(e) => setMeters(e.target.value)}
                  placeholder='e.g. "10 meters"'
                  required
                />
                <button type="submit">Convert</button>
              </form>
              {feet !== null && <p className="result">= {feet} feet</p>}
              {error && <p className="error">{error}</p>}
            </>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
