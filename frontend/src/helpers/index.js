const diagonalDictionaryTLBR = require('../dictionaries/diagonalTopLeftBottomRight.json');
const diagonalDictionaryTRBL = require('../dictionaries/diagonalTopRightBottomLeft.json');
const rowDictionary = require('../dictionaries/row.json');
const columnDictionary = require('../dictionaries/column.json');

const isSameRow = (src, dest) => {
  return !!(rowDictionary[src] && rowDictionary[src][dest]);
}

const isSameColumn = (src, dest) => {
  return !!(columnDictionary[src] && columnDictionary[src][dest]);
}

const isSameDiagonal = (src, dest) => {
  return !!((diagonalDictionaryTLBR[src] && diagonalDictionaryTLBR[src][dest]) ||
    (diagonalDictionaryTRBL[src] && diagonalDictionaryTRBL[src][dest]))
}

const isPathClean = (srcToDestPath, squares, isDestEnemyOccupied) => {
  
  for (let i = 0; i < srcToDestPath.length; i++) {
    
    if (squares[srcToDestPath[i]]) {
      return false;
    }
  }
  if (isDestEnemyOccupied) {
    return false;
  }

  return true;
};

module.exports = {
  isSameRow,
  isSameColumn,
  isSameDiagonal,
  isPathClean
}