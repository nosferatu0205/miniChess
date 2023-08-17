import Piece from './piece.js';
import { isSameRow, isSameColumn,  isPathClean } from '../helpers'

export default class Rook extends Piece {
  constructor(player) {
    super(player, (player === 1 ? "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg"));
  }

  isMovePossible(src, dest, squares, isDestEnemyOccupied) {
    const srcToDestPath = this.getSrcToDestPath(src, dest);
    if (srcToDestPath.length === 0) {
      return isSameColumn(src, dest) || isSameRow(src, dest);
    }
    return isPathClean(srcToDestPath, squares) && (isSameColumn(src, dest) || isSameRow(src, dest));
  }

  /**
   * get path between src and dest (src and dest exclusive)
   * @param  {num} src  
   * @param  {num} dest 
   * @return {[array]}      
   */
  getSrcToDestPath(src, dest) {
    console.log(src, dest);
    let path = [],
      pathStart,
      pathEnd,
      incrementBy;
    if (src > dest) {
      pathStart = dest;
      pathEnd = src;
    } else {
      pathStart = src;
      pathEnd = dest;
    }
    const boardSize = 5; // Change this to match your mini chess board's size
    if (Math.abs(src - dest) % 5 === 0) {
      incrementBy = 5;
      pathStart += 5;
    } else {
      incrementBy = 1;
      pathStart += 1;
    }


    for (let i = pathStart; i < pathEnd; i += incrementBy) {
      path.push(i);
    }


    return path;
  }



}