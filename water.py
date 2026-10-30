import tkinter as tk
from datetime import datetime
import threading
import subprocess
import winsound
import time
import sys

# =========================================================
# SETTINGS
# =========================================================

INTERVAL = 15 * 60   # 15 minutes


# =========================================================
# VOICE
# =========================================================

def speak():
    try:
        powershell_command = (
            'Add-Type -AssemblyName System.Speech; '
            '$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            '$speaker.Speak("Drink Water Sahab")'
        )

        subprocess.Popen(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell_command
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    except Exception as e:
        print(f"\n[VOICE ERROR] {e}")


# =========================================================
# SOUND
# =========================================================

def play_sound():
    try:
        winsound.Beep(1000, 250)
        winsound.Beep(1300, 250)
        winsound.Beep(1000, 250)

    except Exception:
        winsound.MessageBeep()


# =========================================================
# WATER REMINDER POPUP
# =========================================================

def show_reminder():

    print()
    print("=" * 55)
    print("💧  DRINK WATER SAHAB")
    print("=" * 55)

    # Sound
    play_sound()

    # Voice
    threading.Thread(
        target=speak,
        daemon=True
    ).start()

    # Popup
    popup = tk.Toplevel(main_root)

    popup.title("💧 Water Reminder")
    popup.geometry("450x280")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)
    popup.configure(bg="#F4FBFF")

    # Center popup
    popup.update_idletasks()

    width = 450
    height = 280

    x = (popup.winfo_screenwidth() - width) // 2
    y = (popup.winfo_screenheight() - height) // 2

    popup.geometry(f"{width}x{height}+{x}+{y}")

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = tk.Label(
        popup,
        text="💧 DRINK WATER",
        font=("Segoe UI", 25, "bold"),
        bg="#F4FBFF",
        fg="#087EA4"
    )

    title.pack(pady=(30, 8))

    # -----------------------------------------------------
    # MESSAGE
    # -----------------------------------------------------

    message = tk.Label(
        popup,
        text=(
            "Drink some water, Sahab!\n\n"
            "🪑 Sit Straight\n"
            "🧘 Relax Your Shoulders"
        ),
        font=("Segoe UI", 14),
        bg="#F4FBFF",
        fg="#263238",
        justify="center"
    )

    message.pack()

    # -----------------------------------------------------
    # OK BUTTON
    # -----------------------------------------------------

    button = tk.Button(
        popup,
        text="✓  OK",
        font=("Segoe UI", 13, "bold"),
        width=12,
        bg="#087EA4",
        fg="white",
        activebackground="#066783",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=popup.destroy
    )

    button.pack(pady=20)

    popup.focus_force()


# =========================================================
# CMD COUNTDOWN
# =========================================================

def countdown():

    remaining = INTERVAL

    while remaining >= 0:

        minutes = remaining // 60
        seconds = remaining % 60

        # Live CMD timer
        sys.stdout.write(
            f"\r⏱️  Next reminder in: "
            f"{minutes:02d}:{seconds:02d}   "
        )

        sys.stdout.flush()

        time.sleep(1)

        remaining -= 1

    # -----------------------------------------------------
    # TIME REACHED
    # -----------------------------------------------------

    print()

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        "⏰ Reminder time reached!"
    )

    # Show popup on Tkinter main thread
    main_root.after(0, show_reminder)

    # Start another countdown
    main_root.after(
        1000,
        start_countdown
    )


# =========================================================
# START COUNTDOWN
# =========================================================

def start_countdown():

    threading.Thread(
        target=countdown,
        daemon=True
    ).start()


# =========================================================
# PROGRAM START
# =========================================================

print("=" * 60)
print("💧 WATER REMINDER PROGRAM STARTED")
print("=" * 60)

print("[INFO] Reminder interval : 15 minutes")
print("[INFO] Voice             : Drink Water Sahab")
print("[INFO] Sound             : ON")
print("[INFO] Popup             : ON")
print("[INFO] CMD countdown     : ON")
print("[INFO] Program is running...")
print()

# =========================================================
# HIDDEN TKINTER ROOT
# =========================================================

main_root = tk.Tk()
main_root.withdraw()

# Start first countdown
start_countdown()

# Keep program alive
main_root.mainloop()