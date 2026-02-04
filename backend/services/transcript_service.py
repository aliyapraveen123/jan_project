"""
YouTube Transcript Service
Uses YouTube captions first, falls back to audio extraction + AI transcription
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import Tuple, List, Dict, Optional
import os
import yt_dlp
import google.generativeai as genai
from pathlib import Path
import tempfile


class TranscriptService:
    """Service for handling YouTube transcript extraction"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key for audio transcription fallback"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
    
    @staticmethod
    def _get_caption_transcript(video_id: str) -> Tuple[Optional[str], Optional[List[Dict]]]:
        """
        Try to get transcript from YouTube captions (fast method)
        
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
                transcript = transcript_list.find_transcript(["en"])
                transcript_data = transcript.fetch()
            except:
                # If English not available, get any available transcript
                try:
                    transcript = transcript_list.find_generated_transcript(["en"])
                    transcript_data = transcript.fetch()
                except:
                    # Get the first available transcript in any language
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript_data = available_transcripts[0].fetch()
                    else:
                        raise Exception("No captions available")
            
            # Combine all transcript segments into one text
            transcript_text = " ".join([item["text"] for item in transcript_data])
            
            print(f"✅ Extracted transcript from captions: {len(transcript_text)} characters")
            return transcript_text, transcript_data
            
        except Exception as e:
            print(f"⚠️ Captions not available: {str(e)}")
            return None, None
    
    def _download_audio(self, video_id: str) -> Optional[str]:
        """
        Download audio from YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Path to downloaded audio file or None if failed
        """
        try:
            # Create temp directory for audio
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f"{video_id}")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
            }
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"📥 Downloading audio from video...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Return the path to the mp3 file
            audio_file = f"{output_path}.mp3"
            if os.path.exists(audio_file):
                print(f"✅ Audio downloaded: {audio_file}")
                return audio_file
            else:
                print(f"❌ Audio file not found after download")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading audio: {str(e)}")
            return None
    
    def _transcribe_audio_with_gemini(self, audio_path: str) -> Optional[str]:
        """
        Transcribe audio file using Gemini AI
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            if not self.api_key:
                print("❌ No API key available for transcription")
                return None
            
            print("🤖 Transcribing audio with Gemini AI...")
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Upload audio file to Gemini
            print("📤 Uploading audio to Gemini...")
            audio_file = genai.upload_file(audio_path)
            
            # Use Gemini to transcribe
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = """Please transcribe this audio file completely and accurately.
Provide the full transcription of all spoken content.
Do not add any commentary or notes - just the transcription."""
            
            print("⏳ Waiting for transcription...")
            response = model.generate_content([prompt, audio_file])
            
            transcript = response.text.strip()
            
            print(f"✅ Transcription complete: {len(transcript)} characters")
            
            # Clean up uploaded file
            try:
                genai.delete_file(audio_file.name)
            except:
                pass
            
            return transcript
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"❌ API Quota Exceeded: Free tier limit reached (20 requests/day)")
                print(f"   Please wait 24 hours or use videos with captions")
            else:
                print(f"❌ Error transcribing audio: {error_msg}")
            return None
    
    def get_transcript(self, video_id: str) -> Tuple[Optional[str], Optional[List[Dict]]]:
        """
        Get transcript from YouTube video - tries captions first, then audio extraction
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (transcript_text, transcript_list) or (None, None) if failed
        """
        # Method 1: Try to get captions (fast and free)
        print("📝 Attempting to extract captions...")
        transcript, transcript_data = self._get_caption_transcript(video_id)
        
        if transcript:
            return transcript, transcript_data
        
        # Method 2: Download audio and transcribe with Gemini
        print("🎵 Captions not available, trying audio extraction...")
        
        audio_path = self._download_audio(video_id)
        if not audio_path:
            print("❌ Could not download audio")
            return None, None
        
        try:
            transcript = self._transcribe_audio_with_gemini(audio_path)
            
            # Clean up audio file
            try:
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            except:
                pass
            
            if transcript:
                return transcript, None
            else:
                return None, None
                
        except Exception as e:
            print(f"❌ Error in audio transcription: {str(e)}")
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
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable
                })
            
            return {
                "available": True,
                "transcripts": available,
                "count": len(available)
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "transcripts": [],
                "count": 0
            }
