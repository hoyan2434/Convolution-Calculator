# **Convolution Simulator User Manual**

This README serves as the official documentation and user manual for the **Convolution Simulator**, a Python-based interactive tool designed to visualize 2D image convolution operations. It is particularly useful for students and researchers to understand how different kernels, padding types, and data ranges affect image processing.

## ---

**🚀 Features**

* **Real-Time Configuration:** Adjust padding, operations, and sizes instantly.  
* **Non-Destructive Matrix Resizing:** Change image or kernel dimensions without losing existing data; new cells are initialized as "null".  
* **Smart Numerical Formatting:** Values are automatically displayed as floats for terminating decimals and fractions for repeating decimals to maintain precision.  
* **Visual Padding Insight:** Distinct color-coding (cyan text and blue backgrounds) highlights padded regions in the input view.  
* **Advanced Sharpening:** Supports unsharp masking where you provide the blur kernel and alpha value to derive the final sharpening filter.

## ---

**🛠️ Installation**

Ensure you have Python 3.x installed along with the following dependencies:

Bash

pip install numpy scipy matplotlib

## ---

**📖 User Guide**

### **1\. Configuration (Top Panel)**

Configure the mathematical parameters for the convolution before entering data.

* **Padding Type:** \* zero: Pads the boundary with 0s.  
  * replicate: Replicates the edge pixels of the image.  
* **Operation:**  
  * blur: Standard convolution using the user-defined kernel.  
  * sharpen: Uses the formula $K \= (1 \+ \\alpha)I \- \\alpha B$, where $B$ is your input blur kernel and $\\alpha$ is the sharpening strength.  
* **Alpha ($\\alpha$):** Only used for sharpening; controls the intensity of the effect.  
* **Range:** Choose between \[0, 255\] for standard pixel values or \[0.0, 1.0\] for normalized values.  
* **Clip Output:** If enabled, ensures the output values stay within the selected data range.  
* **Matrix Sizes:** Enter dimensions (e.g., $4 \\times 4$ for Image, $3 \\times 3$ for Kernel) to update the input grids in real-time.

### **2\. Matrix Input (Middle Panel)**

* **Entering Data:** Click into the white boxes to type values. You can use integers, decimals, or fractions (e.g., 1/9 or 0.11).  
* **Navigation:** Use the **Tab** key to move horizontally through a row and automatically jump to the next row or the next matrix.  
* **Run Convolution:** Click this button after you have finished entering your matrix data to update the visualization.

### **3\. Visualization (Bottom Panel)**

The simulator displays three distinct views:

1. **Input (Padded):** Shows your image with the selected padding applied. Padded cells are highlighted in **cyan**.  
2. **Kernel Filter:** Shows the actual filter being applied. In sharpening mode, this displays the *derived* sharpen kernel.  
3. **Output:** The final result of the convolution.

## ---

**📐 Mathematical Precision**

The simulator prioritizes exactness:

* If a result is $1/3$, it will display **1/3**.  
* If a result is $0.1$, it will display **0.1**.

---

**Would you like me to add a "Troubleshooting" section to this README for common user errors?**
