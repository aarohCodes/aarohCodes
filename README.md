<div align="center">
  <img src="./assets/hero.svg" width="100%" alt="Aaroh Nanoti. An autonomous race car drives through a neon city at night while its LiDAR scans the road and labels a cone, a sign and a barrier." />
</div>

<p align="center">
  <b>Aaroh Nanoti</b> · Computer Science @ UT Dallas<br/>
  I build systems that perceive, decide, and move: autonomous vehicles, medical-imaging ML, and LLM agents.
</p>

<br/>

<img src="./assets/h-profile.svg" width="100%" alt="01 / Driver profile" />

<img align="right" width="36%" src="./assets/radar.svg" alt="Radar sweep of what I'm tracking: self-driving, ADAS, LLM agents, energy ML, medical AI, ROS 2" />

I'm a computer science student at UT Dallas. I like problems where software has to deal with the real world: a car that has to see the track, a scan a clinician has to trust, an assistant that has to actually get the thing done.

- 🏎️ **Autonomous vehicles and ADAS**: ROS 2, F1TENTH racing, dSPACE ASM simulation
- 🩻 **Medical-imaging ML** that reports its own limits: confidence intervals, leakage audits, abstention
- 🧠 **LLM agents** with tool calling and voice interfaces
- ⚡ **Energy systems**: LSTM demand forecasting
- 🏁 **Hackathons**: HackAI, Axxess, FinHack (winner), T-Mobile challenge

<sub>Fun fact: I debug code faster than I debug my life.</sub>

<br clear="both"/>

<img src="./assets/h-grid.svg" width="100%" alt="02 / Starting grid: featured projects" />

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/OvaScope_Meta_2026"><img src="./assets/p1-ovascope.svg" width="100%" alt="P1 OvaScope: an ultrasound sweep finds a lesion, draws a box prompt, then a segmentation mask" /></a>
<b><a href="https://github.com/aarohCodes/OvaScope_Meta_2026">OvaScope</a></b><br/>
Ovarian ultrasound analysis with inspectable evidence. Asks whether lesion localisation (a DINOv2 patch localiser prompting SAM 2.1) beats whole-image classification on eight MMOTU categories, then reports what the data says: bootstrap confidence intervals, a near-duplicate leakage audit, and an abstain path. Research prototype, not a diagnostic.<br/>
<sub><code>PyTorch</code> <code>DINOv2</code> <code>SAM 2.1</code> <code>FastAPI</code> <code>Next.js</code> <code>Docker</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/HackAI2026"><img src="./assets/p2-pondr.svg" width="100%" alt="P2 Pondr: a knowledge graph whose nodes fade from green to red, then refresh" /></a>
<b><a href="https://github.com/aarohCodes/HackAI2026">Pondr</a></b><br/>
Adaptive learning platform built for HackAI 2026. What you know becomes a live knowledge graph; an XGBoost model on Ebbinghaus forgetting curves predicts when each concept will fade, and a Gemini tutor schedules the review before it does.<br/>
<sub><code>FastAPI</code> <code>XGBoost</code> <code>Gemini</code> <code>MongoDB</code> <code>React Flow</code> <code>ElevenLabs</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/AxxessHackathon2026"><img src="./assets/p3-maternalguard.svg" width="100%" alt="P3 MaternalGuard: a heartbeat trace above SHAP feature bars" /></a>
<b><a href="https://github.com/aarohCodes/AxxessHackathon2026">MaternalGuard</a></b><br/>
Clinical decision-support prototype from Axxess Hackathon 2026. Predicts risk for five postpartum complications and explains each prediction with SHAP values a clinician can read. Trained on synthetic data.<br/>
<sub><code>XGBoost</code> <code>SHAP</code> <code>FastAPI</code> <code>Next.js</code> <code>Recharts</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/Jarvis"><img src="./assets/p4-jarvis.svg" width="100%" alt="P4 Jarvis: rotating reactor rings above a voice waveform" /></a>
<b><a href="https://github.com/aarohCodes/Jarvis">Jarvis</a></b><br/>
A personal assistant for student life. An LLM with tool calling sits on top of my Canvas calendar, course schedule, syllabi, tasks and weather, builds a morning briefing, and pushes reminders to my phone. Web and mobile clients.<br/>
<sub><code>FastAPI</code> <code>PostgreSQL</code> <code>Redis</code> <code>Next.js</code> <code>React Native</code> <code>Docker</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/F1Tenth-Autonomous-Division"><img src="./assets/p5-f1tenth.svg" width="100%" alt="P5 F1TENTH: a car laps a circuit with its LiDAR fan out front" /></a>
<b><a href="https://github.com/aarohCodes/F1Tenth-Autonomous-Division">F1TENTH Autonomous Division</a></b><br/>
ROS 2 workspace for the F1TENTH 1/10-scale autonomous racing platform: Ackermann drive publisher and relay nodes with launch files, run against the F1TENTH gym simulator. The start of the racing stack.<br/>
<sub><code>ROS 2</code> <code>rclpy</code> <code>Ackermann</code> <code>f1tenth_gym_ros</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/aarohCodes/Robo-Advisory-Portfolio-Optimizer"><img src="./assets/p6-quada.svg" width="100%" alt="P6 QUADA: an efficient frontier draws itself and marks the max-Sharpe portfolio" /></a>
<b><a href="https://github.com/aarohCodes/Robo-Advisory-Portfolio-Optimizer">QUADA</a></b> 🏆<br/>
FinHack-winning robo-advisor. Builds ESG-aware portfolios across risk profiles and pairs them with a Gemini-powered investment chat.<br/>
<sub><code>React</code> <code>Flask</code> <code>Gemini</code> <code>Tailwind</code> <code>Google OAuth</code></sub>
</td>
</tr>
</table>

<img src="./assets/h-pitlane.svg" width="100%" alt="03 / Pit lane: more builds" />

| Build | What it does | Stack |
| :-- | :-- | :-- |
| **[Arkos](https://github.com/aarohCodes/AI-Driven-Energy-Advisory-and-LSTM-Prediction-Platform)** | HackAI 2025 team project. AI energy advisory with LSTM demand forecasting; 15% improvement in energy efficiency. | `TensorFlow` `LSTM` `Python` |
| **[Network Optimizer](https://github.com/aarohCodes/HarmoniQ-T-Mobile-Challenge)** | T-Mobile challenge team project. Forecasts cellular network demand and recommends where to allocate capacity. | `Prophet` `scikit-learn` `Flask` `React` |
| **[CodeRed](https://github.com/aarohCodes/CodeRed)** | Voice-first kitchen assistant: wake word, pantry inventory, image scanning. | `Python` `Gemini` `ElevenLabs` |
| **[FlowCraft](https://github.com/aarohCodes/FlowCraft)** | AI productivity suite: tasks, flashcards, email triage, meeting transcripts. | `React` `TypeScript` `Supabase` |
| **RSNA Knee** 🔒 | Knee abnormality detection for the RSNA Kaggle competition. Private working repo. | `Medical imaging` `Kaggle` |

<img src="./assets/h-power.svg" width="100%" alt="04 / Power unit: tech stack" />

| Subsystem | Components |
| :-- | :-- |
| **Engine** <br/><sub>languages</sub> | <kbd>Python</kbd> <kbd>TypeScript</kbd> <kbd>JavaScript</kbd> <kbd>C++</kbd> <kbd>Java</kbd> <kbd>SQL</kbd> |
| **Perception** <br/><sub>ML</sub> | <kbd>PyTorch</kbd> <kbd>TensorFlow</kbd> <kbd>scikit-learn</kbd> <kbd>XGBoost</kbd> <kbd>SHAP</kbd> <kbd>DINOv2</kbd> <kbd>SAM 2.1</kbd> <kbd>pandas</kbd> <kbd>NumPy</kbd> |
| **Driver aids** <br/><sub>LLMs and voice</sub> | <kbd>Claude API</kbd> <kbd>Gemini API</kbd> <kbd>OpenAI API</kbd> <kbd>tool calling</kbd> <kbd>ElevenLabs</kbd> |
| **Chassis** <br/><sub>full stack</sub> | <kbd>FastAPI</kbd> <kbd>Flask</kbd> <kbd>Next.js</kbd> <kbd>React</kbd> <kbd>React Native</kbd> <kbd>Tailwind</kbd> |
| **Fuel system** <br/><sub>data and infra</sub> | <kbd>PostgreSQL</kbd> <kbd>MongoDB</kbd> <kbd>Redis</kbd> <kbd>Supabase</kbd> <kbd>Docker</kbd> <kbd>Git</kbd> |
| **Track tools** <br/><sub>robotics and sim</sub> | <kbd>ROS 2</kbd> <kbd>F1TENTH gym</kbd> <kbd>dSPACE ASM</kbd> |

<img src="./assets/h-radio.svg" width="100%" alt="05 / Team radio: contact" />

<p align="center">
  Building something in autonomy, medical AI, or agents? The radio is on.
</p>

<p align="center">
  <a href="mailto:aarohnanoti@gmail.com"><img src="./assets/btn-email.svg" height="46" alt="Email" /></a>
  &nbsp;
  <a href="https://github.com/aarohCodes?tab=repositories"><img src="./assets/btn-github.svg" height="46" alt="All repos" /></a>
</p>

<details>
<summary>📻 Radio transcript</summary>
<br/>

```
ENGINEER  Box, box. The tests are failing.
AAROH     Copy. It works on my machine.
ENGINEER  We are checking.
AAROH     Leave me alone, I know what I'm doing.
ENGINEER  ...CI is green. Push, push.
```

</details>

<br/>

<img src="./assets/footer.svg" width="100%" alt="Chequered flag. Thanks for stopping by." />
