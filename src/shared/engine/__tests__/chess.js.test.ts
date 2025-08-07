import { Chess } from 'chess.js';

describe('chess.js Behavior Tests', () => {
    test('Check and checkmate detection', () => {
        const game = new Chess();

        // Test fool's mate position (where black is in check)
        game.load('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
        
        console.log('\nFools mate position:');
        console.log('- isCheck:', game.isCheck());
        console.log('- isCheckmate:', game.isCheckmate());
        console.log('- isGameOver:', game.isGameOver());
        console.log('- Possible moves:', game.moves());

        // Test scholar's mate position (where black is in checkmate)
        game.load('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4');
        
        console.log('\nScholars mate position:');
        console.log('- isCheck:', game.isCheck());
        console.log('- isCheckmate:', game.isCheckmate());
        console.log('- isGameOver:', game.isGameOver());
        console.log('- Possible moves:', game.moves());
    });
});
