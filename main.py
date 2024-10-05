import cv2
import numpy as np
import handtrackingmodule as htm  # Import the hand tracking module

# Define brush thickness and eraser thickness
brushThickness = 25
eraserThickness = 70
drawColor = (82, 113, 255)  # Default color (BGR format for OpenCV)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas to draw on

# Create undo and redo stacks
undo_stack = []
redo_stack = []

cap = cv2.VideoCapture(0)  # Capture video from webcam
cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

detector = htm.handDetector(detectionCon=0.50, maxHands=1)  # Initialize hand detector

# Define button areas
# headerHeight = 70  # Reduced header height
colorPickerButtonArea = (50, 20, 265, 60)  # Color Picker button area (x1, y1, x2, y2)
eraserButtonArea = (290, 20, 410, 60)  # Eraser button area (x1, y1, x2, y2)
undoButtonArea = (435, 20, 535, 60)  # Undo button area
redoButtonArea = (550, 20, 645, 60)  # Redo button area
increaseBrushButtonArea = (670, 20, 715, 60)  # Increase Brush Thickness button area
decreaseBrushButtonArea = (805, 20, 850, 60)  # Decrease Brush Thickness button area

eraserMode = False  # Initial state of eraser mode

# Define a new color palette (BGR values for 36 distinct colors)
colorPalette = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255),  # Bright colors
    (255, 165, 0), (128, 0, 128), (255, 192, 203), (139, 69, 19), (128, 128, 128), (0, 0, 0),  # Varied tones
    (255, 255, 255), (173, 216, 230), (0, 0, 139), (144, 238, 144), (255, 215, 0), (255, 105, 180),  # Light and pastel colors
    (230, 230, 250), (75, 0, 130), (255, 218, 185), (255, 127, 80), (250, 128, 114), (210, 180, 140),  # Shades and tints
    (0, 128, 128), (0, 0, 128), (255, 215, 0), (192, 192, 192), (135, 206, 235), (255, 250, 205),  # More variations
    (127, 255, 0), (240, 128, 128), (255, 99, 71), (210, 105, 30), (65, 105, 225), (255, 20, 147)  # Last set
]

# Function to save canvas state for undo
def save_canvas_state():
    global imgCanvas
    # Push the current state to undo stack
    undo_stack.append(imgCanvas.copy())  # Save a copy of the current canvas

# Function to display the color picker
def show_color_picker():
    global drawColor, eraserMode  # Include eraserMode to modify it

    # Create a larger window for the color picker
    colorPickerCanvas = np.zeros((670, 670, 3), np.uint8)  # Updated size for 6x6 layout
    block_size = 100  # Size of each color block (100x100 pixels)
    gap = 10  # Gap between color blocks

    # Starting positions for the first color block to include the gap
    start_x_offset = 10  # 10 pixels from the left
    start_y_offset = 10  # 10 pixels from the top
    hovered_box_index = -1  # No box hovered initially

    while True:
        for i, color in enumerate(colorPalette):
            start_x = start_x_offset + (i % 6) * (block_size + gap)  # 6 blocks in a row
            start_y = start_y_offset + (i // 6) * (block_size + gap)  # 6 blocks in a column
            end_x = start_x + block_size
            end_y = start_y + block_size

            # Fill the box with the original color
            cv2.rectangle(colorPickerCanvas, (start_x + 2, start_y + 2), (end_x - 2, end_y - 2), color, -1)

            # Draw the border around the color block
            cv2.rectangle(colorPickerCanvas, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)

            # Highlight the box if it's hovered over by drawing a yellow border
            if hovered_box_index == i:
                cv2.rectangle(colorPickerCanvas, (start_x, start_y), (end_x, end_y), (0, 255, 255), 4)

        # Capture the frame to detect hand gestures
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Flip to avoid mirror inversion
        img = detector.findHands(img)  # Detect hands in the image
        lmList, bbox = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # Get the index finger tip position
            x1, y1 = lmList[8][1], lmList[8][2]

            # Track whether the finger is hovering over any box
            is_hovering_any_box = False

            # Check if the index finger is hovering over any color block
            for i, color in enumerate(colorPalette):
                start_x = start_x_offset + (i % 6) * (block_size + gap)
                start_y = start_y_offset + (i // 6) * (block_size + gap)
                end_x = start_x + block_size
                end_y = start_y + block_size

                if start_x < x1 < end_x and start_y < y1 < end_y:
                    hovered_box_index = i  # Highlight the currently hovered box
                    is_hovering_any_box = True

                    # Check if index and middle finger are closed to confirm the selection
                    fingers = detector.fingersUp()
                    if fingers[1] and not fingers[2]:
                        drawColor = color
                        eraserMode = False  # Disable eraser mode when selecting a color
                        cv2.destroyWindow("Color Picker")
                        return

            if not is_hovering_any_box:
                hovered_box_index = -1

            # Draw a smaller visual cursor at the tip of the index finger
            cv2.circle(colorPickerCanvas, (x1, y1), 10, (0, 0, 0), 2)

        cv2.imshow("Color Picker", colorPickerCanvas)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyWindow("Color Picker")
            break

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip
        x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip
        fingers = detector.fingersUp()

        # Detect if both index and middle fingers are up (hover)
        if fingers[1] and fingers[2]:
            # Check if hovering over color picker button
            if colorPickerButtonArea[0] < x1 < colorPickerButtonArea[2] and colorPickerButtonArea[1] < y1 < colorPickerButtonArea[3]:
                xp, yp = 0, 0
                show_color_picker()

            # Check if hovering over eraser button
            if eraserButtonArea[0] < x1 < eraserButtonArea[2] and eraserButtonArea[1] < y1 < eraserButtonArea[3]:
                eraserMode = True

            # Check if hovering over undo button
            if undoButtonArea[0] < x1 < undoButtonArea[2] and undoButtonArea[1] < y1 < undoButtonArea[3]:
                xp, yp = 0, 0
                if undo_stack:  # Only undo if there's something to undo
                    redo_stack.append(imgCanvas.copy())  # Push the current state to redo stack
                    imgCanvas = undo_stack.pop()  # Restore the last state from undo stack

            # Check if hovering over redo button
            if redoButtonArea[0] < x1 < redoButtonArea[2] and redoButtonArea[1] < y1 < redoButtonArea[3]:
                xp, yp = 0, 0
                if redo_stack:  # Only redo if there's something to redo
                    imgCanvas = redo_stack.pop()  # Restore the last state from redo stack

            # Check if hovering over increase brush thickness button
            if increaseBrushButtonArea[0] < x1 < increaseBrushButtonArea[2] and increaseBrushButtonArea[1] < y1 < increaseBrushButtonArea[3]:
                xp, yp = 0, 0
                brushThickness += 2  # Increase brush thickness
                brushThickness = min(brushThickness, 99)  # Limit to max thickness

            # Check if hovering over decrease brush thickness button
            if decreaseBrushButtonArea[0] < x1 < decreaseBrushButtonArea[2] and decreaseBrushButtonArea[1] < y1 < decreaseBrushButtonArea[3]:
                xp, yp = 0, 0
                brushThickness -= 2  # Decrease brush thickness
                brushThickness = max(brushThickness, 5)  # Limit to min thickness

        if fingers[1] and not fingers[2]:  # Drawing Mode
            save_canvas_state()  # Save the current canvas state before drawing

            if xp == 0 and yp == 0:  # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                xp, yp = x1, y1  # so to avoid that we set xp=x1 and yp=y1

            if eraserMode:
                # Draw a line for eraser
                xp, yp = x1, y1
                cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), eraserThickness)  # Eraser shown in black
                cv2.circle(img, (x1, y1), (eraserThickness // 2) + 3, (0, 0, 0), cv2.FILLED)  # Draw black circle at the eraser location
                cv2.circle(img, (x1, y1), eraserThickness // 2, (255, 255, 255), cv2.FILLED)  # Draw black circle at the eraser location

            else:
                # Draw a line for brush
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1  # Update previous x, y

    # Display the canvas and webcam feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)  # Apply the canvas to the webcam feed
    img = cv2.bitwise_or(img, imgCanvas)  # Combine the canvas with the webcam feed

    # Draw the header with buttons
    cv2.rectangle(img, colorPickerButtonArea[:2], colorPickerButtonArea[2:], (0, 0, 0), -1)  # Color Picker Button
    cv2.putText(img, 'Color Picker', (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.rectangle(img, eraserButtonArea[:2], eraserButtonArea[2:], (255, 255, 255), -1)  # Eraser Button
    cv2.putText(img, 'Eraser', (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.rectangle(img, undoButtonArea[:2], undoButtonArea[2:], (0, 165, 255), -1)  # Undo Button
    cv2.putText(img, 'Undo', (445, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.rectangle(img, redoButtonArea[:2], redoButtonArea[2:], (0, 165, 255), -1)  # Redo Button
    cv2.putText(img, 'Redo', (560, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.rectangle(img, increaseBrushButtonArea[:2], increaseBrushButtonArea[2:], (32, 90, 1), -1)  # Increase Brush Button
    cv2.putText(img, '+', (680, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.rectangle(img, decreaseBrushButtonArea[:2], decreaseBrushButtonArea[2:], (32, 90, 1), -1)  # Decrease Brush Button
    cv2.putText(img, '-', (815, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Draw brush thickness display box near the "+" and "-" buttons
    cv2.rectangle(img, (730, 20), (790, 60), (190, 190, 190), -1)  # Box to show brush thickness
    cv2.putText(img, f'{brushThickness}', (740, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Display the brush thickness

    # Display the combined image
    cv2.imshow("Virtual Paint", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q'
        break

cap.release()
cv2.destroyAllWindows()
