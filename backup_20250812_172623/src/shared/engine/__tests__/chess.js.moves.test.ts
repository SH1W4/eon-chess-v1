import { Chess } from 'chess.js';

describe('chess.js Move Validation Tests', () => {
    test('Test legal moves', () => {
        const game = new Chess();
        
        // Test e4
        const e4 = game.move({ from: 'e2', to: 'e4' });
        console.log('Move e4:', e4);
        console.log('FEN after e4:', game.fen());
        console.log('Is whites turn?', game.turn() === 'w');
        
        // Test Nf3
        const nf3 = game.move({ from: 'g1', to: 'f3' });
        console.log('Move Nf3:', nf3);
        console.log('FEN after Nf3:', game.fen());
        console.log('Legal moves:', game.moves({ verbose: true }));
    });
});
