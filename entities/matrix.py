"""
Matrix entity representing a mathematical matrix.
"""
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class Matrix:
    """Represents a mathematical matrix with operations for determinant calculation."""
    
    def __init__(self, data: List[List[float]]):
        """
        Initialize matrix with given data.
        
        Args:
            data: 2D list representing matrix elements
        """
        self._validate_matrix(data)
        self._data = [row[:] for row in data]  # Deep copy
        self._rows = len(data)
        self._cols = len(data[0]) if data else 0
        
        logger.info(f"Matrix created with dimensions {self._rows}x{self._cols}")
    
    def _validate_matrix(self, data: List[List[float]]) -> None:
        """Validate that the matrix data is properly formatted."""
        if not data:
            raise ValueError("Matrix cannot be empty")
        
        if not all(isinstance(row, list) for row in data):
            raise ValueError("All rows must be lists")
        
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("All rows must have the same length")
        
        if not all(isinstance(element, (int, float)) for row in data for element in row):
            raise ValueError("All elements must be numbers")
    
    @property
    def rows(self) -> int:
        """Get number of rows."""
        return self._rows
    
    @property
    def cols(self) -> int:
        """Get number of columns."""
        return self._cols
    
    @property
    def is_square(self) -> bool:
        """Check if matrix is square."""
        return self._rows == self._cols
    
    def get_element(self, row: int, col: int) -> float:
        """Get element at specified position."""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Index out of bounds")
        return self._data[row][col]
    
    def set_element(self, row: int, col: int, value: float) -> None:
        """Set element at specified position."""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Index out of bounds")
        self._data[row][col] = value
        logger.debug(f"Set element at ({row}, {col}) to {value}")
    
    def get_submatrix(self, exclude_row: int, exclude_col: int) -> 'Matrix':
        """
        Get submatrix by excluding specified row and column.
        
        Args:
            exclude_row: Row index to exclude
            exclude_col: Column index to exclude
            
        Returns:
            New Matrix instance with submatrix
        """
        if not (0 <= exclude_row < self._rows and 0 <= exclude_col < self._cols):
            raise IndexError("Exclude indices out of bounds")
        
        submatrix_data = []
        for i in range(self._rows):
            if i != exclude_row:
                row = []
                for j in range(self._cols):
                    if j != exclude_col:
                        row.append(self._data[i][j])
                submatrix_data.append(row)
        
        logger.debug(f"Created submatrix excluding row {exclude_row} and col {exclude_col}")
        return Matrix(submatrix_data)
    
    def to_list(self) -> List[List[float]]:
        """Convert matrix to 2D list."""
        return [row[:] for row in self._data]
    
    def __str__(self) -> str:
        """String representation of matrix."""
        return '\n'.join([' '.join(f'{elem:8.2f}' for elem in row) for row in self._data])
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Matrix({self._data})"
