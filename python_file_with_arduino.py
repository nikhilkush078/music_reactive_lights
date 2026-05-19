import librosa
import numpy as np
import sounddevice as sd
import time
import tkinter as tk
import serial

# ==============================
# 🔌 SERIAL SETUP (CHANGE PORT)
# ==============================
ser = serial.Serial('COM3', 115200)  # बदलें अगर अलग पोर्ट है
time.sleep(2)

# ==============================
# 🎧 LOAD AUDIO
# ==============================
FILE = "pasoori.mp3"
y, sr = librosa.load(FILE, sr=None)

# ==============================
# 🎚️ ENERGY ANALYSIS
# ==============================
S = np.abs(librosa.stft(y, n_fft=1024, hop_length=512))
energy = np.mean(S, axis=0)
energy /= np.max(energy)

# ==============================
# 💡 TKINTER SETUP
# ==============================
root = tk.Tk()
root.title("Smart RGB LED Controller")

canvas = tk.Canvas(root, width=400, height=200, bg="black")
canvas.pack()

led_r = canvas.create_oval(50, 50, 120, 120, fill="#000000")
led_g = canvas.create_oval(160, 50, 230, 120, fill="#000000")
led_b = canvas.create_oval(270, 50, 340, 120, fill="#000000")

# ==============================
# 🎵 PLAY AUDIO
# ==============================
sd.play(y, sr)
start_time = time.time()

prev_energy = 0
phase = 0

# ==============================
# 📡 SEND TO ARDUINO
# ==============================
def send_to_arduino(r, g, b):
    data = f"{r},{g},{b}\n"
    ser.write(data.encode())

# ==============================
# 💡 UPDATE LEDS
# ==============================
def set_leds(r, g, b):
    # Update UI (only intensity, no color mixing)
    canvas.itemconfig(led_r, fill=f'#{r:02x}0000')
    canvas.itemconfig(led_g, fill=f'#00{g:02x}00')
    canvas.itemconfig(led_b, fill=f'#0000{b:02x}')

    # Send to Arduino
    send_to_arduino(r, g, b)

# ==============================
# 🌊 BREATHING EFFECT
# ==============================
def breathing(t, speed=1):
    return int((0.5 + 0.5*np.sin(t * speed)) * 255)

# ==============================
# 🔄 MAIN LOOP
# ==============================
def update():
    global prev_energy, phase

    t = time.time() - start_time
    idx = int(t * sr / 512)

    if idx >= len(energy):
        return

    e = energy[idx]
    diff = e - prev_energy

    # ==============================
    # 🎯 STATE DETECTION
    # ==============================
    if e < 0.3:
        state = "SLOW"
    elif diff > 0.02:
        state = "BUILD"
    elif diff < -0.02:
        state = "DROP"
    else:
        state = "STEADY"

    # ==============================
    # 🎨 SEQUENCES
    # ==============================

    if state == "SLOW":
        # 🌊 Smooth breathing
        val = breathing(t, speed=1)
        set_leds(val, val//2, val//3)

    elif state == "BUILD":
        # ▶️ Forward sequence R → G → B
        phase = (phase + 1) % 3
        if phase == 0:
            set_leds(255, 0, 0)
        elif phase == 1:
            set_leds(0, 255, 0)
        else:
            set_leds(0, 0, 255)

    elif state == "DROP":
        # ◀️ Reverse sequence B → G → R
        phase = (phase - 1) % 3
        if phase == 0:
            set_leds(255, 0, 0)
        elif phase == 1:
            set_leds(0, 255, 0)
        else:
            set_leds(0, 0, 255)

    else:
        # ⚖️ Stable glow
        val = int(e * 255)
        set_leds(val, val//2, val//3)

    prev_energy = e

    root.after(80, update)

# ==============================
# ▶️ START
# ==============================
update()
root.mainloop()

sd.wait()
ser.close()