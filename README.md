# BWINF 2024 - Problem Solutions

Welcome to our collection of solutions for **BWINF 2024** (Bundeswettbewerb Informatik 2024), the prestigious Computer Science Olympiad in Germany. Each problem has been tackled using **custom-designed algorithms** implemented in Python, reflecting our unique problem-solving approach.

For detailed explanations of the tasks and solutions, refer to the accompanying PDF documentation. Notably, the explanation for **Task 5** is provided in English for accessibility.

---

## Tasks Overview

### **Task 3: Wandertag** *(Hiking Day)*

The Informatik-Gesundheitskasse (IGK) organizes an annual hiking event. However, many members hesitate to join because the routes are either too long or too short. 

To encourage participation, members were surveyed to specify their preferred minimum and maximum route lengths. A member will participate if a route falls within this range.

**Our Goal**:  
We developed an algorithm to calculate **three optimal route lengths** that maximize member participation. The program outputs the total number of participants and specifies which members participate in each route.

---

### **Task 4: Krocket** *(Croquet)*

Laura is playing croquet and discovers a sequence of gates. Inspired by her father's claim of passing all gates in order with just two hits, she wonders if it's possible to do this in a single hit.

**Our Goal**:  
Our solution checks whether all gates can be passed in sequence with a **single hit** and determines the best **starting point** and **direction**. 

To simplify the initial calculation, we assume the ball has no radius (`r = 0`). This allows us to focus on the geometric problem before introducing complexities.

---

### **Task 5: Das ägyptische Grabmal** *(The Egyptian Tomb)*

Petra faces a corridor leading to an Egyptian tomb, where each section is blocked by a periodically moving stone slab. The slabs alternate between blocking and unblocking based on their respective periods.

To navigate the corridor:
1. Petra must wait for a section to be unblocked.
2. She can move to an adjacent section only if both sections are unblocked simultaneously.

**Example**:  
For slabs with periods `5, 8, 12`, Petra can:
- Wait 8 minutes.
- Move to section 2.
- Wait 4 minutes.
- Move to section 3 and reach the tomb.

**Our Goal**:  
Using a custom algorithm, we calculate the **fastest route** through the corridor. The program outputs step-by-step instructions, such as when to wait and where to move. The explanation for this task is fully documented in English.

---

## About the Solutions

For each task, we designed and implemented our own algorithms, emphasizing efficiency, clarity, and correctness. These solutions demonstrate our ability to approach problems creatively while ensuring practical, executable results.

---

### Running the Programs

To explore the solutions:
1. Open the relevant task's Python script.
2. Run the program in your Python environment.
3. Follow the prompts or provide inputs as specified in the task's documentation.

---

Happy exploring, and good luck with your own coding problems! 😊
