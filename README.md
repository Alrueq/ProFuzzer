# 🎯 Pro-Fuzzer v4.0 (Auto-Exploit Edition)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Pro-Fuzzer** is a high-performance, multithreaded web directory brute-forcing tool with an integrated **Auto-Exploit Engine**. It doesn't just find hidden directories; it automatically tests discovered endpoints for common vulnerabilities like SQL Injection (SQLi), Cross-Site Scripting (XSS), and Local File Inclusion (LFI) using universal parameter fuzzing.

---

## ⚠️ LEGAL DISCLAIMER (PLEASE READ)

**FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY.**

This tool is designed to assist security researchers and students in authorized penetration testing environments. 
1. **The developer (and the tool) provides NO WARRANTY or GUARANTEE of any kind.**
2. **The user is solely responsible for any damage caused to any system.**
3. **Usage of this tool for attacking targets without prior mutual consent is illegal.** 4. **By using this software, you agree that the developer will not be held liable for any legal actions, damages, or consequences arising from the use of this code.**

---

## ✨ Key Features

* **🚀 Multithreaded Engine:** High-speed scanning using Python's `ThreadPoolExecutor`.
* **🕵️‍♂️ Universal Parameter Fuzzing:** Automatically detects and tests common web parameters (`id`, `cat`, `query`, etc.).
* **💣 Auto-Exploit Module:** Built-in payload delivery for:
  * **SQL Injection (SQLi):** Database error signature detection.
  * **Cross-Site Scripting (XSS):** Reflected script execution testing.
  * **Local File Inclusion (LFI):** Sensitive file access simulation.
* **🖥️ Modern GUI:** Sleek, dark-themed interface built with `customtkinter`.
* **📊 Real-time Dashboard:** Track RPS, discovered directories, and critical vulnerabilities instantly.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Alrueq/Pro-Fuzzer.git](https://github.com/Alrueq/Pro-Fuzzer.git)
   cd Pro-Fuzzer
