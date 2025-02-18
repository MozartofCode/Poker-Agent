# ♠️ Texas Hold'em Poker Simulation – AI Poker Agents 🃏  

**A simulation of Texas Hold'em Poker featuring a Poker Multi-Agent Bot (CrewAI) vs. a Monte Carlo Simulation Bot. This project leverages AI-driven decision-making to optimize poker strategy and gameplay.**  

## 📌 Overview  
This project simulates **Texas Hold'em Poker**, where multiple AI agents compete against each other using advanced decision-making strategies. The **Poker Multi-Agent System** (powered by CrewAI) competes against a **Monte Carlo Simulation Bot**, offering a realistic poker-playing experience. The simulation is designed to analyze AI-driven poker strategies and evaluate their effectiveness in different game scenarios.  

## 🔥 Key Features  
✅ **Poker Multi-Agent System** – Uses **CrewAI** to manage multiple poker-playing agents with distinct strategies.  
✅ **Monte Carlo Simulation Bot** – Simulates multiple possible game outcomes to make probabilistic decisions.  
✅ **Texas Hold'em Simulation** – Models real poker rules, betting structures, and hand evaluations.  
✅ **AI vs. AI Gameplay** – Compare different AI models based on win rates, profitability, and strategic adaptability.  
✅ **Performance Analysis** – Tracks decision efficiency and evaluates strategy effectiveness over multiple hands.  

## 🏗️ Tech Stack  
- **AI Agents:** CrewAI (Multi-Agent System)  
- **Monte Carlo Methods:** Monte Carlo Simulation for probabilistic decision-making  
- **Poker Logic:** Python-based hand evaluation and game mechanics  
- **Data Analysis:** NumPy, Pandas for statistical analysis  
- **Visualization:** Matplotlib for data visualization  

## 🃏 Poker Game Rules  
The simulation follows the **Texas Hold'em** poker format with the following structure:  
1️⃣ **2 to 6 AI Players** in each game simulation.  
2️⃣ Each player is **dealt two hole cards**, followed by community cards.  
3️⃣ The game follows the **pre-flop, flop, turn, and river** betting rounds.  
4️⃣ Players make strategic decisions based on **hand strength, probabilities, and expected value (EV) calculations**.  
5️⃣ The AI agents aim to **maximize profit and optimize betting strategies** over multiple rounds.  

## 🛠️ Installation & Setup  
### **Clone the repository:**  
```sh
git clone https://github.com/MozartofCode/Poker-Agent.git
cd Poker-Agent
```

### **Set up a virtual environment (optional but recommended):**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

### **Install dependencies:**  
```sh
pip install -r requirements.txt
```

### **Run the Poker Simulation:**  
```sh
python poker_simulation.py
```

## 🎯 AI Agent Strategies  
The project features two distinct AI-driven poker-playing strategies:  

### **1️⃣ CrewAI Poker Multi-Agent System**  
- Uses **multiple AI agents** that specialize in different aspects of poker strategy.  
- Agents make decisions based on **hand strength, betting patterns, and opponent modeling**.  
- Incorporates **bluffing, aggressive vs. passive strategies, and adaptive playstyles**.  

### **2️⃣ Monte Carlo Simulation Bot**  
- Simulates thousands of possible hands to estimate **expected win probabilities**.  
- Uses a **probabilistic decision-making** approach to maximize long-term profitability.  
- Adjusts betting behavior based on the strength of its current hand and estimated opponent moves.  

## 📊 Performance Analysis  
After running multiple simulations, the system provides statistical insights, such as:  
```
Total hands played: 50,000  
Win rate (CrewAI Agents): 56.4%  
Win rate (Monte Carlo Bot): 43.6%  
Average pot size: $75.23  
Biggest win streak: 8 hands  
```

## 🚧 Future Enhancements  
🔹 **Reinforcement Learning (RL)** – Train bots to self-optimize their poker strategies over time.  
🔹 **Neural Networks (DQN)** – Implement Deep Q-Networks to improve AI decision-making.  
🔹 **Real-Time Multiplayer Mode** – Enable live human-vs-AI poker matches.  
🔹 **Improved Bluffing Mechanics** – Enhance deception strategies using game-theory-based AI.  

## 🏆 Project Inspiration  
This project was inspired by **AI poker competitions** such as Libratus and Pluribus, which demonstrated how AI can outperform human professionals in poker through strategic decision-making and probability-based play.  

## 🤝 Contributing  
Contributions are welcome! Feel free to fork the repo, open issues, or submit pull requests.  
