
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MicroInteractionProps {
  children: React.ReactNode;
  type?: 'hover' | 'click' | 'focus';
  delay?: number;
}

export const MicroInteraction: React.FC<MicroInteractionProps> = ({ 
  children, 
  type = 'hover',
  delay = 0.1 
}) => {
  const [isActive, setIsActive] = useState(false);
  
  const variants = {
    initial: { scale: 1, rotate: 0 },
    hover: { scale: 1.05, rotate: 2 },
    click: { scale: 0.95, rotate: -1 },
    focus: { scale: 1.02, rotate: 0 }
  };
  
  return (
    <motion.div
      initial="initial"
      animate={isActive ? type : "initial"}
      variants={variants}
      transition={{ duration: delay, ease: "easeInOut" }}
      onHoverStart={() => type === 'hover' && setIsActive(true)}
      onHoverEnd={() => type === 'hover' && setIsActive(false)}
      onTapStart={() => type === 'click' && setIsActive(true)}
      onTapEnd={() => type === 'click' && setIsActive(false)}
      onFocus={() => type === 'focus' && setIsActive(true)}
      onBlur={() => type === 'focus' && setIsActive(false)}
    >
      {children}
    </motion.div>
  );
};

export const ChessPieceAnimation: React.FC<{ 
  children: React.ReactNode;
  isMoving: boolean;
}> = ({ children, isMoving }) => {
  return (
    <AnimatePresence>
      {isMoving && (
        <motion.div
          initial={{ scale: 1, y: 0 }}
          animate={{ scale: 1.1, y: -10 }}
          exit={{ scale: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
};
