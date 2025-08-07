import React from 'react';

interface CircularMetricProps {
  value: number;
  threshold: number;
  label: string;
  colorClass: string;
  size?: string;
}

const CircularMetric: React.FC\u003cCircularMetricProps\u003e = ({
  value,
  threshold,
  label,
  colorClass,
  size = 'w-24 h-24',
}) => {
  // Calcula o ângulo do clip-path baseado no valor
  const angle = (value / 1) * 360;
  const clip = 100 - (value * 100);

  return (
    \u003cdiv className="bg-white p-6 rounded-lg shadow-lg"\u003e
      \u003ch3 className="text-xl font-bold text-gray-900 mb-4"\u003e{label}\u003c/h3\u003e
      \u003cdiv className="flex items-center justify-between"\u003e
        \u003cspan className="text-gray-600"\u003eLimite: {threshold}\u003c/span\u003e
        \u003cdiv className={`relative ${size}`}\u003e
          \u003cdiv className="absolute inset-0 flex items-center justify-center"\u003e
            \u003cspan className={`text-2xl font-bold text-${colorClass}`}\u003e
              {value.toFixed(2)}
            \u003c/span\u003e
          \u003c/div\u003e
          \u003cdiv className={`w-full h-full border-4 border-${colorClass}-200 rounded-full`}\u003e
            \u003cdiv 
              className={`h-full w-full border-4 border-${colorClass}-600 rounded-full`}
              style={{ 
                clipPath: `inset(${clip}% ${clip}% ${clip}% ${clip}% round 100%)`
              }}
            \u003e\u003c/div\u003e
          \u003c/div\u003e
        \u003c/div\u003e
      \u003c/div\u003e
    \u003c/div\u003e
  );
};

export default CircularMetric;
