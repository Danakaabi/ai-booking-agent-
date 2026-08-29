const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

if (!API_BASE_URL) {
  throw new Error('VITE_API_BASE_URL is not configured')
}

export async function createConversation() {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to create conversation (${response.status})`)
  }

  return response.json()
}

export async function sendMessage(conversationId, content) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${encodeURIComponent(conversationId)}/messages`,
    {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        role: 'user',
        content,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(`Failed to send message (${response.status})`)
  }

  return response.json()
}

export async function getConversationMessages(conversationId) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${encodeURIComponent(conversationId)}/messages`,
    {
      headers: {
        Accept: 'application/json',
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      `Failed to load conversation messages (${response.status})`,
    )
  }

  return response.json()
}
