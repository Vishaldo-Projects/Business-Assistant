# 💼 Business AI Assistant

A professional AI-powered business consultant built with Google's Gemini API and Gradio. Get expert guidance on strategy, marketing, finance, operations, and more for your business needs.

## 🚀 Features

- **💬 Professional Business Consultation** - Expert advice across all business domains
- **📊 Persistent Conversation History** - Track your consultation sessions
- **⚡ Real-time Streaming Responses** - Get immediate, detailed guidance
- **🎯 Specialized Business Expertise** - Covers strategy, finance, marketing, operations, and scaling
- **💾 Session Management** - Automatic conversation saving and loading
- **📈 Business Analytics** - Track consultation history and progress

## 🎯 Business Services

### 📈 Strategy & Planning
- Business model development
- Strategic planning & goal setting
- Competitive analysis
- SWOT analysis & risk assessment

### 💰 Finance & Accounting
- Financial planning & forecasting
- Budgeting & cost management
- Pricing strategies
- Investment & funding advice

### 🎯 Marketing & Sales
- Digital marketing strategies
- Brand development
- Customer acquisition & retention
- Sales funnel optimization

### 🏢 Operations & Management
- Process optimization
- Team building & HR
- Supply chain management
- Quality control systems

### 🚀 Growth & Scaling
- Market expansion strategies
- Partnership development
- Technology implementation
- Performance metrics & KPIs

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google API Key (Gemini)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/business-ai-assistant.git
cd business-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

5. **Get your Google API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy and paste it into your `.env` file

## 🚦 Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:7860`

### Using the Business Assistant

1. **Ask Business Questions**: Type your business challenge or question
2. **Get Expert Advice**: Receive professional guidance with actionable steps
3. **Follow Up**: Ask for clarification or deeper insights
4. **Track History**: Review past consultations in the summary section

### Example Queries

```
"Help me create a business plan for my startup idea"
"What's the best marketing strategy for a small local business?"
"How do I price my products competitively?"
"What should I consider when hiring my first employee?"
"How can I improve my cash flow management?"
```

## 📁 Project Structure

```
business-ai-assistant/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
├── chat_history.log           # Text logs (auto-generated)
└── conversation_history.json  # Session data (auto-generated)
```

## 📦 Dependencies

```txt
gradio>=4.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

## ⚙️ Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

### Model Settings
- **Model**: `gemini-1.5-flash` (configurable in app.py)
- **Port**: `7860` (configurable in app.py)
- **Host**: `127.0.0.1` (configurable in app.py)

## 🔧 Customization

### Modify Business Expertise
Edit the `system_message` in `app.py` to customize the assistant's expertise areas and communication style.

### Change UI Theme
Modify the Gradio theme in the `gr.Blocks()` configuration:
```python
with gr.Blocks(title="Business AI Assistant", theme=gr.themes.Soft()) as demo:
```

### Add New Example Queries
Add to the `examples` list in the Gradio interface section.

## 📊 Data Storage

- **Conversation History**: Stored in `conversation_history.json`
- **Chat Logs**: Stored in `chat_history.log` with timestamps
- **Session Persistence**: Automatically loads previous conversations on startup

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   [ERROR] Google API Key not set
   ```
   **Solution**: Ensure your `.env` file contains a valid `GOOGLE_API_KEY`

2. **OpenMP Warning**
   ```
   OMP: Error #15: Initializing libiomp5md.dll
   ```
   **Solution**: The app automatically sets `KMP_DUPLICATE_LIB_OK=TRUE` to handle this

3. **Port Already in Use**
   ```
   Address already in use
   ```
   **Solution**: Change the port in `app.py` or kill the process using port 7860

### Getting Help

If you encounter issues:
1. Check the console logs for error messages
2. Verify your Google API key is valid and has quota
3. Ensure all dependencies are installed correctly
4. Check that Python version is 3.8 or higher

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Google Gemini API** - For providing the AI capabilities
- **Gradio** - For the user interface framework
- **Open Source Community** - For the amazing tools and libraries

**⚠️ Disclaimer**: This assistant provides general business guidance. For legal, tax, or specialized professional advice, consult qualified professionals.

**🎯 Made for entrepreneurs, by entrepreneurs** - Helping businesses grow and succeed! 💼✨
