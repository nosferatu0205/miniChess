import Bishop from '../pieces/bishop.js';
import King from '../pieces/king.js';
import Knight from '../pieces/knight.js';
import Pawn from '../pieces/pawn.js';
import Queen from '../pieces/queen.js';
import Rook from '../pieces/rook.js';

export default function initialiseChessBoard() {
  const squares = Array(30).fill(null);

  for (let i = 5; i < 10; i++) {
    squares[i] = new Pawn(2);
    
  }
  for (let i = 20; i < 25; i++) {
    
    squares[i] = new Pawn(1);
  }
 
  squares[0] = new Rook(2);
  squares[25] = new Rook(1);

  squares[1] = new Knight(2);
  squares[26] = new Knight(1);
  
  squares[2] = new Bishop(2);
  squares[27] = new Bishop(1);
  
  squares[3] = new Queen(2);
  squares[4] = new King(2);

  squares[28] = new Queen(1);
  squares[29] = new King(1);

  return squares;
}