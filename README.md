# 🧞‍♂️ Genie AI – A Visual AI Search Engine

Genie AI is a visually rich, AI-powered search engine built with **Streamlit**, combining the intelligence of GPT-4 and the power of the YouTube Data API to deliver search results with web links, images, and videos — all in a single interface.

---

## 📌 Features

- 🔍 **AI-Powered Search**: Get smart, context-aware answers using OpenAI's GPT-4.
- 🖼️ **Image Search**: Instantly fetch relevant images from the web.
- 🎥 **Video Search**: Embed YouTube results directly in your search output.
- 🌐 **Web Links**: Lists relevant article links just like a search engine.
- ⚙️ **Customizable Options**:
  - Set results per tab (slider)
  - Toggle Safe Search
  - Enable/Disable AI-generated answers
- 💬 **Multi-purpose**: Works for general queries (e.g., tourist spots, topics) and legal ones (like IPC sections).

---

## 🛠️ Tech Stack

| Component         | Technology        |
|------------------|-------------------|
| UI & Backend      | [Streamlit](https://streamlit.io/) |
| AI Engine         | OpenAI GPT-4 (via API key) |
| Video Search      | YouTube Data API |
| Image & Web Links | Custom scraping/API integrations |

---

## 🧠 How it works

Just type your query (e.g., _“Tourist places of Shivamogga”_ or _“IPC Section 302 explanation”_) and Genie AI fetches:

- 🌐 Related **web pages**
- 🖼️ Relevant **images**
- 📺 Related **YouTube videos**

You can switch between tabs (Web / Images / Videos) for each type of content.

> ✅ **Use cases**: Law students, researchers, travelers, or just curious minds.

---

## 📷 Demo Screenshots

**🔎 Image Search**
![Image Search](./Screenshot%202025-04-07%20220723.png)

**▶️ Video Results**
![Video Search](./Screenshot%202025-04-07%20220736.png)

---

## 🔑 API Keys Required

To run this app, you’ll need:

- **OpenAI API Key** – for GPT-4 responses
- **YouTube API Key** – for video embedding

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/genie-ai.git
   cd genie-ai
2.Install dependencies
  pip install -r requirements.txt
3.Run the app
  streamlit run app.py

