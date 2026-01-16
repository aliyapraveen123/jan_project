"""
AI Service for generating summaries, key points, and quizzes
Uses Google Gemini AI
"""

import google.generativeai as genai
import json
import re
from typing import Optional, List, Dict


class AIService:
    """Service for AI-powered content generation using Google Gemini"""
    
    def __init__(self, api_key: str):
        """
        Initialize AI service with API key
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.model = None
        self.configure_api()
    
    def configure_api(self) -> bool:
        """Configure Google Gemini API"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            return True
        except Exception as e:
            print(f"Error configuring API: {str(e)}")
            return False
    
    def generate_summary(self, transcript: str) -> Optional[str]:
        """
        Generate comprehensive summary using Gemini
        
        Args:
            transcript: Video transcript text
            
        Returns:
            Generated summary or None if failed
        """
        try:
            prompt = f"""
            You are an expert educational content analyzer. Analyze the following YouTube video transcript and provide a comprehensive summary.
            
            Transcript:
            {transcript}
            
            Please provide:
            1. A brief overview (2-3 sentences)
            2. Main topics covered (bullet points)
            3. Detailed summary organized by sections
            4. Key takeaways
            
            Format your response in a clear, structured way suitable for students.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return None
    
    def extract_key_points(self, transcript: str) -> Optional[str]:
        """
        Extract core learning points from transcript
        
        Args:
            transcript: Video transcript text
            
        Returns:
            Extracted key points or None if failed
        """
        try:
            prompt = f"""
            You are an expert educator. Analyze the following YouTube video transcript and extract the most important learning points.
            
            Transcript:
            {transcript}
            
            Extract 8-12 core learning points that students MUST remember. These should be:
            - Factual and specific
            - Exam-oriented
            - Clear and concise
            - Cover all major concepts
            
            Format each point as a numbered list with brief explanations where needed.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error extracting key points: {str(e)}")
            return None
    
    def generate_quiz(self, transcript: str, max_retries: int = 3) -> Optional[List[Dict]]:
        """
        Generate exactly 10 quiz questions from transcript
        
        Args:
            transcript: Video transcript text
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of quiz questions or None if failed
        """
        for attempt in range(max_retries):
            try:
                prompt = f"""
                You are an expert quiz creator. Based on the following YouTube video transcript, create EXACTLY 10 multiple-choice questions.
                
                Transcript:
                {transcript}
                
                Requirements:
                - Create EXACTLY 10 questions (no more, no less)
                - Questions should test understanding of key concepts from the video
                - Each question must have 4 options (A, B, C, D)
                - Only ONE correct answer per question
                - Include a mix of difficulty levels (easy, medium, hard)
                - Questions should be clear and unambiguous
                
                Format your response as a JSON array with this structure:
                [
                    {{
                        "question": "Question text here?",
                        "options": {{
                            "A": "Option A text",
                            "B": "Option B text",
                            "C": "Option C text",
                            "D": "Option D text"
                        }},
                        "correct_answer": "A",
                        "explanation": "Brief explanation of why this is correct"
                    }}
                ]
                
                Return ONLY the JSON array, nothing else.
                """
                
                response = self.model.generate_content(prompt)
                quiz_text = response.text.strip()
                
                # Extract JSON from response
                json_match = re.search(r'\[.*\]', quiz_text, re.DOTALL)
                if json_match:
                    quiz_json = json_match.group(0)
                    quiz_data = json.loads(quiz_json)
                    
                    # Ensure exactly 10 questions
                    if len(quiz_data) == 10:
                        return quiz_data
                    elif len(quiz_data) > 10:
                        return quiz_data[:10]
                    else:
                        # Less than 10, retry
                        print(f"Generated {len(quiz_data)} questions, retrying... (Attempt {attempt + 1})")
                        continue
                else:
                    print(f"Could not parse quiz JSON, retrying... (Attempt {attempt + 1})")
                    continue
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing quiz JSON: {str(e)}, retrying... (Attempt {attempt + 1})")
                continue
            except Exception as e:
                print(f"Error generating quiz: {str(e)}, retrying... (Attempt {attempt + 1})")
                continue
        
        # If all retries failed
        print(f"Failed to generate quiz after {max_retries} attempts")
        return None
