import React, { useState } from 'react';

interface SelectProps {
  value?: string;
  onValueChange?: (value: string) => void;
  children: React.ReactNode;
}

interface SelectTriggerProps {
  children: React.ReactNode;
  className?: string;
}

interface SelectValueProps {
  placeholder?: string;
}

interface SelectContentProps {
  children: React.ReactNode;
  className?: string;
}

interface SelectItemProps {
  value: string;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Select({ value, onValueChange, children }: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            isOpen,
            setIsOpen,
            value,
            onValueChange
          } as any);
        }
        return child;
      })}
    </div>
  );
}

export function SelectTrigger({ children, className = '', isOpen, setIsOpen }: SelectTriggerProps & any) {
  return (
    <button
      type="button"
      onClick={() => setIsOpen?.(!isOpen)}
      className={`flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
    >
      {children}
      <svg className="h-4 w-4 opacity-50" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="m6 9 6 6 6-6" />
      </svg>
    </button>
  );
}

export function SelectValue({ placeholder }: SelectValueProps) {
  return <span className="text-gray-900">{placeholder || 'Select...'}</span>;
}

export function SelectContent({ children, className = '' }: SelectContentProps) {
  return (
    <div className={`absolute top-full z-50 mt-1 min-w-[200px] bg-white border border-gray-200 rounded-md shadow-lg ${className}`}>
      {children}
    </div>
  );
}

export function SelectItem({ value, children, onClick }: SelectItemProps) {
  return (
    <div
      onClick={onClick}
      className="px-3 py-2 text-sm cursor-pointer hover:bg-gray-100 focus:bg-gray-100"
    >
      {children}
    </div>
  );
}
