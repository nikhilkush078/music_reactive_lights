import librosa
import numpy as np
import sounddevice as sd
import time
import tkinter as tk

# ==============================
# 🎧 LOAD AUDIO
# ==============================
FILE = "character_dheela.mp3"
y, sr = librosa.load(FILE, sr=None)

# ==============================
# 🎚️ FREQUENCY ANALYSIS
# ==============================
S = np.abs(librosa.stft(y, n_fft=1024, hop_length=512))

energy = np.mean(S, axis=0)
energy /= np.max(energy)

# ==============================
# 💡 TKINTER SETUP
# ==============================
root = tk.Tk()
root.title("Smart RGB LED + Ambient Strip")

canvas = tk.Canvas(root, width=400, height=300, bg="black")
canvas.pack()

# 🔴 RGB LEDs (top)
led_r = canvas.create_oval(50, 50, 120, 120, fill="#000000")
led_g = canvas.create_oval(160, 50, 230, 120, fill="#000000")
led_b = canvas.create_oval(270, 50, 340, 120, fill="#000000")

# 🌈 LED STRIP (bottom)
strip = canvas.create_rectangle(20, 200, 380, 260, fill="#101010")

# ==============================
# 🎵 PLAY AUDIO
# ==============================
sd.play(y, sr)
start_time = time.time()

prev_energy = 0
phase = 0

# For smooth ambient strip
smooth_energy = 0.3  # initial base

# ==============================
# 🎨 HELPER FUNCTIONS
# ==============================
def set_leds(r, g, b):
    canvas.itemconfig(led_r, fill=f'#{r:02x}0000')
    canvas.itemconfig(led_g, fill=f'#00{g:02x}00')
    canvas.itemconfig(led_b, fill=f'#0000{b:02x}')

def set_strip(r, g, b):
    canvas.itemconfig(strip, fill=f'#{r:02x}{g:02x}{b:02x}')

def breathing(t, speed=1):
    val = int((0.5 + 0.5*np.sin(t * speed)) * 255)
    return val

# ==============================
# 🔄 UPDATE LOOP
# ==============================
def update():
    global prev_energy, phase, smooth_energy

    t = time.time() - start_time
    idx = int(t * sr / 512)

    if idx >= len(energy):
        return

    e = energy[idx]

    # 🔽 Smooth energy (LOW PASS FILTER)
    smooth_energy = 0.95 * smooth_energy + 0.05 * e

    diff = e - prev_energy

    # ==============================
    # 🎯 STATE LOGIC (FAST LEDs)
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
    # 🎨 FAST LED EFFECTS
    # ==============================
    if state == "SLOW":
        val = breathing(t, speed=1)
        set_leds(val, val, val)

    elif state == "BUILD":
        phase = (phase + 1) % 3
        if phase == 0:
            set_leds(255, 0, 0)
        elif phase == 1:
            set_leds(0, 255, 0)
        else:
            set_leds(0, 0, 255)

    elif state == "DROP":
        phase = (phase - 1) % 3
        if phase == 0:
            set_leds(255, 0, 0)
        elif phase == 1:
            set_leds(0, 255, 0)
        else:
            set_leds(0, 0, 255)

    else:
        val = int(e * 255)
        set_leds(val, val//2, val//3)

    # ==============================
    # 🌈 AMBIENT STRIP (NEW 🔥)
    # ==============================

    base = 80  # NEVER OFF brightness
    variation = int(smooth_energy * 100)  # small variation

    # Slow color cycling
    r = base + variation + int(20 * np.sin(t * 0.5))
    g = base + variation + int(20 * np.sin(t * 0.7 + 2))
    b = base + variation + int(20 * np.sin(t * 0.9 + 4))

    # Clamp values
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    set_strip(r, g, b)

    prev_energy = e

    root.after(80, update)

# Start
update()
root.mainloop()
sd.wait()