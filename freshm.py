from sympy import symbols, simplify_logic, sympify, And, Or, Not
import time
import re
import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import os  # For macOS Siri voice

digital_logic_data = {
    "boolean algebra": {
        "concept": "Boolean algebra is a branch of algebra that deals with true/false values, represented as 1 and 0, using operations like AND, OR, and NOT.",
        "formulas": [
            "x + 0 = x",
            "x + 1 = 1",
            "x . 1 = x",
            "x . 0 = 0",
            "x + x' = 1",
            "x . x' = 0",
            "x + yz = (x + y) (x + z)",
            "x(y+z) = xy + xz"
        ]
    },
    "flip flop": {
        "concept": "A flip-flop is a basic memory element in digital electronics used for storing a single bit of data. Types include SR, D, JK, and T flip-flops.",
        "formulas": [
            "SR Flip-Flop: Q(n+1) = S + Q(n)R'",
            "D Flip-Flop: Q(n+1) = D",
            "JK Flip-Flop: Q(n+1) = JQ' + K'Q",
            "T Flip-Flop: Q(n+1) = T ⊕ Q"
        ]
    }
}

def preprocess_expression(expression_str):
    expression_str = expression_str.replace("'", "~").replace(" ", "")
    expression_str = re.sub(r'([A-Za-z0-9])([A-Za-z0-9~])', r'\1 & \2', expression_str)
    expression_str = expression_str.replace("+", "|").replace(")(", ") & (")
    return expression_str

def optimize_circuit(expression_str):
    try:
        expression_str = preprocess_expression(expression_str)
        variables = set(re.findall(r'[A-Za-z]', expression_str))
        symbols_dict = {var: symbols(var) for var in variables}
        expression = sympify(expression_str, locals={**symbols_dict, 'And': And, 'Or': Or, 'Not': Not})
        start_time = time.time()
        optimized_expr = simplify_logic(expression, form='dnf')
        end_time = time.time()
        reduction_percentage = 100 - (len(str(optimized_expr)) / len(expression_str)) * 100
        return f"✨ Original: {expression_str}\n✅ Optimized: {optimized_expr}\n⏳ Time: {end_time - start_time:.6f} sec\n📉 Reduction: {reduction_percentage:.2f}%"
    except Exception as e:
        return f"❌ Error: {e}\nInvalid Boolean expression."

def number_conversion(conversion_type, value):
    try:
        if conversion_type == 1:
            return f"🔢 Binary: {bin(int(value, 16))[2:]}"
        elif conversion_type == 2:
            return f"🔢 Decimal: {int(value, 2)}"
        elif conversion_type == 3:
            return f"🔢 Hexadecimal: {hex(int(value))[2:].upper()}"
        else:
            return "❌ Invalid choice."
    except Exception as e:
        return f"❌ Error: {e}\nInvalid input."

def speak(text):
    os.system(f'say "{text}"')

def get_concept_explanation(concept):
    concept = concept.lower()
    for key in digital_logic_data.keys():
        if concept in key:
            data = digital_logic_data[key]
            explanation = data["concept"]
            formulas = "\n".join(data["formulas"]) if data["formulas"] else "No specific formulas available."
            response = f"📚 Concept: {explanation}\n📝 Formulas:\n{formulas}"
            messagebox.showinfo("Concept Explanation", response)
            speak(explanation)
            speak("Now, let me explain the formulas.")
            speak(formulas)
            return response
    return "❌ Concept not found. Try again!"

def main():
    root = tk.Tk()
    root.withdraw()
    while True:
        choice = simpledialog.askinteger("🔧 Digital Logic Tool", "Choose an option:\n1️⃣ Boolean Algebra Optimization\n2️⃣ Number System Conversion\n3️⃣ Ask Concept from Digital Logic\n4️⃣ ❌ Exit")
        if choice == 1:
            expr = simpledialog.askstring("✨ Boolean Optimization", "Enter Boolean Expression:")
            result = optimize_circuit(expr)
            messagebox.showinfo("✅ Optimization Result", result)
        elif choice == 2:
            conversion_type = simpledialog.askinteger("🔢 Conversion", "1️⃣ Hex to Binary\n2️⃣ Binary to Decimal\n3️⃣ Decimal to Hex")
            value = simpledialog.askstring("🔢 Input", "Enter value:")
            result = number_conversion(conversion_type, value)
            messagebox.showinfo("🔢 Conversion Result", result)
        elif choice == 3:
            concept = simpledialog.askstring("📚 Ask Concept", "Enter the topic/concept:")
            if concept:
                result = get_concept_explanation(concept)
                messagebox.showinfo("📚 Concept Explanation", result)
            else:
                messagebox.showerror("❌ Error", "Please enter a valid concept.")
        elif choice == 4:
            break
        else:
            messagebox.showerror("❌ Error", "Invalid choice. Try again.")
    root.destroy()

if __name__ == "__main__":
    main()
