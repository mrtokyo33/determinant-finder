"""
Determinant calculator using Gaussian elimination (row reduction).
"""
import logging
from typing import List, Tuple
from .matrix import Matrix

logger = logging.getLogger(__name__)


class DeterminantCalculator:
    """Calculates matrix determinant using Gaussian elimination."""
    
    @staticmethod
    def calculate(matrix: Matrix) -> float:
        """
        Calculate determinant using Gaussian elimination.
        
        Args:
            matrix: Square matrix to calculate determinant for
            
        Returns:
            Determinant value
            
        Raises:
            ValueError: If matrix is not square
        """
        if not matrix.is_square:
            raise ValueError("Matrix must be square to calculate determinant")
        
        logger.info(f"Calculating determinant for {matrix.rows}x{matrix.cols} matrix using Gaussian elimination")
        
        # Create a copy of the matrix to avoid modifying the original
        matrix_data = matrix.to_list()
        n = matrix.rows
        determinant = 1.0
        row_swaps = 0
        
        # Convert to upper triangular form
        for i in range(n):
            # Find the pivot (largest element in current column)
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix_data[k][i]) > abs(matrix_data[max_row][i]):
                    max_row = k
            
            # Swap rows if necessary
            if max_row != i:
                matrix_data[i], matrix_data[max_row] = matrix_data[max_row], matrix_data[i]
                row_swaps += 1
                logger.debug(f"Swapped rows {i} and {max_row}")
            
            # If pivot is zero, matrix is singular
            if abs(matrix_data[i][i]) < 1e-10:
                logger.info("Matrix is singular (determinant = 0)")
                return 0.0
            
            # Eliminate column below pivot
            for k in range(i + 1, n):
                if abs(matrix_data[k][i]) > 1e-10:  # Skip if already zero
                    factor = matrix_data[k][i] / matrix_data[i][i]
                    logger.debug(f"Eliminating element ({k},{i}) using factor {factor}")
                    
                    for j in range(i, n):
                        matrix_data[k][j] -= factor * matrix_data[i][j]
        
        # Calculate determinant as product of diagonal elements
        for i in range(n):
            determinant *= matrix_data[i][i]
        
        # Apply sign change for row swaps
        if row_swaps % 2 == 1:
            determinant = -determinant
        
        logger.info(f"Final determinant: {determinant} (after {row_swaps} row swaps)")
        return determinant
    
    @staticmethod
    def calculate_with_steps(matrix: Matrix) -> Tuple[float, List[str]]:
        """
        Calculate determinant with detailed steps for logging.
        
        Args:
            matrix: Square matrix to calculate determinant for
            
        Returns:
            Tuple of (determinant, list of step descriptions)
        """
        steps = []
        
        if not matrix.is_square:
            raise ValueError("Matrix must be square to calculate determinant")
        
        steps.append(f"Calculating determinant for {matrix.rows}x{matrix.cols} matrix using Gaussian elimination")
        steps.append("=" * 50)
        
        # Create a copy of the matrix to avoid modifying the original
        matrix_data = [row[:] for row in matrix.to_list()]
        n = matrix.rows
        determinant = 1.0
        row_swaps = 0
        
        steps.append("Initial matrix:")
        DeterminantCalculator._add_matrix_to_steps(steps, matrix_data)
        
        # Convert to upper triangular form
        for i in range(n):
            steps.append(f"\n--- Step {i+1}: Working with column {i+1} ---")
            
            # Find the pivot (largest element in current column)
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix_data[k][i]) > abs(matrix_data[max_row][i]):
                    max_row = k
            
            # Swap rows if necessary
            if max_row != i:
                matrix_data[i], matrix_data[max_row] = matrix_data[max_row], matrix_data[i]
                row_swaps += 1
                steps.append(f"Swapped rows {i+1} and {max_row+1} (row swap #{row_swaps})")
                DeterminantCalculator._add_matrix_to_steps(steps, matrix_data)
            
            # If pivot is zero, matrix is singular
            if abs(matrix_data[i][i]) < 1e-10:
                steps.append("Pivot is zero - matrix is singular!")
                steps.append("Determinant = 0")
                return 0.0, steps
            
            steps.append(f"Pivot element: {matrix_data[i][i]}")
            
            # Eliminate column below pivot
            for k in range(i + 1, n):
                if abs(matrix_data[k][i]) > 1e-10:  # Skip if already zero
                    factor = matrix_data[k][i] / matrix_data[i][i]
                    steps.append(f"Eliminating row {k+1}: factor = {matrix_data[k][i]} / {matrix_data[i][i]} = {factor:.4f}")
                    
                    for j in range(i, n):
                        old_value = matrix_data[k][j]
                        matrix_data[k][j] -= factor * matrix_data[i][j]
                        if j == i:  # Only log the first element to avoid clutter
                            steps.append(f"  Row {k+1} = Row {k+1} - {factor:.4f} * Row {i+1}")
                    
                    DeterminantCalculator._add_matrix_to_steps(steps, matrix_data)
        
        steps.append("\n--- Final triangular matrix ---")
        DeterminantCalculator._add_matrix_to_steps(steps, matrix_data)
        
        # Calculate determinant as product of diagonal elements
        steps.append("\nCalculating determinant:")
        diagonal_products = []
        for i in range(n):
            diagonal_products.append(matrix_data[i][i])
            steps.append(f"Diagonal element [{i+1},{i+1}] = {matrix_data[i][i]}")
        
        determinant = 1.0
        for i, val in enumerate(diagonal_products):
            determinant *= val
            if i == 0:
                steps.append(f"Product so far: {val}")
            else:
                steps.append(f"Product so far: {determinant} * {val} = {determinant}")
        
        # Apply sign change for row swaps
        if row_swaps % 2 == 1:
            determinant = -determinant
            steps.append(f"\nApplied sign change for {row_swaps} row swaps (odd number)")
            steps.append(f"Final determinant: -{abs(determinant)} = {determinant}")
        else:
            steps.append(f"\nNo sign change needed ({row_swaps} row swaps - even number)")
            steps.append(f"Final determinant: {determinant}")
        
        return determinant, steps
    
    @staticmethod
    def _add_matrix_to_steps(steps: List[str], matrix_data: List[List[float]]) -> None:
        """Add matrix representation to steps list."""
        for i, row in enumerate(matrix_data):
            row_str = "  " + "  ".join(f"{elem:8.3f}" for elem in row)
            steps.append(row_str)
