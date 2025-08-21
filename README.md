# 🧮 MathGenius Academy

An interactive Math Olympiad training platform powered by AI, designed to help students from Grade 1-10 master mathematics through adaptive learning and engaging challenges.

![MathGenius Academy](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-00D2FF?style=for-the-badge)

## ✨ Features

### 🎯 **Adaptive Learning**
- AI-generated questions tailored to grade level
- Dynamic difficulty adjustment based on performance
- Personalized learning paths for each student

### 📊 **Progress Tracking**
- Comprehensive analytics and performance insights
- Visual progress charts and trend analysis
- Achievement badges and streak tracking

### 🎮 **Multiple Game Modes**
- **Practice Mode**: Learn at your own pace with no time pressure
- **Timed Mode**: Build speed and confidence with time challenges
- **Challenge Mode**: Push your limits with advanced problems

### 🏆 **Achievement System**
- Earn badges for various accomplishments
- Track daily learning streaks
- Celebrate milestones and improvements

### 🎨 **Beautiful UI**
- Modern, responsive design with custom CSS
- Intuitive navigation and user-friendly interface
- Mobile-optimized for learning on any device

## 🚀 Live Demo

**Coming Soon!** - The application will be deployed on Streamlit Community Cloud.

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI Engine**: Groq API (Llama 3.3 70B Versatile)
- **Data Visualization**: Plotly, Pandas
- **Deployment**: Streamlit Community Cloud
- **Language**: Python 3.8+

## 📚 Grade Level Coverage

| Grade Range | Age Group | Topics Covered |
|-------------|-----------|----------------|
| **Grades 1-4** | Ages 6-10 | Basic arithmetic, counting, simple word problems, pattern recognition |
| **Grades 5-8** | Ages 10-14 | Pre-algebra, fractions, decimals, basic statistics, coordinate geometry |
| **Grades 9-10** | Ages 14-16 | Advanced algebra, geometry proofs, trigonometry, complex problem solving |

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mathgenius-academy.git
   cd mathgenius-academy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Create a `.streamlit/secrets.toml` file
   - Add your Groq API key:
     ```toml
     GROQ_API_KEY = "your_api_key_here"
     ```

4. **Run the application**
   ```bash
   streamlit run app1.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for AI question generation

### Customization Options
- Grade level difficulty mappings
- Question generation parameters
- UI themes and styling
- Achievement criteria

## 📈 Performance Features

- **Caching**: Optimized question generation with smart caching
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Fast Loading**: Efficient resource management and lazy loading
- **Error Handling**: Robust error handling for reliable user experience

## 🔒 Security

- API keys stored securely using Streamlit secrets
- No sensitive data exposed in client-side code
- Input validation and sanitization
- Secure deployment practices

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing the AI infrastructure
- **Streamlit** for the amazing web framework
- **Plotly** for beautiful data visualizations
- **Math educators** worldwide for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [deployment guide](deployment-guide.md) for common solutions
2. Review the [setup instructions](deployment-setup.md)
3. Open an issue on GitHub for bug reports
4. Contact us for feature requests

## 🎯 Roadmap

### Upcoming Features
- [ ] User authentication and persistent profiles
- [ ] Advanced analytics dashboard
- [ ] Social features and leaderboards
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Additional subjects beyond mathematics

### Technical Improvements
- [ ] Database integration for data persistence
- [ ] Advanced caching mechanisms
- [ ] Performance optimizations
- [ ] Enhanced AI question generation

---

**Made with ❤️ for young mathematicians everywhere!**

*Empowering the next generation of problem solvers through interactive learning.*