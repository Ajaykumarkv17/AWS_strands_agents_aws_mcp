#!/usr/bin/env python3
"""
Windows-Compatible Diagram Generator
Bypasses MCP server's SIGALRM timeout mechanism
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class DiagramGenerator:
    """Direct diagram generation without MCP server timeout issues"""
    
    def __init__(self, output_dir: str = "diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_diagram(self, code: str, workspace_dir: Optional[str] = None) -> str:
        """
        Generate diagram from Python code
        
        Args:
            code: Python code using diagrams package
            workspace_dir: Optional directory for output
            
        Returns:
            Path to generated diagram file
        """
        try:
            # Set output directory
            if workspace_dir:
                output_path = Path(workspace_dir)
            else:
                output_path = self.output_dir
            
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Change to output directory
            original_dir = os.getcwd()
            os.chdir(output_path)
            
            try:
                # Execute the diagram code
                exec_globals = {}
                exec(code, exec_globals)
                
                # Find generated PNG files
                png_files = list(output_path.glob("*.png"))
                if png_files:
                    latest_file = max(png_files, key=lambda p: p.stat().st_mtime)
                    logger.info(f"Diagram generated: {latest_file}")
                    return str(latest_file)
                else:
                    raise FileNotFoundError("No diagram file was generated")
                    
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"Failed to generate diagram: {e}", exc_info=True)
            raise

def create_diagram_tool():
    """Create a Strands-compatible tool for diagram generation"""
    from strands import tool
    
    generator = DiagramGenerator()
    
    @tool
    def generate_aws_diagram(code: str, workspace_dir: Optional[str] = None) -> str:
        """
        Generate AWS architecture diagram from Python code.
        
        Args:
            code: Python code using diagrams package (no imports needed)
            workspace_dir: Optional output directory
            
        Returns:
            Path to generated diagram PNG file
        """
        # Add necessary imports to the code
        full_code = """
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import *
from diagrams.aws.database import *
from diagrams.aws.network import *
from diagrams.aws.storage import *
from diagrams.aws.analytics import *
from diagrams.aws.integration import *
from diagrams.aws.ml import *
from diagrams.aws.security import *
from diagrams.aws.management import *

""" + code
        
        return generator.generate_diagram(full_code, workspace_dir)
    
    return generate_aws_diagram

if __name__ == "__main__":
    # Test the generator
    test_code = '''
from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb

with Diagram("Test Serverless", show=False, filename="test_diagram"):
    api = APIGateway("API")
    lambda_fn = Lambda("Function")
    db = Dynamodb("Database")
    
    api >> lambda_fn >> db
'''
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(test_code)
    print(f"Generated: {result}")
