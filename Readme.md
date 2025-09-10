# Salt - Mouse & Keyboard Automation Tool

中文使用者参阅 [ReadmeCN.md](ReadmeCN.md) 。

Salt is a lightweight, cross-platform automation tool built with Python. It allows you to record mouse positions and create custom keyboard shortcuts to trigger actions, such as clicking at specific coordinates or remapping one key to another. Designed for efficiency, Salt operates primarily through global hotkeys, enabling you to automate repetitive tasks without interrupting your workflow.

**Author:** Momster
**Version:** v1.2.0-dev+5e0910v2
**License:** GNU General Public License v3.0
**Repository:** [github.com/tmomster/salt](https://github.com/tmomster/salt)
**Last Edited:** 2025.07.21

---

## 🚀 Features

* **Mouse Position Recording:** Click anywhere on your screen to record its coordinates and assign a hotkey to replay that click (left or right button).
* **Key Remapping:** Map one keyboard key or combination to trigger another key or combination.
* **Dual Modes:**
  * **Edit Mode:** Configure your mouse actions and key mappings.
  * **Work Mode:** Activate all your configured shortcuts for use.
* **Persistent Configuration:** Your settings are automatically saved to `mouse_agent_data.json` and loaded on startup.
* **Minimalist Mode:** Toggle to a tiny, unobtrusive window when you need more screen space.
* **Multi-Language Support:** Switch between English and Chinese interfaces.
* **Built-in Help:** Access a comprehensive guide and key reference table directly within the application.

---

## 🎯 Usage

After launching Salt, you will be greeted by its main interface. The application starts in **Edit Mode**.

### Recording a Mouse Click

1. Navigate to the "Mouse Actions" tab.
2. In the "Record Click" section, enter the desired **Hotkey** (e.g., `q`).
3. (Optional) Set a **Delay** in seconds before the click is executed.
4. Click the "Start Recording" button.
5. Move your cursor and click anywhere on the screen. The position and button type (left/right) will be recorded.
6. The recorded action will appear in the "Mouse Record" list.

### Creating a Key Mapping

1. Navigate to the "Key Mapping" tab.
2. In the "Key Mapping" section, enter the **Trigger** key (e.g., `c`).
3. Enter the **Target** key that you want to be pressed (e.g., `delete`).
4. Click the "Add Mapping" button.
5. The mapping will appear in the "Key Mapping List".

### Activating Your Shortcuts

* Press **F6** to toggle from Edit Mode to **Work Mode**. In Work Mode, all your configured hotkeys and key mappings become active.
* Press **F6** again to return to Edit Mode and suspend all shortcuts.

### Global Hotkeys

* **F6:** Toggle between Edit Mode and Work Mode.
* **F4:** Exit the Salt application.
* **F1:** Open the Help window.
* **— (Minimize Button):** Toggle Minimalist Mode.

---

## 📥 Installation

1. **Prerequisites:** Ensure you have Python 3.7 or higher installed on your system.

2. **Clone the Repository:**
   
   ```bash
   git clone https://github.com/tmomster/salt.git
   cd salt
   ```

3. **Install Dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```
   
   *(Note: If a `requirements.txt` file is not provided in the repo, you will need to install the required packages manually: `pip install tkinter keyboard pynput`)*

4. **Run the Application:**
   
   ```bash
   python main.py
   ```
   
   *(Replace `main.py` with the actual filename if it's different.)*

---

## 🛠️ Requirements

* Python 3.7+
* `tkinter` (Usually comes with Python)
* `keyboard`
* `pynput`

Install the Python dependencies using pip:

```bash
pip install keyboard pynput
```

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Feedback

For bugs, feature requests, or questions, please open an issue on the GitHub repository: [github.com/tmomster/salt/issues](https://github.com/tmomster/salt/issues).

---

## ⚠️ Disclaimer

This tool is provided "as is" without any warranties. Use it responsibly and ethically. The author is not responsible for any unintended consequences or misuse of the software.

---

© 2024-2025 Momster. All rights reserved.
