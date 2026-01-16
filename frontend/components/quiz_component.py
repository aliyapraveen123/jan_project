"""
Quiz Component
Interactive quiz display with scoring
"""

import streamlit as st


def display_quiz(quiz_data):
    """
    Display interactive quiz
    
    Args:
        quiz_data: List of quiz questions
    """
    if not quiz_data or len(quiz_data) == 0:
        st.error("No quiz data available")
        return
    
    st.subheader(f"📝 Quiz ({len(quiz_data)} Questions)")
    
    # Initialize session state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Display questions
    for i, q in enumerate(quiz_data, 1):
        st.markdown(f"**Question {i}:** {q['question']}")
        
        options = q['options']
        answer = st.radio(
            f"Select your answer for Question {i}:",
            options=list(options.keys()),
            format_func=lambda x: f"{x}: {options[x]}",
            key=f"q_{i}",
            disabled=st.session_state.quiz_submitted
        )
        
        st.session_state.quiz_answers[i] = answer
        st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Submit Quiz", type="primary"):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    with col2:
        if st.button("Reset Quiz"):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
    
    # Show results after submission
    if st.session_state.quiz_submitted:
        st.markdown("---")
        st.subheader("📊 Quiz Results")
        
        correct_count = 0
        for i, q in enumerate(quiz_data, 1):
            user_answer = st.session_state.quiz_answers.get(i)
            correct_answer = q['correct_answer']
            
            if user_answer == correct_answer:
                correct_count += 1
                st.success(f"✅ Question {i}: Correct!")
            else:
                st.error(f"❌ Question {i}: Incorrect")
                st.info(f"Your answer: {user_answer} | Correct answer: {correct_answer}")
            
            with st.expander(f"Explanation for Question {i}"):
                st.write(q.get('explanation', 'No explanation available'))
        
        # Overall score
        score_percentage = (correct_count / len(quiz_data)) * 100
        st.markdown("---")
        st.metric(
            "Your Score",
            f"{correct_count}/{len(quiz_data)}",
            f"{score_percentage:.1f}%"
        )
        
        # Performance feedback
        if score_percentage >= 80:
            st.success("🎉 Excellent! You have a strong understanding of the content!")
        elif score_percentage >= 60:
            st.info("👍 Good job! Review the missed questions to improve further.")
        else:
            st.warning("📚 Keep studying! Review the key points and try again.")
