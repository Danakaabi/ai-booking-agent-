import { useState } from 'react'
import './App.css'

const quickActions = [
  {
    label: 'Book an appointment',
    message: 'I want to book an appointment',
  },
  {
    label: 'Check availability',
    message: 'Show me the available times',
  },
  {
    label: 'View services',
    message: 'What services are available?',
  },
  {
    label: 'Find staff',
    message: 'Show me the available staff',
  },
]

function App() {
  const [message, setMessage] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage) {
      return
    }

    // Backend conversation integration will be connected later.
  }

  function handleQuickAction(selectedMessage) {
    setMessage(selectedMessage)
  }

  return (
    <main className="app-shell">
      <section className="chat">
        <header className="chat-header">
          <div className="agent-identity">
            <div className="agent-avatar" aria-hidden="true">
              AI
            </div>

            <div>
              <p className="eyebrow">AI Booking Agent</p>
              <h1>Booking Assistant</h1>
              <p className="agent-description">
                Intelligent scheduling assistant
              </p>
            </div>
          </div>

          <span className="status">Online</span>
        </header>

        <div className="chat-messages" aria-live="polite">
          <div className="welcome-state">
            <div className="welcome-icon" aria-hidden="true">
              ✦
            </div>

            <p className="welcome-label">AI BOOKING ASSISTANT</p>

            <h2>How can I help you today?</h2>

            <p className="welcome-description">
              Book an appointment, explore services, check available times,
              or find the right staff member through a simple conversation.
            </p>

            <div className="quick-actions" aria-label="Quick actions">
              {quickActions.map((action) => (
                <button
                  key={action.label}
                  type="button"
                  className="quick-action"
                  onClick={() => handleQuickAction(action.message)}
                >
                  <span>{action.label}</span>
                  <span className="quick-action-arrow" aria-hidden="true">
                    →
                  </span>
                </button>
              ))}
            </div>

            <div className="capabilities">
              <span>Booking</span>
              <span>Availability</span>
              <span>Services</span>
              <span>Staff</span>
            </div>
          </div>
        </div>

        <div className="composer-area">
          <form className="message-composer" onSubmit={handleSubmit}>
            <label className="sr-only" htmlFor="message">
              Message
            </label>

            <input
              id="message"
              name="message"
              type="text"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Ask about a booking..."
              autoComplete="off"
            />

            <button type="submit" disabled={!message.trim()}>
              <span>Send</span>
              <span aria-hidden="true">↑</span>
            </button>
          </form>

          <p className="composer-hint">
            AI responses will be validated by the booking system.
          </p>
        </div>
      </section>
    </main>
  )
}

export default App
