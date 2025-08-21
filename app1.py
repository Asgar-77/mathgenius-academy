import streamlit as st
import os
from groq import Groq
import json
import re
from typing import List, Dict, Optional
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="🧮 MathGenius Academy",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Hide Streamlit branding and elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    .stActionButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    #MainMenu {display: none;}
    footer {display: none;}
    .stApp > header {display: none;}
    .css-1rs6os {display: none;}
    .css-17eq0hr {display: none;}
    .viewerBadge_container__1QSob {display: none;}
    .styles_viewerBadge__1yB5_ {display: none;}
    #MainMenu {visibility: hidden;}
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    
    /* Force light mode theme */
    .stApp {
        background-color: #FFFFFF !important;
        color: #262730 !important;
    }
    
    .main .block-container {
        background-color: #FFFFFF !important;
    }
    
    /* Ensure sidebar stays light */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #F0F2F6 !important;
    }
    
    /* Override any dark mode styles */
    [data-theme="dark"] .stApp {
        background-color: #FFFFFF !important;
        color: #262730 !important;
    }
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Nunito:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header Styling */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(20px, -20px) rotate(180deg); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Card Styling */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        color: #333;
    }
    
    .custom-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .custom-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .custom-card h4 {
        color: #667eea !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .custom-card p, .custom-card li {
        color: #444 !important;
        line-height: 1.6;
    }
    
    .custom-card ul {
        padding-left: 1.5rem;
    }
    
    .custom-card ol {
        padding-left: 1.5rem;
    }
    
    /* Question Card */
    .question-card {
        background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 6px solid #667eea;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateX(10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Buttons */
    .custom-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .custom-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e2e8f0;
        border-radius: 50px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 20px;
        border-radius: 50px;
        transition: width 1s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    /* Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .slide-in-up {
        animation: slideInUp 0.6s ease-out;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Toast Notifications */
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideInRight 0.5s ease;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .custom-card {
            padding: 1rem;
        }
        
        .question-card {
            padding: 1rem;
        }
    }
    body, .main, .block-container {
        background: #f7f9fb !important;
    }
    .custom-card {
        margin-bottom: 2rem;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
    }
    .question-card {
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 24px rgba(102, 126, 234, 0.10);
        margin-bottom: 2rem;
        padding: 2rem 2.5rem;
    }
    .question-card:hover {
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    .question-card .stRadio > div {
        gap: 1.5rem;
    }
    .stRadio label {
        background: #f0f4fa;
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        transition: background 0.2s, color 0.2s;
        cursor: pointer;
    }
    .stRadio label:hover {
        background: #e3e9f7;
        color: #667eea;
    }
    .stRadio input:checked + label {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 2.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.10);
        transition: background 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    .stMarkdown hr {
        border: none;
        border-top: 2px solid #e1e8ed;
        margin: 2rem 0;
    }
    .progress-container {
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

class MathOlympiadExam:
    def __init__(self):
        self.client = self._initialize_groq_client()
        self.grade_levels = {
            1: {"name": "Grade 1 (Ages 6-7)", "emoji": "🌱", "color": "#FF6B6B"},
            2: {"name": "Grade 2 (Ages 7-8)", "emoji": "🌿", "color": "#4ECDC4"},
            3: {"name": "Grade 3 (Ages 8-9)", "emoji": "🍃", "color": "#45B7D1"},
            4: {"name": "Grade 4 (Ages 9-10)", "emoji": "🌳", "color": "#96CEB4"},
            5: {"name": "Grade 5 (Ages 10-11)", "emoji": "🎯", "color": "#FECA57"},
            6: {"name": "Grade 6 (Ages 11-12)", "emoji": "🚀", "color": "#FF9FF3"},
            7: {"name": "Grade 7 (Ages 12-13)", "emoji": "⭐", "color": "#54A0FF"},
            8: {"name": "Grade 8 (Ages 13-14)", "emoji": "💎", "color": "#5F27CD"},
            9: {"name": "Grade 9 (Ages 14-15)", "emoji": "🏆", "color": "#00D2D3"},
            10: {"name": "Grade 10 (Ages 15-16)", "emoji": "👑", "color": "#FF6348"}
        }
        
    def _initialize_groq_client(self) -> Optional[Groq]:
        """Initialize Groq client with API key"""
        try:
            # Use Streamlit secrets for secure API key management
            api_key = st.secrets["GROQ_API_KEY"]
            if not api_key:
                st.error("⚠️ GROQ_API_KEY not found in secrets!")
                return None
            return Groq(api_key=api_key)
        except Exception as e:
            st.error(f"Failed to initialize Groq client: {e}")
            return None
    
    def generate_questions(self, grade: int, num_questions: int, difficulty: str = "medium") -> List[Dict]:
        """Generate math olympiad questions with enhanced difficulty options"""
        if not self.client:
            return []
            
        try:
            difficulty_map = {
                1: "very basic arithmetic, counting 1-20, simple shapes recognition, basic patterns",
                2: "addition and subtraction within 100, simple word problems, basic time and money", 
                3: "multiplication tables up to 10, basic division, simple fractions, pattern recognition",
                4: "advanced multiplication and division, fractions, basic decimals, area and perimeter",
                5: "advanced arithmetic, introduction to algebra, geometry, data interpretation",
                6: "pre-algebra, ratios and proportions, percentages, coordinate geometry, statistics",
                7: "algebra fundamentals, advanced geometry, probability, scientific notation",
                8: "linear equations, quadratic basics, trigonometry introduction, advanced geometry",
                9: "advanced algebra, geometry proofs, probability and statistics, trigonometry",
                10: "pre-calculus, advanced trigonometry, complex numbers, advanced problem solving"
            }
            
            difficulty_modifiers = {
                "easy": "Make questions slightly easier than typical olympiad level, focusing on fundamental concepts",
                "medium": "Standard olympiad difficulty with moderate complexity",
                "hard": "Advanced olympiad level with complex multi-step problems"
            }
            
            topics = difficulty_map.get(grade, "general math concepts")
            modifier = difficulty_modifiers.get(difficulty, "")
            
            prompt = f"""Generate exactly {num_questions} Math Olympiad-style multiple choice questions for Grade {grade} students.

Topics focus: {topics}
Difficulty: {modifier}

Format each question EXACTLY as follows:
**Question X:** [Question text here]
A) [Option A]
B) [Option B] 
C) [Option C]
D) [Option D]
**Correct Answer:** [Letter only - A, B, C, or D]
**Explanation:** [Clear step-by-step solution]
**Hint:** [Helpful hint for students]

Make questions engaging and educational. Include varied problem types: word problems, visual problems, logical reasoning, and computational challenges."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert Math Olympiad coach creating engaging, educational questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            return self._parse_questions(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Failed to generate questions: {e}")
            return []
    
    def _parse_questions(self, content: str) -> List[Dict]:
        """Enhanced question parsing with hints"""
        questions = []
        question_blocks = re.split(r'\*\*Question \d+:\*\*', content)[1:]
        
        for i, block in enumerate(question_blocks, 1):
            try:
                lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
                
                if len(lines) < 6:
                    continue
                    
                question_text = lines[0]
                options = []
                correct_answer = None
                explanation = ""
                hint = ""
                
                for line in lines[1:]:
                    if line.startswith(('A)', 'B)', 'C)', 'D)')):
                        options.append(line)
                    elif line.startswith('**Correct Answer:**'):
                        correct_answer = line.replace('**Correct Answer:**', '').strip()
                    elif line.startswith('**Explanation:**'):
                        explanation = line.replace('**Explanation:**', '').strip()
                    elif line.startswith('**Hint:**'):
                        hint = line.replace('**Hint:**', '').strip()
                
                if len(options) == 4 and correct_answer:
                    questions.append({
                        'question_number': i,
                        'question_text': question_text,
                        'options': options,
                        'correct_answer': correct_answer,
                        'explanation': explanation,
                        'hint': hint,
                        'user_answer': None,
                        'time_taken': 0,
                        'difficulty': self._estimate_difficulty(question_text)
                    })
                    
            except Exception as e:
                st.warning(f"Error parsing question {i}: {e}")
                continue
        
        return questions
    
    def _estimate_difficulty(self, question_text: str) -> str:
        """Estimate question difficulty based on content"""
        hard_keywords = ['prove', 'complex', 'advanced', 'multiple steps', 'system of']
        easy_keywords = ['basic', 'simple', 'find', 'calculate', 'what is']
        
        text_lower = question_text.lower()
        
        if any(keyword in text_lower for keyword in hard_keywords):
            return "Hard"
        elif any(keyword in text_lower for keyword in easy_keywords):
            return "Easy"
        else:
            return "Medium"

# Initialize session state
def initialize_session_state():
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'exam_completed' not in st.session_state:
        st.session_state.exam_completed = False
    if 'grade_selected' not in st.session_state:
        st.session_state.grade_selected = None
    if 'exam_history' not in st.session_state:
        st.session_state.exam_history = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'exam_mode' not in st.session_state:
        st.session_state.exam_mode = 'practice'
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'Math Explorer',
            'total_exams': 0,
            'total_questions': 0,
            'correct_answers': 0,
            'favorite_grade': 5,
            'badges': [],
            'streak': 0
        }
    if 'seen_questions' not in st.session_state:
        st.session_state.seen_questions = set()

@st.cache_resource
def get_exam_system():
    return MathOlympiadExam()

def render_hero_section():
    """Render the hero section with animations"""
    st.markdown("""
    <div class="hero-header slide-in-up">
        <div class="hero-title">🧮 MathGenius Academy</div>
        <div class="hero-subtitle">Master Mathematics Through Interactive Olympiad Training</div>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">🎯 Adaptive Learning</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">📊 Progress Tracking</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem;">🏆 Achievement System</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Render user dashboard with statistics"""
    profile = st.session_state.user_profile
    
    st.markdown("### 📊 Your Learning Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{profile['total_exams']}</div>
            <div class="stat-label">Exams Taken</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        accuracy = (profile['correct_answers'] / max(profile['total_questions'], 1)) * 100
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{accuracy:.1f}%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{profile['streak']}</div>
            <div class="stat-label">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(profile['badges'])}</div>
            <div class="stat-label">Badges Earned</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress Chart
    if st.session_state.exam_history:
        df = pd.DataFrame(st.session_state.exam_history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Performance Trend")
            fig = px.line(df, x='date', y='percentage', 
                         title='Your Progress Over Time',
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Grade Distribution")
            grade_counts = df['grade'].value_counts().sort_index()
            fig = px.bar(x=grade_counts.index, y=grade_counts.values,
                        title='Exams by Grade Level',
                        color_discrete_sequence=['#764ba2'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)

def render_question_card(question, question_index, total_questions):
    """Render an individual question with enhanced UI"""
    progress = ((question_index + 1) / total_questions) * 100
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%;">
            Question {question_index + 1} of {total_questions}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="question-card slide-in-up">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="color: #667eea; margin: 0;">Question {question['question_number']}</h3>
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">
                {question.get('difficulty', 'Medium')} Level
            </span>
        </div>
        <div style="font-size: 1.1rem; font-weight: 500; margin-bottom: 1.5rem; line-height: 1.6; color: #222;">
            {question['question_text']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Options with enhanced styling
    option_labels = [opt.split(')', 1)[1].strip() for opt in question['options']]
    option_keys = [opt.split(')', 1)[0].strip() for opt in question['options']]
    
    selected = st.radio(
        "Choose your answer:",
        options=option_keys,
        format_func=lambda x, labels=option_labels, keys=option_keys: f"{x}) {labels[keys.index(x)]}",
        key=f"q_{question_index}",
        index=None
    )
    
    # Hint system
    if st.button(f"💡 Need a hint?", key=f"hint_{question_index}"):
        if question.get('hint'):
            st.info(f"💡 **Hint:** {question['hint']}")
        else:
            st.info("💡 **Hint:** Try breaking down the problem step by step!")
    
    return selected

def render_exam_interface():
    """Render the main exam interface"""
    questions = st.session_state.questions
    total_questions = len(questions)
    
    if st.session_state.exam_mode == 'timed':
        # Timer display
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, (total_questions * 120) - elapsed)  # 2 minutes per question
            
            mins, secs = divmod(int(remaining), 60)
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E8E); color: white; 
                           padding: 1rem; border-radius: 15px; display: inline-block; font-size: 1.5rem; font-weight: 600;">
                    ⏰ {mins:02d}:{secs:02d}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if remaining <= 0:
                st.error("⏰ Time's up! Submitting your exam...")
                st.session_state.exam_completed = True
                st.rerun()
    
    # Question navigation
    if total_questions > 1:
        st.markdown("#### 📍 Question Navigation")
        cols = st.columns(min(10, total_questions))
        for i in range(total_questions):
            with cols[i % 10]:
                status = "✅" if questions[i]['user_answer'] else "⭕"
                if st.button(f"{status} Q{i+1}", key=f"nav_{i}"):
                    st.session_state.current_question = i
    
    # Current question
    current_q = st.session_state.current_question
    if current_q < total_questions:
        selected = render_question_card(questions[current_q], current_q, total_questions)
        questions[current_q]['user_answer'] = selected
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_q > 0:
                if st.button("⬅️ Previous", key="prev_btn"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if current_q < total_questions - 1:
                if st.button("Next ➡️", key="next_btn"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("🎯 Submit Exam", key="submit_btn", type="primary"):
                    unanswered = [i+1 for i, q in enumerate(questions) if not q['user_answer']]
                    
                    if unanswered:
                        st.error(f"⚠️ Please answer all questions. Missing: {', '.join(map(str, unanswered))}")
                    else:
                        st.session_state.exam_completed = True
                        st.rerun()

def calculate_badges(score, total, grade):
    """Calculate badges earned based on performance"""
    percentage = (score / total) * 100
    badges = []
    
    if percentage == 100:
        badges.append("🏆 Perfect Score")
    elif percentage >= 90:
        badges.append("⭐ Excellence")
    elif percentage >= 80:
        badges.append("🎯 High Achiever")
    elif percentage >= 70:
        badges.append("📚 Good Progress")
    
    if grade >= 8:
        badges.append("🚀 Advanced Level")
    
    return badges

def render_results_section():
    """Render enhanced results with animations and insights - REMOVED ACTION BUTTONS"""
    st.markdown("---")
    st.markdown("### 🎉 Exam Results")
    
    questions = st.session_state.questions
    correct_count = sum(1 for q in questions if q['user_answer'] == q['correct_answer'])
    total_questions = len(questions)
    percentage = (correct_count / total_questions) * 100
    
    # Update user profile
    profile = st.session_state.user_profile
    profile['total_exams'] += 1
    profile['total_questions'] += total_questions
    profile['correct_answers'] += correct_count
    
    # Add to history
    st.session_state.exam_history.append({
        'date': datetime.now(),
        'grade': st.session_state.grade_selected,
        'score': correct_count,
        'total': total_questions,
        'percentage': percentage
    })
    
    # Calculate badges
    new_badges = calculate_badges(correct_count, total_questions, st.session_state.grade_selected)
    profile['badges'].extend(new_badges)
    
    # Animated score reveal
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card pulse-animation">
            <div class="stat-number">{correct_count}/{total_questions}</div>
            <div class="stat-label">Final Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card pulse-animation">
            <div class="stat-number">{percentage:.1f}%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if percentage >= 90:
            grade_emoji = "🏆"
            grade_text = "Excellent!"
        elif percentage >= 80:
            grade_emoji = "⭐"
            grade_text = "Great Job!"
        elif percentage >= 70:
            grade_emoji = "👍"
            grade_text = "Good Work!"
        else:
            grade_emoji = "📚"
            grade_text = "Keep Practicing!"
        
        st.markdown(f"""
        <div class="stat-card pulse-animation">
            <div class="stat-number">{grade_emoji}</div>
            <div class="stat-label">{grade_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # New badges notification
    if new_badges:
        st.success(f"🎉 New badges earned: {', '.join(new_badges)}")
    
    # Detailed question review
    st.markdown("#### 📝 Question Review")
    
    for i, question in enumerate(questions):
        is_correct = question['user_answer'] == question['correct_answer']
        
        with st.expander(f"Question {i+1} - {'✅ Correct' if is_correct else '❌ Incorrect'} ({question.get('difficulty', 'Medium')} Level)"):
            st.markdown(f"**Question:** {question['question_text']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Your Answer:** {question['user_answer']}")
            with col2:
                st.markdown(f"**Correct Answer:** {question['correct_answer']}")
            
            if question.get('explanation'):
                st.markdown(f"**Explanation:** {question['explanation']}")
            
            if not is_correct and question.get('hint'):
                st.info(f"💡 **Hint for next time:** {question['hint']}")
    
    # Performance insights
    exam_system = get_exam_system()
    if exam_system.client:
        st.markdown("#### 🧠 AI Performance Analysis")
        with st.spinner("Generating personalized insights..."):
            summary = generate_enhanced_summary(
                st.session_state.grade_selected,
                questions,
                correct_count,
                total_questions,
                exam_system
            )
        
        st.markdown(f"""
        <div class="custom-card">
            {summary}
        </div>
        """, unsafe_allow_html=True)
    
    # Show completion message instead of action buttons
    st.markdown("#### 🎓 Exam Complete!")
    st.info("Great job completing the exam! Use the sidebar to generate a new exam or check out the Dashboard tab to view your progress.")

def generate_enhanced_summary(grade, questions, score, total, exam_system):
    """Generate enhanced AI-powered performance summary"""
    try:
        # Analyze performance patterns
        correct_questions = [q for q in questions if q['user_answer'] == q['correct_answer']]
        incorrect_questions = [q for q in questions if q['user_answer'] != q['correct_answer']]
        
        difficulty_analysis = {}
        for q in questions:
            diff = q.get('difficulty', 'Medium')
            if diff not in difficulty_analysis:
                difficulty_analysis[diff] = {'correct': 0, 'total': 0}
            difficulty_analysis[diff]['total'] += 1
            if q['user_answer'] == q['correct_answer']:
                difficulty_analysis[diff]['correct'] += 1
        
        percentage = (score / total * 100) if total > 0 else 0
        
        prompt = f"""Analyze this Math Olympiad performance for a Grade {grade} student:

PERFORMANCE SUMMARY:
- Score: {score}/{total} ({percentage:.1f}%)
- Difficulty Breakdown: {difficulty_analysis}

SAMPLE INCORRECT QUESTIONS:
{chr(10).join([f"- {q['question_text'][:100]}..." for q in incorrect_questions[:2]])}

Please provide a concise summary (max 4-5 sentences) with:
- 1-2 key strengths
- 1 main area to improve
- 1 motivational message
Use simple, encouraging language for a Grade {grade} student. Avoid long lists or detailed study plans."""

        response = exam_system.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert Math Olympiad mentor providing detailed, encouraging feedback to help students improve."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"""
        **Performance Summary:**
        You scored {score} out of {total} ({percentage:.1f}%).
        Great job! You showed strong skills in several areas. Focus on reviewing the questions you missed. Keep practicing and you'll get even better! 🌟
        """

def reset_exam():
    """Reset exam state for new attempt"""
    st.session_state.questions = []
    st.session_state.exam_completed = False
    st.session_state.current_question = 0
    st.session_state.start_time = None
    st.rerun()

def render_sidebar():
    """Enhanced sidebar with user profile and settings"""
    exam_system = get_exam_system()
    
    with st.sidebar:
        # User profile section
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">👋</div>
            <div style="font-size: 1.2rem; font-weight: 600;">{st.session_state.user_profile['name']}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Level {st.session_state.user_profile['favorite_grade']} Explorer</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Exam Configuration")
        
        # Grade selection with enhanced UI
        grade_options = list(exam_system.grade_levels.keys())
        grade_labels = [f"{exam_system.grade_levels[g]['emoji']} {exam_system.grade_levels[g]['name']}" for g in grade_options]
        
        grade = st.selectbox(
            "🎯 Select Grade Level:",
            options=grade_options,
            format_func=lambda x: f"{exam_system.grade_levels[x]['emoji']} {exam_system.grade_levels[x]['name']}",
            key="grade_selector",
            help="Choose your current grade level for appropriate difficulty"
        )
        
        # Exam mode
        exam_mode = st.radio(
            "📝 Exam Mode:",
            ["practice", "timed", "challenge"],
            format_func=lambda x: {
                "practice": "🎯 Practice Mode",
                "timed": "⏰ Timed Mode", 
                "challenge": "🔥 Challenge Mode"
            }[x],
            help="Practice: No time limit | Timed: 2 min/question | Challenge: Extra hard questions"
        )
        st.session_state.exam_mode = exam_mode
        
        # Number of questions
        if exam_mode == "challenge":
            num_questions = st.slider("📊 Questions:", 5, 20, 10, help="Challenge mode: 5-20 questions")
        else:
            num_questions = st.slider("📊 Questions:", 3, 15, 5, help="Choose number of questions")
        
        # Difficulty level
        difficulty = st.select_slider(
            "⚡ Difficulty:",
            options=["easy", "medium", "hard"],
            value="medium",
            format_func=lambda x: {
                "easy": "🟢 Easy",
                "medium": "🟡 Medium", 
                "hard": "🔴 Hard"
            }[x]
        )
        
        # Generate exam button
        if st.button("🚀 Generate New Exam", type="primary", use_container_width=True):
            if not exam_system.client:
                st.error("🚫 API not available!")
            else:
                with st.spinner(f"🎭 Creating your {exam_mode} exam..."):
                    # Add loading animation
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    challenge_difficulty = "hard" if exam_mode == "challenge" else difficulty
                    questions = exam_system.generate_questions(grade, num_questions, challenge_difficulty)
                    
                    if questions:
                        # Filter out previously seen questions
                        if 'seen_questions' in st.session_state:
                            new_questions = [q for q in questions if q['question_text'] not in st.session_state.seen_questions]
                            st.session_state.questions = new_questions
                            # Update seen_questions with the new questions
                            st.session_state.seen_questions.update(q['question_text'] for q in new_questions)
                        else:
                            st.session_state.questions = questions
                        
                        st.session_state.exam_completed = False
                        st.session_state.grade_selected = grade
                        st.session_state.current_question = 0
                        st.session_state.start_time = time.time() if exam_mode == "timed" else None
                        
                        st.success(f"✨ Generated {len(st.session_state.questions)} questions!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to generate exam. Try again!")
        
        st.markdown("---")
        
        # Quick stats
        profile = st.session_state.user_profile
        st.markdown("### 📈 Quick Stats")
        st.metric("🎯 Total Exams", profile['total_exams'])
        
        if profile['total_questions'] > 0:
            accuracy = (profile['correct_answers'] / profile['total_questions']) * 100
            st.metric("🎪 Accuracy", f"{accuracy:.1f}%")
        
        st.metric("🔥 Streak", f"{profile['streak']} days")
        
        # Recent badges
        if profile['badges']:
            st.markdown("### 🏆 Recent Badges")
            for badge in profile['badges'][-3:]:
                st.markdown(f"- {badge}")
        
        st.markdown("---")
        
        # Settings
        with st.expander("⚙️ Settings"):
            new_name = st.text_input("Your Name:", value=profile['name'])
            if new_name != profile['name']:
                profile['name'] = new_name
                st.success("Name updated!")
            
            if st.button("🗑️ Reset Progress"):
                if st.checkbox("I'm sure"):
                    initialize_session_state()
                    st.success("Progress reset!")
                    st.rerun()

def render_welcome_screen():
    """Render welcome screen for new users"""
    # Main welcome container
    st.markdown("""
    <div class="custom-card slide-in-up" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌟</div>
        <h2 style="color: #667eea; margin-bottom: 1rem;">Welcome to MathGenius Academy!</h2>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            Ready to embark on an exciting mathematical journey? Let's discover your potential!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards using Streamlit columns for better compatibility
    st.markdown("### ✨ What Makes Us Special")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="margin: 0.5rem 0; color: white;">Adaptive Learning</h4>
            <p style="margin: 0; color: rgba(255,255,255,0.9);">Questions adjust to your skill level</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="margin: 0.5rem 0; color: white;">Progress Tracking</h4>
            <p style="margin: 0; color: rgba(255,255,255,0.9);">See your improvement over time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🏆</div>
            <h4 style="margin: 0.5rem 0; color: white;">Achievement System</h4>
            <p style="margin: 0; color: rgba(255,255,255,0.9);">Earn badges and unlock new levels</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Getting started message
    st.markdown("---")
    st.info("👈 Choose your grade level from the sidebar and click 'Generate New Exam' to begin your mathematical adventure!")
    
    # Quick start tips
    with st.expander("🚀 Quick Start Guide"):
        st.markdown("""
        **Ready to begin? Follow these simple steps:**
        
        1. **🎯 Choose Your Grade**: Select your current grade level from the sidebar
        2. **📝 Pick Your Mode**: 
           - 🟢 **Practice Mode**: No time pressure, perfect for learning
           - ⏰ **Timed Mode**: Challenge yourself with time limits
           - 🔥 **Challenge Mode**: Extra difficult questions for advanced learners
        3. **⚡ Set Difficulty**: Easy, Medium, or Hard - pick what feels right
        4. **📊 Choose Questions**: 3-20 questions depending on your time
        5. **🚀 Generate & Start**: Hit the generate button and begin!
        
        **💡 Pro Tips:**
        - Start with Practice mode to get comfortable
        - Use hints when you're stuck - learning is the goal!
        - Review all explanations to understand concepts better
        - Track your progress in the Dashboard tab
        """)
    
    # Motivational quote
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 20px; color: white;">
        <h3 style="margin: 0; color: white;">"Mathematics is not about numbers, equations, or algorithms. It is about understanding." - William Paul Thurston</h3>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Get exam system
    exam_system = get_exam_system()
    
    # Render hero section
    render_hero_section()
    
    # Main navigation
    tab1, tab2, tab3 = st.tabs(["🎯 Exam", "📊 Dashboard", "ℹ️ About"])
    
    with tab1:
        # Render sidebar
        render_sidebar()
        
        # Main exam interface
        if not st.session_state.questions:
            render_welcome_screen()
        elif st.session_state.exam_completed:
            render_results_section()
        else:
            st.markdown("### 🧮 Math Olympiad Challenge")
            
            if st.session_state.exam_mode == "timed" and st.session_state.start_time:
                # Show exam info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"📚 Grade {st.session_state.grade_selected}")
                with col2:
                    st.info(f"⏱️ {st.session_state.exam_mode.title()} Mode")
                with col3:
                    st.info(f"📝 {len(st.session_state.questions)} Questions")
            
            render_exam_interface()
    
    with tab2:
        render_dashboard()
        
        # Additional dashboard features
        if st.session_state.exam_history:
            st.markdown("#### 🎯 Detailed Analytics")
            
            df = pd.DataFrame(st.session_state.exam_history)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Score Distribution")
                fig = px.histogram(df, x='percentage', nbins=10,
                                 title='Score Distribution',
                                 color_discrete_sequence=['#667eea'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("##### 📈 Improvement Trend")
                df_trend = df.copy()
                df_trend['moving_avg'] = df_trend['percentage'].rolling(window=3, min_periods=1).mean()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_trend['date'], y=df_trend['percentage'],
                                       mode='markers+lines', name='Actual Score',
                                       line=dict(color='#667eea')))
                fig.add_trace(go.Scatter(x=df_trend['date'], y=df_trend['moving_avg'],
                                       mode='lines', name='Trend',
                                       line=dict(color='#764ba2', dash='dash')))
                
                fig.update_layout(title='Performance Trend',
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        
        # Achievement showcase
        profile = st.session_state.user_profile
        if profile['badges']:
            st.markdown("#### 🏆 Your Achievements")
            
            badge_cols = st.columns(min(4, len(profile['badges'])))
            for i, badge in enumerate(profile['badges'][-8:]):  # Show last 8 badges
                with badge_cols[i % 4]:
                    st.markdown(f"""
                    <div style="text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); 
                                color: white; padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{badge.split()[0]}</div>
                        <div style="font-size: 0.8rem;">{' '.join(badge.split()[1:])}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("# 📖 About MathGenius Academy")
        
        # Mission section
        with st.container():
            st.markdown("## 🎯 Our Mission")
            st.markdown("""
            <div class="custom-card">
                <p style="font-size: 1.1rem; line-height: 1.6; color: #444;">
                    To make mathematics accessible, engaging, and fun for students of all levels through 
                    interactive Olympiad-style training. We believe every student can excel in mathematics 
                    with the right guidance and practice.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Features section
        st.markdown("## ✨ Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div class="custom-card">
                    <h4 style="color: #667eea;">🤖 AI-Powered Learning</h4>
                    <ul style="color: #444;">
                        <li><strong>Adaptive Questions:</strong> Problems that match your skill level</li>
                        <li><strong>Smart Difficulty:</strong> Automatic adjustment based on performance</li>
                        <li><strong>Personalized Feedback:</strong> Detailed insights and recommendations</li>
                    </ul>
                    <h4 style="color: #667eea;">🎮 Multiple Game Modes</h4>
                    <ul style="color: #444;">
                        <li><strong>Practice Mode:</strong> Learn at your own pace</li>
                        <li><strong>Timed Mode:</strong> Build speed and confidence</li>
                        <li><strong>Challenge Mode:</strong> Push your limits with hard problems</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="custom-card">
                    <h4 style="color: #667eea;">📊 Progress & Analytics</h4>
                    <ul style="color: #444;">
                        <li><strong>Performance Tracking:</strong> Monitor improvement over time</li>
                        <li><strong>Detailed Statistics:</strong> Accuracy, trends, and insights</li>
                        <li><strong>Visual Charts:</strong> Interactive graphs and analysis</li>
                    </ul>
                    <h4 style="color: #667eea;">🏆 Achievement System</h4>
                    <ul style="color: #444;">
                        <li><strong>Badges & Rewards:</strong> Celebrate your success</li>
                        <li><strong>Streak Tracking:</strong> Build consistent study habits</li>
                        <li><strong>Level Progression:</strong> Unlock new challenges</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Getting Started Guide
        st.markdown("## 🚀 Getting Started")
        
        steps_col1, steps_col2 = st.columns(2)
        
        with steps_col1:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #667eea;">📋 Setup Steps</h4>
                <ol style="color: #444;">
                    <li><strong>Select Grade Level:</strong> Choose from Grade 1-10</li>
                    <li><strong>Pick Exam Mode:</strong> Practice, Timed, or Challenge</li>
                    <li><strong>Set Difficulty:</strong> Easy, Medium, or Hard</li>
                    <li><strong>Choose Questions:</strong> 3-20 questions per exam</li>
                    <li><strong>Generate Exam:</strong> Click the generate button</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with steps_col2:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #667eea;">💡 Success Tips</h4>
                <ul style="color: #444;">
                    <li><strong>Start Easy:</strong> Begin with Practice mode</li>
                    <li><strong>Use Hints:</strong> Don't hesitate to ask for help</li>
                    <li><strong>Review Mistakes:</strong> Learn from wrong answers</li>
                    <li><strong>Track Progress:</strong> Check your Dashboard regularly</li>
                    <li><strong>Stay Consistent:</strong> Practice a little each day</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Grade Level Guide
        st.markdown("## 🎯 Grade Level Guide")
        
        grade_col1, grade_col2, grade_col3 = st.columns(3)
        
        with grade_col1:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #667eea;">🌱 Elementary (Grades 1-4)</h4>
                <ul style="color: #444;">
                    <li>Basic arithmetic operations</li>
                    <li>Simple word problems</li>
                    <li>Pattern recognition</li>
                    <li>Basic geometry shapes</li>
                    <li>Counting and number sense</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with grade_col2:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #667eea;">🚀 Middle School (Grades 5-8)</h4>
                <ul style="color: #444;">
                    <li>Pre-algebra concepts</li>
                    <li>Fractions and decimals</li>
                    <li>Basic statistics</li>
                    <li>Coordinate geometry</li>
                    <li>Problem-solving strategies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with grade_col3:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #667eea;">⭐ High School (Grades 9-10)</h4>
                <ul style="color: #444;">
                    <li>Advanced algebra</li>
                    <li>Geometry proofs</li>
                    <li>Trigonometry basics</li>
                    <li>Complex problem solving</li>
                    <li>Mathematical reasoning</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # FAQ Section
        with st.expander("❓ Frequently Asked Questions"):
            st.markdown("""
            **Q: How are the questions generated?**
            
            A: We use advanced AI to create unique, grade-appropriate questions that follow Math Olympiad standards.
            
            **Q: Can I retake exams?**
            
            A: Yes! You can generate unlimited exams to practice and improve your skills.
            
            **Q: How is my progress tracked?**
            
            A: We track your accuracy, response times, difficulty preferences, and improvement trends over time.
            
            **Q: What if I get stuck on a question?**
            
            A: Use the hint feature! We provide helpful hints to guide your thinking without giving away the answer.
            
            **Q: Is there a time limit?**
            
            A: Only in Timed Mode. Practice and Challenge modes let you work at your own pace.
            
            **Q: How do I earn badges?**
            
            A: Badges are earned automatically based on your performance, consistency, and achievements.
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white;">
            <h3 style="color: white; margin-bottom: 1rem;">Ready to become a Math Genius? 🧮</h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">
                Join thousands of students improving their mathematical skills every day!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Made with ❤️ for young mathematicians everywhere!**")

if __name__ == "__main__":
    main()