from tkinter import Tk, filedialog, messagebox
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from gtts import gTTS
import subprocess
import os

# Set the path to the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to select an image file
def select_image():
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    return file_path

# Function to enhance the image for better OCR accuracy
def enhance_image(image_path):
    try:
        image = Image.open(image_path)
        # Convert to grayscale
        image = ImageOps.grayscale(image)
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Adjust contrast factor as needed
        # Apply thresholding
        image = image.point(lambda p: p > 128 and 255)
        return image
    except Exception as e:
        messagebox.showerror("Error", f"Image enhancement failed: {str(e)}")
        return None

# Main function
def image_to_speech():
    while True:
        image_path = select_image()
        if not image_path:
            messagebox.showinfo("Info", "No file selected. Exiting.")
            break

        try:
            # Enhance the image
            enhanced_image = enhance_image(image_path)
            if not enhanced_image:
                continue
            
            # Extract text from the enhanced image
            text = pytesseract.image_to_string(enhanced_image)
            
            if text.strip():
                print("Extracted Text:")
                print(text)
                
                # Convert text to speech
                tts = gTTS(text)
                audio_path = filedialog.asksaveasfilename(
                    title="Save Audio As",
                    defaultextension=".mp3",
                    filetypes=[("MP3 Files", "*.mp3")]
                )
                if audio_path:
                    tts.save(audio_path)
                    print(f"Speech saved as {audio_path}")
                    
                    # Play the audio file
                    if os.name == "nt":  # Windows
                        os.system(f"start {audio_path}")
                    elif os.name == "posix":  # macOS/Linux
                        subprocess.run(["xdg-open", audio_path] if "linux" in os.sys.platform else ["open", audio_path])
                else:
                    print("Audio file not saved.")
            else:
                messagebox.showinfo("Info", "No text found in the image.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Ask if the user wants to process another image
        if not messagebox.askyesno("Continue", "Do you want to process another image?"):
            break

if __name__ == "__main__":
    image_to_speech()
