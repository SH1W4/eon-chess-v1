import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700">
      <div className="container mx-auto px-4 py-8">
        {children}
      </div>
    </div>
  );
};

export const MemoizedLayout = React.memo(Layout);
