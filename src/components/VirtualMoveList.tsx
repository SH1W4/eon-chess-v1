
import React from 'react';
import { FixedSizeList as List } from 'react-window';

interface Move {
  san: string;
  color: 'w' | 'b';
  piece: string;
}

interface VirtualMoveListProps {
  moves: Move[];
}

export const VirtualMoveList: React.FC<VirtualMoveListProps> = ({ moves }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => {
    const moveIndex = index * 2;
    const whiteMove = moves[moveIndex];
    const blackMove = moves[moveIndex + 1];
    
    return (
      <div style={style} className="move-row flex items-center p-2 border-b border-gray-200">
        <span className="move-number w-8 text-gray-500">{index + 1}.</span>
        <span className="move-white flex-1 px-2">{whiteMove?.san || ''}</span>
        <span className="move-black flex-1 px-2">{blackMove?.san || ''}</span>
      </div>
    );
  };
  
  return (
    <List
      height={400}
      itemCount={Math.ceil(moves.length / 2)}
      itemSize={40}
      width="100%"
      className="border border-gray-300 rounded"
    >
      {Row}
    </List>
  );
};
