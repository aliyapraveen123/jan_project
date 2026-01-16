"""
Utility functions for URL parsing and video ID extraction
"""

from urllib.parse import urlparse, parse_qs
from typing import Optional


class URLUtils:
    """Utility class for handling YouTube URLs"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video ID or None if extraction failed
        """
        try:
            # Handle different YouTube URL formats
            if "youtu.be" in url:
                # Format: https://youtu.be/VIDEO_ID
                return url.split("/")[-1].split("?")[0]
            elif "youtube.com" in url:
                parsed_url = urlparse(url)
                if parsed_url.path == "/watch":
                    # Format: https://www.youtube.com/watch?v=VIDEO_ID
                    return parse_qs(parsed_url.query)["v"][0]
                elif parsed_url.path.startswith("/embed/"):
                    # Format: https://www.youtube.com/embed/VIDEO_ID
                    return parsed_url.path.split("/")[2]
                elif parsed_url.path.startswith("/v/"):
                    # Format: https://www.youtube.com/v/VIDEO_ID
                    return parsed_url.path.split("/")[2]
            return None
        except Exception as e:
            print(f"Error extracting video ID: {str(e)}")
            return None
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """
        Check if URL is a valid YouTube URL
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid YouTube URL, False otherwise
        """
        if not url:
            return False
        
        return "youtube.com" in url or "youtu.be" in url
    
    @staticmethod
    def clean_url(url: str) -> str:
        """
        Clean URL by removing extra parameters
        
        Args:
            url: URL to clean
            
        Returns:
            Cleaned URL
        """
        try:
            video_id = URLUtils.extract_video_id(url)
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
            return url
        except:
            return url
