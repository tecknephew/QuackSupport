# 🦆 Quacksupport

Self-hosted desktop app to have AI control your computer, powered by the new Claude [computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) capability. Allow Claude to take over your laptop and do your tasks for you (or at least attempt to, lol). Written in Python, using PyQt.

## Demo

TODO 

## 🎯 What it does
Our agent provides step-by-step, visual guidance by spotlighting where users should move their cursor. It empowers them to easily navigate technology, reducing reliance on others and restoring confidence.

## 💻 How we built it

By leveraging Anthropic’s [computer-use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use), community [tools](https://github.com/suitedaces/computer-agent) built on top of it and [PyQt](https://wiki.python.org/moin/PyQt), we built an AI agent that is capable of interacting with the native operating system and guiding users visually without the dangers of giving full control.

A threaded agent loop powered real-time updates, ensuring the system refined its actions based on user feedback for an engaging and responsive experience.

## 🛠️ Setup

Get an Anthropic API key [here]([https://console.anthropic.com/keys](https://console.anthropic.com/dashboard)).

```bash
# Python 3.12+ recommended
poetry install 

# Add API key to .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run
poetry-run python run.py
```

## 🔑 Productivity Keybindings
- `Ctrl + Enter`: Execute the current instruction
- `Ctrl + C`: Stop the current agent action
- `Ctrl + W`: Minimize to system tray
- `Ctrl + Q`: Quit application

## 💡 What's next

We aim to refine accuracy and latency of our human-in-the-loop AI agent and build the community's trust into the technology, bridging the divide for groups left behind by digitalization and AI. 

We plan to expand the system’s capabilities by integrating voice-based interactions to expand Quacksupport's abilities to enable people suffering by neck-down paralysis. Quacksupport will continue to operate with a human-in-the-loop based system, validating all actions of the AI agent.

---
