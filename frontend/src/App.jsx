import { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    const updatedMessages = [...messages, { role: 'user', content: input }];

    setMessages(updatedMessages);

    const res = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: updatedMessages }),
    });

    const data = await res.json();
    setResponse(data.reply);
    setMessages([...updatedMessages, { role: 'assistant', content: data.reply }]);
    setInput('');
  };

  return (
    <div>
      <h1>FortuneAI Chat</h1>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleSubmit}>Send</button>
      <div>
        <h3>Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
