"""
YouTube Transcript Service
Handles fetching transcripts from YouTube videos
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import Tuple, List, Dict, Optional


class TranscriptService:
    """Service for handling YouTube transcript extraction"""
    
    @staticmethod
    def get_transcript(video_id: str) -> Tuple[Optional[str], Optional[List[Dict]]]:
        """
        Get transcript from YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (transcript_text, transcript_list) or (None, None) if failed
        """
        try:
            # Try to get transcript in multiple languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get English transcript first
            try:
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
            except:
                # If English not available, get any available transcript
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_data = transcript.fetch()
                except:
                    # Get the first available transcript in any language
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript_data = available_transcripts[0].fetch()
                    else:
                        raise Exception("No transcripts available for this video")
            
            # Combine all transcript segments into one text
            transcript_text = " ".join([item["text"] for item in transcript_data])
            return transcript_text, transcript_data
            
        except Exception as e:
            error_msg = f"Error fetching transcript: {str(e)}"
            print(error_msg)
            return None, None
    
    @staticmethod
    def get_transcript_info(video_id: str) -> Dict:
        """
        Get information about available transcripts
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with transcript information
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            available = []
            
            for transcript in transcript_list:
                available.append({
                    'language': transcript.language,
                    'language_code': transcript.language_code,
                    'is_generated': transcript.is_generated,
                    'is_translatable': transcript.is_translatable
                })
            
            return {
                'available': True,
                'transcripts': available,
                'count': len(available)
            }
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'transcripts': [],
                'count': 0
            }
