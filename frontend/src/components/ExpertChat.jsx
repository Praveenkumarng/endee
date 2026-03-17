import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const ExpertChat = ({ diseaseName }) => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Hello! I see your crop might have ${diseaseName}. What would you like to know about treating or managing it?` }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      // In production, configure API URL properly or use existing axios instance
      const response = await fetch('http://localhost:8000/ask-expert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          disease_name: diseaseName,
          question: userMsg
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer || "I'm sorry, I couldn't process that response." 
      }]);
    } catch (error) {
      console.error('Error fetching expert response:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Sorry, I'm having trouble connecting to the expert database right now. Please ensure the backend and Endee server are running." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!diseaseName || diseaseName === 'Healthy Leaf') {
    return null;
  }

  return (
    <Card className="h-full flex flex-col mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          Ask Expert AI (Powered by Endee DB)
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col flex-1 pb-4">
        {/* Chat window */}
        <div className="flex-1 overflow-y-auto min-h-[250px] max-h-[400px] mb-4 space-y-4 pr-2 custom-scrollbar">
          {messages.map((msg, idx) => (
            <div 
              key={idx} 
              className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`mt-1 p-2 rounded-full h-8 w-8 flex items-center justify-center shrink-0 ${
                msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'
              }`}>
                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className={`p-3 rounded-xl max-w-[80%] text-sm ${
                msg.role === 'user' 
                  ? 'bg-primary text-primary-foreground rounded-tr-none' 
                  : 'bg-secondary text-secondary-foreground rounded-tl-none whitespace-pre-line'
              }`}>
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-3">
              <div className="mt-1 p-2 rounded-full h-8 w-8 flex items-center justify-center shrink-0 bg-secondary text-secondary-foreground">
                <Bot size={16} />
              </div>
              <div className="p-3 rounded-xl bg-secondary text-secondary-foreground rounded-tl-none flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                <span className="text-sm text-muted-foreground">Searching Endee database...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <form onSubmit={handleSend} className="flex gap-2 mt-auto">
          <Input 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask about ${diseaseName}...`}
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ExpertChat;
