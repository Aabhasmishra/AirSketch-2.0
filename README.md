# 🖌️ AirSketch 2.0 – Draw with Your Hands!

AirSketch 2.0 is a virtual painting application that transforms your hand into a digital paintbrush. By leveraging computer vision, it allows you to draw in mid-air using your webcam.

---

## ✨ Features

- 🎨 **Air Drawing**: Draw in the air using your index finger tracked via webcam.
- 🖌️ **Color Picker**: Activate the color picker by touching the color picker icon with two fingers to select from a range of colors.
- 🔄 **Undo/Redo**: Easily undo or redo your last strokes to correct mistakes or revisit previous steps.
- 📏 **Brush Thickness Adjustment**: Modify the thickness of your brush strokes through intuitive gestures.
- 🧽 **Eraser Mode**: Switch to eraser mode to remove unwanted parts of your drawing.
- 📷 **Webcam-Based Hand Tracking**: Utilize your webcam to track hand movements in real-time.
- 🤖 **Powered by OpenCV and MediaPipe**: Leverages advanced computer vision libraries for accurate hand tracking and drawing.


---

## 📸 Screenshots



Drawing in Action[AirSketch 2 0 1](https://github.com/user-attachments/assets/d46026dd-40cd-42ac-a36c-d7fce4cda015)

Color Selection Interface![AirSketch 2 0 2](https://github.com/user-attachments/assets/09ac695c-ac00-4cd2-bc93-35bee75be450)

Eraser Mode Screenshot![AirSketch 2 0 3](https://github.com/user-attachments/assets/8ddcc98e-60f2-472b-b07c-a3bcedb8fef9)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- OpenCV

### Installation

```bash
git clone https://github.com/Aabhasmishra/AirSketch-2.0.git
cd AirSketch-2.0
pip install opencv-python
```

## 🚀 Running the App

To start the virtual drawing tool, run the following command in your terminal:

```bash
python main.py
```

---

## 🧠 How It Works

AirSketch 2.0 uses computer vision to detect your hand gestures and translate them into drawing actions. Here's a breakdown of the logic:

- 🖐️ **Hand Tracking**: Utilizes MediaPipe to detect and track your hand and fingers using a webcam.
- ☝️ **Drawing Mode**: When only the index finger is up, it draws on the canvas at the fingertip's position.
- ✌️ **Selection Mode**: When both the index and middle fingers are up, the app checks if you're selecting a color/tool from the top header area.
- 🧽 **Eraser Mode**: When the eraser is selected, it draws a thick white line over previous drawings to simulate erasing.
- 🧠 **Smart Switching**: The system intelligently switches between drawing, selecting, and erasing based on finger gestures.
- 📸 **Real-Time Rendering**: A transparent canvas is layered on top of the webcam feed to render strokes instantly.

The core logic is handled in `main.py` with hand tracking provided by the `handtrackingmodule.py` script.

---

## 🗂️ Project Structure

- `Header/` – Toolbar icons and header UI assets  
- `handtrackingmodule.py` – Custom module for hand tracking using MediaPipe  
- `main.py` – Main script with drawing, color selection, undo/redo logic  
- `README.md` – Project documentation
