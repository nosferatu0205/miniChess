import Piece from './piece.js';
import { isSameDiagonal } from '../helpers'

export default class Pawn extends Piece {
  constructor(player) {
    super(player, (player === 1 ? "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg"));
    this.initialPositions = {
      1: [20,21,22,23,24],
      2: [5, 6, 7, 8, 9]
    }
  }

  isMovePossible(src, dest, isDestEnemyOccupied) {

    if (this.player === 1) {
      if ((dest === src - 5 && !isDestEnemyOccupied) || (dest === src - 10 && !isDestEnemyOccupied && this.initialPositions[1].indexOf(src) !== -1)) {
        return true;
      }
      else if (isDestEnemyOccupied && isSameDiagonal(src, dest) && (dest === src - 4 || dest === src - 6)) {
        return true;
      }
    }
    else if (this.player === 2) {
      if ((dest === src +5 && !isDestEnemyOccupied) || (dest === src + 10 && !isDestEnemyOccupied && this.initialPositions[2].indexOf(src) !== -1)) {
        return true;
      }
      else if (isDestEnemyOccupied && isSameDiagonal(src, dest) && (dest === src + 4 || dest === src + 6)) {
        return true;
      }
    }
    return false;
  }

  /**
   * returns array of one if pawn moves two steps, else returns empty array  
   * @param  {[type]} src  [description]
   * @param  {[type]} dest [description]
   * @return {[type]}      [description]
   */
  getSrcToDestPath(src, dest) {
    if (dest === src - 10) {
      return [src - 5];
    }
    else if (dest === src + 10) {
      return [src + 5];
    }
    return [];
  }
}