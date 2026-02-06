"""
API Key Rotation Manager
Rotates between multiple API keys to maximize free tier quota
"""

import os
from typing import List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


class APIKeyRotator:
    """Manages rotation of multiple API keys"""
    
    def __init__(self):
        """Initialize with API keys from environment"""
        # Load keys from .env
        self.keys = self._load_keys()
        self.current_index = 0
        self.usage_file = Path("cache/api_usage.json")
        self.usage_file.parent.mkdir(exist_ok=True)
        self.usage_data = self._load_usage()
    
    def _load_keys(self) -> List[str]:
        """Load all API keys from environment or Streamlit secrets"""
        keys = []
        
        # Try to load from Streamlit secrets first (for cloud deployment)
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                # Primary key
                primary = st.secrets.get("GOOGLE_API_KEY")
                if primary:
                    keys.append(primary)
                
                # Secondary keys
                key2 = st.secrets.get("GOOGLE_API_KEY_2")
                if key2 and key2 != "your_second_api_key_here":
                    keys.append(key2)
                
                key3 = st.secrets.get("GOOGLE_API_KEY_3")
                if key3 and key3 != "your_third_api_key_here":
                    keys.append(key3)
        except:
            pass
        
        # If no keys from secrets, try environment variables (for local)
        if not keys:
            # Primary key
            primary = os.getenv("GOOGLE_API_KEY")
            if primary:
                keys.append(primary)
            
            # Secondary keys
            key2 = os.getenv("GOOGLE_API_KEY_2")
            if key2 and key2 != "your_second_api_key_here":
                keys.append(key2)
            
            key3 = os.getenv("GOOGLE_API_KEY_3")
            if key3 and key3 != "your_third_api_key_here":
                keys.append(key3)
        
        if not keys:
            raise ValueError("No API keys found in .env file or Streamlit secrets")
        
        return keys
    
    def _load_usage(self) -> dict:
        """Load usage data from file"""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Initialize usage data
        return {
            key: {
                "requests_today": 0,
                "last_reset": datetime.now().date().isoformat(),
                "total_requests": 0
            }
            for key in self.keys
        }
    
    def _save_usage(self):
        """Save usage data to file"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)
    
    def _reset_if_needed(self, key: str):
        """Reset daily counter if it's a new day"""
        # Initialize key if not exists
        if key not in self.usage_data:
            self.usage_data[key] = {
                "requests_today": 0,
                "last_reset": datetime.now().date().isoformat(),
                "total_requests": 0
            }
            self._save_usage()
            return
        
        today = datetime.now().date().isoformat()
        if self.usage_data[key]["last_reset"] != today:
            self.usage_data[key]["requests_today"] = 0
            self.usage_data[key]["last_reset"] = today
            self._save_usage()
    
    def get_next_key(self) -> Optional[str]:
        """
        Get next available API key with quota remaining
        
        Returns:
            API key string or None if all exhausted
        """
        # Try all keys starting from current index
        for i in range(len(self.keys)):
            key_index = (self.current_index + i) % len(self.keys)
            key = self.keys[key_index]
            
            self._reset_if_needed(key)
            
            # Check if key has quota remaining (20 requests/day)
            if self.usage_data[key]["requests_today"] < 20:
                self.current_index = key_index
                return key
        
        return None
    
    def record_request(self, key: str):
        """
        Record that a request was made with this key
        
        Args:
            key: API key that was used
        """
        # Initialize key if not exists
        if key not in self.usage_data:
            self.usage_data[key] = {
                "requests_today": 0,
                "last_reset": datetime.now().date().isoformat(),
                "total_requests": 0
            }
        
        self.usage_data[key]["requests_today"] += 1
        self.usage_data[key]["total_requests"] += 1
        self._save_usage()
    
    def get_current_key(self) -> str:
        """Get the current active API key"""
        return self.keys[self.current_index]
    
    def get_stats(self) -> dict:
        """
        Get usage statistics for all keys
        
        Returns:
            Dictionary with stats for each key
        """
        stats = {
            "total_keys": len(self.keys),
            "keys": []
        }
        
        for i, key in enumerate(self.keys, 1):
            self._reset_if_needed(key)
            masked_key = f"{key[:20]}...{key[-4:]}"
            
            stats["keys"].append({
                "key_number": i,
                "key": masked_key,
                "requests_today": self.usage_data[key]["requests_today"],
                "remaining_today": 20 - self.usage_data[key]["requests_today"],
                "total_requests": self.usage_data[key]["total_requests"]
            })
        
        return stats
    
    def has_available_quota(self) -> bool:
        """
        Check if any key has remaining quota
        
        Returns:
            True if at least one key has quota remaining
        """
        return self.get_next_key() is not None
