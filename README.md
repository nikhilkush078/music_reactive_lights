# 🎧✨ Smart Music Reactive RGB + Ambient Lighting System

<p align="center">
  <img src="https://img.shields.io/badge/Project-Smart%20RGB%20Lighting-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-Audio%20Processing-yellow?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Arduino-Serial%20Control-green?style=for-the-badge&logo=arduino"/>
  <img src="https://img.shields.io/badge/Status-Working-brightgreen?style=for-the-badge"/>
</p>

---

## 📖 Project Description

This project is a **smart music-reactive lighting system** that transforms audio signals into visually appealing lighting effects using **Python signal processing and Arduino-based hardware control**.

Unlike basic music LED projects that simply blink with sound, this system intelligently **analyzes the structure of music**—such as intensity changes, transitions, and rhythm flow—to produce **smooth, meaningful, and aesthetic lighting patterns**.

It combines:
- 🎧 Real-time audio analysis (Librosa)
- 🎨 Intelligent RGB lighting control
- 🌈 Ambient lighting generation
- 🔌 Hardware communication via serial (Arduino)

The result is a **synchronized light experience** that feels natural, immersive, and dynamic.

---

## 🎬 Demo Video

▶️ Watch the project in action:

👉 https://youtu.be/Wefth7JrdRE?si=o3tYnhsaC4pfSaFX

---

## 🧠 Detailed Explanation

### ⚙️ 1. Audio Processing

- The audio file is loaded using **Librosa**
- A **Short-Time Fourier Transform (STFT)** is applied
- This converts sound into frequency-domain data
- Energy is extracted from the signal:

```text
Energy = Mean of frequency magnitudes
```

This energy represents how **intense/loud** the music is at any moment.

---

### 📊 2. Signal Smoothing

Raw audio energy is unstable, so we apply smoothing:

```text
smooth_energy = 0.95 * prev + 0.05 * current
```

✅ Prevents flickering  
✅ Creates fluid transitions  

---

### 🎯 3. State Detection Logic

The system identifies **music behavior** using energy and its change:

| Condition | State |
|----------|------|
| Low energy | 💤 SLOW |
| Increasing energy | 🚀 BUILD |
| Decreasing energy | 🔻 DROP |
| Stable energy | ⚖️ STEADY |

---

### 🎨 4. RGB Lighting Logic

Each state generates a unique lighting pattern:

- 💤 **SLOW** → Smooth breathing white light  
- 🚀 **BUILD** → Forward color cycling (R → G → B)  
- 🔻 **DROP** → Reverse color cycling  
- ⚖️ **STEADY** → Brightness proportional to energy  

This makes lighting feel **connected to the music flow**, not random.

---

### 🌈 5. Ambient Lighting System

- A separate ambient strip runs continuously
- Uses sinusoidal waves for smooth color variation:

```text
Color = Base + Energy + Sinusoidal variation
```

✅ Always ON  
✅ Enhances environment mood  

---

### 🔌 6. Arduino Communication

Python sends real-time data to Arduino:

```text
R,G,B,AMBIENT\n
```

Example:
```text
255,100,50,120
```

Arduino reads this and outputs **PWM signals** to LEDs.

---

### 🖥️ 7. GUI Visualization

Tkinter provides a live preview:

- 🔴 Red LED
- 🟢 Green LED
- 🔵 Blue LED
- 🌈 Ambient strip

This helps debug and visualize behavior.

---

## 🎯 Features

🟣 Smart music understanding  
🟢 Smooth transitions (no flicker)  
🔵 Dual lighting system (RGB + Ambient)  
🟠 Real-time Arduino control  
🌈 Visually aesthetic patterns  

---

## ⚙️ Tech Stack

| Technology | Usage |
|----------|------|
| 🐍 Python | Core logic |
| 🎧 Librosa | Audio processing |
| 🔢 NumPy | Signal math |
| 🔊 SoundDevice | Audio playback |
| 🖥️ Tkinter | GUI |
| 🔌 PySerial | Arduino communication |

---

## 🚀 Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install librosa numpy sounddevice pyserial
```

---

### 2️⃣ Connect Arduino

- RGB LEDs → PWM pins (3, 5, 6)
- Ambient LED strip → PWM pin

---

### 3️⃣ Update COM Port

```python
arduino = serial.Serial('COM23', 9600)
```

---

### 4️⃣ Run

```bash
python main.py
```

---

## 🎛️ Customization

- 🎵 Sensitivity → energy thresholds  
- 🌈 Colors → RGB logic  
- 💡 Brightness → base values  
- ⏱️ Speed → update interval  

---

## 🔥 Future Improvements

- 🎤 Live microphone input  
- 📱 Mobile control  
- 🎚️ Frequency band lighting  
- 🌈 WS2812B LED strip support  

---

## 👨‍💻 Author

**Nikhil Kushwah**  
⚡ Electrical Engineering Student  
🚀 Embedded Systems Enthusiast  

---

## ⭐ Support

⭐ Star this repo  
🍴 Fork it  
🛠️ Improve it  

---

## 🎉 Final Note

> This project converts **sound into emotion through light**  
> — making music *visible*.

✨🔥🎶
