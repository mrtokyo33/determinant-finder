"""
Use case for calculating matrix determinant.
"""
import logging
from typing import List, Tuple
from entities.matrix import Matrix
from entities.determinant_calculator import DeterminantCalculator

logger = logging.getLogger(__name__)


class CalculateDeterminantUseCase:
    """Use case for calculating matrix determinant with logging."""
    
    def __init__(self):
        """Initialize the use case."""
        self.calculator = DeterminantCalculator()
        logger.info("CalculateDeterminantUseCase initialized")
    
    def execute(self, matrix_data: List[List[float]]) -> Tuple[float, List[str]]:
        """
        Execute determinant calculation.
        
        Args:
            matrix_data: 2D list representing matrix elements
            
        Returns:
            Tuple of (determinant_value, calculation_steps)
            
        Raises:
            ValueError: If matrix is invalid or not square
        """
        logger.info("Starting determinant calculation use case")
        
        try:
            # Create matrix entity
            matrix = Matrix(matrix_data)
            logger.info(f"Matrix created successfully: {matrix.rows}x{matrix.cols}")
            
            # Calculate determinant with steps
            determinant, steps = self.calculator.calculate_with_steps(matrix)
            
            logger.info(f"Determinant calculation completed: {determinant}")
            return determinant, steps
            
        except Exception as e:
            logger.error(f"Error in determinant calculation: {str(e)}")
            raise
    
    def validate_matrix_data(self, matrix_data: List[List[float]]) -> Tuple[bool, str]:
        """
        Validate matrix data before calculation.
        
        Args:
            matrix_data: 2D list representing matrix elements
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not matrix_data:
                return False, "Matrix cannot be empty"
            
            if not all(isinstance(row, list) for row in matrix_data):
                return False, "All rows must be lists"
            
            if not all(len(row) == len(matrix_data[0]) for row in matrix_data):
                return False, "All rows must have the same length"
            
            if not all(isinstance(element, (int, float)) for row in matrix_data for element in row):
                return False, "All elements must be numbers"
            
            if len(matrix_data) != len(matrix_data[0]):
                return False, "Matrix must be square to calculate determinant"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error validating matrix data: {str(e)}")
            return False, f"Validation error: {str(e)}"
