# Invisibility Cloak README

## Introduction
Welcome to the **Invisibility Cloak** project—designed to bring a magical experience straight out of the wizarding world to the realm of Muggles using computer vision and OpenCV! This project allows you to disappear with the help of a cloak, much like the legendary invisibility cloak Harry Potter himself used. With a few spells (or lines of Python), you can watch yourself vanish before your very eyes.

The cloak should ideally be a **single color** to ensure the magic works effectively and seamlessly conceals you.

## Prerequisites

- **Python 3.x**
- Required Magical Libraries (Python Libraries):
  - OpenCV (`opencv-python`)
  - Numpy

Install these dependencies with the following incantation:

```sh
pip install opencv-python numpy
```

## How to Run the Code

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/UmarYaksambi/The_Invisiblity_Cloak.git
   cd The_Invisiblity_Cloak
   ```

2. **Run the Spell (Code):**
   Execute the following incantation in your terminal:
   ```sh
   python Cloak.py
   ```

3. **Magic Unfolds:**
   The spell comprises three magical steps:
   - **Step 1:** Capturing the Background (like casting a charm to freeze the scenery)
   - **Step 2:** Cloak Authentication (ensuring the cloak is truly magical)
   - **Step 3:** Cloak Disappearance Effect (witness the magic as you vanish)

## Application Workflow

### Step 1: Capture the Background
- Begin by **stepping out of the frame** completely, much like leaving the room for Dobby to work his elf-magic!
- A **loading indicator** will appear on-screen as the background is being captured.
- If a **human presence** is detected, the application will raise an `"Intruder Alert: Step Away for Cloak Activation"` warning (because only wizards know how to perform magic).
- Once the coast is clear, the background is captured and saved—ready to assist in your grand vanishing act.

### Step 2: Authenticate the Cloak
- The next step is to **display the cloak** (a solid-colored fabric) so that the application can determine if it’s enchanted.
- A **loading indicator** appears once more.
- The cloak’s color is analyzed and authenticated by capturing the **average HSV value** from the central region of the frame. 
- If authenticated, a success message will be displayed—congratulations, you now hold a real invisibility cloak!

### Step 3: Disappear (It’s Magic Time!)
- With the background captured and the cloak verified, it’s time to witness magic.
- Simply **wear the cloak**, and watch in awe as it is recognized and replaced by the captured background.
- The rest of the frame remains unaffected, creating the mystical illusion that the wearer has truly disappeared.

## Key Magical Features
- **Human Detection:** Like the **Marauder's Map**, the application uses a detection mechanism (Histogram of Oriented Gradients) to ensure no prying eyes are around during background capture.
- **Background Capture:** Enchants the scenery so it can later be summoned to replace the cloak.
- **Cloak Authentication:** Ensures only a true invisibility cloak works—any ordinary blanket just won’t do!
- **Invisibility Effect:** The cloak is magically replaced with the background, making the wearer vanish.

## Running the Spell Step-by-Step

1. **Start the Magic:**
   - After chanting (running the script), a window named **"Invisibility Cloak - Get ready to disappear!"** will appear.
   - A prompt saying `"Press Esc to exit"` is displayed in case you need to reverse the magic.

2. **Capture the Background:**
   - The application checks for any Muggles or creatures in the frame.
   - If a human presence is detected, `"Intruder Alert: Step Away for Cloak Activation"` will appear until the frame is empty.
   - Once the frame is clear, the background is captured, and the scenery is frozen.

3. **Authenticate Your Cloak:**
   - After background capture, you’ll be prompted to present your cloak.
   - The spell `"Is your cloak truly enchanted?"` will be displayed, indicating it's time to **hold the cloak** in front of the camera.
   - Once successfully authenticated, the cloak’s enchantment is captured and prepared for the final magic.

4. **Disappear with the Cloak:**
   - With the background and cloak prepared, **don the cloak** and watch the magic happen.
   - The cloak region is replaced with the captured background, and behold—you’re invisible!
   - To undo the magic and exit, press the **Esc** key.

## Notes for Aspiring Wizards
- The cloak must be **single-colored**—this is key to make the magic work properly.
- It’s best to perform this magic in a **well-lit area**, as darkness will weaken the effect.
- Ensure the cloak **covers enough of yourself** to make the disappearance impressive.
- During background capture and cloak authentication, **stay still**—even the best wizards need focus.

## Troubleshooting your Magic
- **Intruder Alert Won't Disappear:** Make sure all Muggles and magical creatures step out of the frame.
- **Cloak Not Detected Properly:** Try using a bright, unique color—avoid colors that blend with your background or surroundings.
- **No Effect When Wearing Cloak:** Hold the cloak in the center for authentication and ensure it’s a mono-color fabric.

## License
This project is open to all wizards and Muggles under the **MIT License**—feel free to use, modify, and share, so long as you don't use it for anything dark and sinister.

May your journey to mastering the magic of invisibility be filled with wonder and fun! ⚡✨
