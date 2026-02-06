"""
Cache Manager for storing processed video results
Saves API calls by caching summaries, key points, and quizzes
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class CacheManager:
    """Manages local cache for processed videos"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.cache_dir / "transcripts").mkdir(exist_ok=True)
        (self.cache_dir / "summaries").mkdir(exist_ok=True)
        (self.cache_dir / "keypoints").mkdir(exist_ok=True)
        (self.cache_dir / "quizzes").mkdir(exist_ok=True)
    
    def _get_cache_path(self, video_id: str, content_type: str) -> Path:
        """Get cache file path for a video and content type"""
        return self.cache_dir / content_type / f"{video_id}.json"
    
    def is_cached(self, video_id: str) -> bool:
        """
        Check if video is fully cached (all components available)
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if all components are cached
        """
        required = ["transcripts", "summaries", "keypoints", "quizzes"]
        return all(
            self._get_cache_path(video_id, content_type).exists()
            for content_type in required
        )
    
    def get_cached_data(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve all cached data for a video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with transcript, summary, key_points, quiz or None
        """
        if not self.is_cached(video_id):
            return None
        
        try:
            data = {}
            
            # Load transcript
            with open(self._get_cache_path(video_id, "transcripts"), 'r', encoding='utf-8') as f:
                data['transcript'] = json.load(f)['content']
            
            # Load summary
            with open(self._get_cache_path(video_id, "summaries"), 'r', encoding='utf-8') as f:
                data['summary'] = json.load(f)['content']
            
            # Load key points
            with open(self._get_cache_path(video_id, "keypoints"), 'r', encoding='utf-8') as f:
                data['key_points'] = json.load(f)['content']
            
            # Load quiz
            with open(self._get_cache_path(video_id, "quizzes"), 'r', encoding='utf-8') as f:
                data['quiz'] = json.load(f)['content']
            
            return data
        
        except Exception as e:
            print(f"Error loading cached data: {e}")
            return None
    
    def save_to_cache(self, video_id: str, transcript: str = None, 
                     summary: str = None, key_points: str = None, 
                     quiz: Dict = None) -> bool:
        """
        Save processed data to cache
        
        Args:
            video_id: YouTube video ID
            transcript: Video transcript
            summary: Generated summary
            key_points: Extracted key points
            quiz: Generated quiz data
            
        Returns:
            True if saved successfully
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Save transcript
            if transcript:
                self._save_component(video_id, "transcripts", transcript, timestamp)
            
            # Save summary
            if summary:
                self._save_component(video_id, "summaries", summary, timestamp)
            
            # Save key points
            if key_points:
                self._save_component(video_id, "keypoints", key_points, timestamp)
            
            # Save quiz
            if quiz:
                self._save_component(video_id, "quizzes", quiz, timestamp)
            
            return True
        
        except Exception as e:
            print(f"Error saving to cache: {e}")
            return False
    
    def _save_component(self, video_id: str, content_type: str, 
                       content: Any, timestamp: str):
        """Save a single component to cache"""
        cache_data = {
            "video_id": video_id,
            "content": content,
            "cached_at": timestamp
        }
        
        path = self._get_cache_path(video_id, content_type)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    
    def clear_cache(self, video_id: Optional[str] = None):
        """
        Clear cache for a specific video or all videos
        
        Args:
            video_id: Specific video ID to clear, or None to clear all
        """
        if video_id:
            # Clear specific video
            for content_type in ["transcripts", "summaries", "keypoints", "quizzes"]:
                path = self._get_cache_path(video_id, content_type)
                if path.exists():
                    path.unlink()
        else:
            # Clear all cache
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        stats = {
            "total_videos": len(list((self.cache_dir / "transcripts").glob("*.json"))),
            "transcripts": len(list((self.cache_dir / "transcripts").glob("*.json"))),
            "summaries": len(list((self.cache_dir / "summaries").glob("*.json"))),
            "keypoints": len(list((self.cache_dir / "keypoints").glob("*.json"))),
            "quizzes": len(list((self.cache_dir / "quizzes").glob("*.json")))
        }
        return stats
