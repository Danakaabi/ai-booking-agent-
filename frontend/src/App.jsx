import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    const trimmedMessage = message.trim()

    if (!trimmedMessage) {
      return
    }

    // API integration will be added in the next step.
  }

  return (
    <main className="app-shell">
      <section className="chat">
        <header className="chat-header">
          <div>
            <p className="eyebrow">AI Booking Agent</p>
            <h1>Booking Assistant</h1>
          </div>

          <span className="status">Ready</span>
        </header>

        <div className="chat-messages" aria-live="polite">
          <div className="empty-state">
            <h2>Start a conversation</h2>
            <p>
              Ask the assistant to book a service, check availability, or help
              you choose a time.
            </p>
          </div>
        </div>

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
            placeholder="Type your message..."
            autoComplete="off"
          />

          <button type="submit" disabled={!message.trim()}>
            Send
          </button>
        </form>
      </section>
    </main>
  )
}

export default App
