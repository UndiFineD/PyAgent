import React, { useState } from 'react';
import { cn } from '../utils';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'calculator', title: 'Calculator', category: 'Utilities' };

export const Calculator: React.FC = () => {
  const [display, setDisplay] = useState('0');
  const [prevValue, setPrevValue] = useState<string | null>(null);
  const [operator, setOperator] = useState<string | null>(null);
  const [newNumber, setNewNumber] = useState(true);

  const handleNumber = (num: string) => {
    if (newNumber) {
      setDisplay(num);
      setNewNumber(false);
    } else {
      setDisplay(display === '0' ? num : display + num);
    }
  };

  const handleOperator = (op: string) => {
    setOperator(op);
    setPrevValue(display);
    setNewNumber(true);
  };

  const calculate = () => {
    if (!prevValue || !operator) return;
    const current = parseFloat(display);
    const previous = parseFloat(prevValue);
    let result = 0;

    switch (operator) {
      case '+': result = previous + current; break;
      case '-': result = previous - current; break;
      case '×': result = previous * current; break;
      case '÷': result = previous / current; break;
    }

    setDisplay(result.toString());
    setOperator(null);
    setPrevValue(null);
    setNewNumber(true);
  };

  const clear = () => {
    setDisplay('0');
    setPrevValue(null);
    setOperator(null);
    setNewNumber(true);
  };

  const btnClass = "h-12 rounded-lg font-medium text-lg transition-colors active:scale-95 flex items-center justify-center";
  const numClass = "bg-os-header text-os-text hover:brightness-110";
  const opClass = "bg-os-accent text-white hover:brightness-110";
  const fnClass = "bg-os-border text-os-text hover:brightness-110";

  return (
    <div className="h-full flex flex-col p-4 bg-os-bg gap-4">
      <div className="bg-os-window border border-os-border rounded-xl p-4 text-right text-3xl font-mono text-os-text overflow-hidden shadow-inner h-20 flex items-center justify-end">
        {display}
      </div>
      <div className="grid grid-cols-4 gap-3 flex-1">
        <button onClick={clear} className={cn(btnClass, fnClass, "col-span-3")}>AC</button>
        <button onClick={() => handleOperator('÷')} className={cn(btnClass, opClass)}>÷</button>
        
        {['7', '8', '9'].map(n => (
          <button key={n} onClick={() => handleNumber(n)} className={cn(btnClass, numClass)}>{n}</button>
        ))}
        <button onClick={() => handleOperator('×')} className={cn(btnClass, opClass)}>×</button>

        {['4', '5', '6'].map(n => (
          <button key={n} onClick={() => handleNumber(n)} className={cn(btnClass, numClass)}>{n}</button>
        ))}
        <button onClick={() => handleOperator('-')} className={cn(btnClass, opClass)}>-</button>

        {['1', '2', '3'].map(n => (
          <button key={n} onClick={() => handleNumber(n)} className={cn(btnClass, numClass)}>{n}</button>
        ))}
        <button onClick={() => handleOperator('+')} className={cn(btnClass, opClass)}>+</button>

        <button onClick={() => handleNumber('0')} className={cn(btnClass, numClass, "col-span-2")}>0</button>
        <button onClick={() => handleNumber('.')} className={cn(btnClass, numClass)}>.</button>
        <button onClick={calculate} className={cn(btnClass, opClass)}>=</button>
      </div>
    </div>
  );
};
