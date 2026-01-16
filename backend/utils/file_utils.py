"""
File utilities for downloading and managing content
"""

from datetime import datetime
from typing import Dict, Any
import json


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def generate_filename(prefix: str, video_id: str, extension: str) -> str:
        """
        Generate filename with timestamp
        
        Args:
            prefix: Filename prefix (e.g., 'transcript', 'summary')
            video_id: YouTube video ID
            extension: File extension (e.g., 'txt', 'json')
            
        Returns:
            Generated filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{video_id}_{timestamp}.{extension}"
    
    @staticmethod
    def prepare_download_data(content: str, content_type: str) -> Dict[str, Any]:
        """
        Prepare content for download
        
        Args:
            content: Content to download
            content_type: Type of content (transcript, summary, etc.)
            
        Returns:
            Dictionary with download data
        """
        return {
            'content': content,
            'type': content_type,
            'timestamp': datetime.now().isoformat(),
            'size': len(content)
        }
    
    @staticmethod
    def format_quiz_json(quiz_data: list) -> str:
        """
        Format quiz data as pretty JSON
        
        Args:
            quiz_data: Quiz questions list
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(quiz_data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def get_file_mime_type(extension: str) -> str:
        """
        Get MIME type for file extension
        
        Args:
            extension: File extension
            
        Returns:
            MIME type string
        """
        mime_types = {
            'txt': 'text/plain',
            'json': 'application/json',
            'md': 'text/markdown',
            'pdf': 'application/pdf'
        }
        return mime_types.get(extension, 'text/plain')
