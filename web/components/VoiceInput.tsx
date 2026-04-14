import React, { useCallback, useRef, useState } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { cn } from '../utils';

interface VoiceInputProps {
  onTranscript: (transcript: string, isFinal: boolean) => void;
}

export const VoiceInput: React.FC<VoiceInputProps> = ({ onTranscript }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  const startListening = useCallback(() => {
    const SpeechRecognitionAPI =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognitionAPI) {
      console.warn('Web Speech API not supported in this browser');
      return;
    }
    const recognition: any = new SpeechRecognitionAPI();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event: any) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          onTranscript(result[0].transcript, true);
        } else {
          interim += result[0].transcript;
        }
      }
      if (interim) onTranscript(interim, false);
    };

    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);

    recognition.start();
    recognitionRef.current = recognition;
    setIsListening(true);
  }, [onTranscript]);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    setIsListening(false);
  }, []);

  return (
    <button
      onMouseDown={startListening}
      onMouseUp={stopListening}
      onTouchStart={startListening}
      onTouchEnd={stopListening}
      className={cn(
        'p-2 rounded-lg transition-all duration-200 border',
        isListening
          ? 'bg-red-500 text-white border-red-600 animate-pulse'
          : 'bg-os-window text-os-text border-os-border hover:bg-os-border'
      )}
      title="Hold to speak"
      aria-label={isListening ? 'Listening…' : 'Push to talk'}
    >
      {isListening ? <Mic size={18} /> : <MicOff size={18} />}
    </button>
  );
};
