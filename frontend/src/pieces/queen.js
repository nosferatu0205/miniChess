import Piece from './piece.js';
import { isSameRow, isSameColumn, isSameDiagonal, isPathClean } from '../helpers'

export default class Queen extends Piece {
  constructor(player) {
    super(player, (player === 1 ? "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg"));
  }

  isMovePossible(src, dest, squares, isDestEnemyOccupied) {
    const srcToDestPath = this.getSrcToDestPath(src, dest);
    return isPathClean(srcToDestPath, squares) && (isSameColumn(src, dest) || isSameRow(src, dest) || isSameDiagonal(src, dest));
  }

  /**
   * get path between src and dest (src and dest exclusive)
   * @param  {num} src  
   * @param  {num} dest 
   * @return {[array]}      
   */
  getSrcToDestPath(src, dest) {
    let path = [], pathStart, pathEnd, incrementBy;
    if (src > dest) {
      pathStart = dest;
      pathEnd = src;
    }
    else {
      pathStart = src;
      pathEnd = dest;
    }
    if (Math.abs(src - dest) % 5 === 0) {
      incrementBy = 5;
      pathStart += 5;
    }
    else if (Math.abs(src - dest) % 6 === 0) {
      incrementBy = 6;
      pathStart += 6;
    }
    else if (Math.abs(src - dest) % 4 === 0) {
      incrementBy = 4;
      pathStart += 4;
    }
    else {
      incrementBy = 1;
      pathStart += 1;
    }

    for (let i = pathStart; i < pathEnd; i += incrementBy) {
      path.push(i);
    }
    return path;
  }
}