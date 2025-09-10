import tkinter as tk
from tkinter import ttk, messagebox
import json
import keyboard
from pynput import mouse
import sys
import time
import threading

class MouseAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("Salt v1.2.0-dev+5e0910v2")
        self.root.geometry("850x700")
        self.root.configure(bg="#1e1e2e")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        self.center_window()
        
        self.drag_threshold = 5
        self.mouse_pressed = False
        self.is_dragging = False
        self.press_start_x = 0
        self.press_start_y = 0
        self.window_start_x = 0
        self.window_start_y = 0
        
        keyboard.add_hotkey('f4', self.quit_app)
        keyboard.add_hotkey('f6', self.toggle_mode)
        keyboard.add_hotkey('f1', self.show_help)
        
        self.positions = []
        self.key_mappings = []
        self.current_mode = "edit"
        self.working = False
        self.record_click = False
        self.is_minimal_mode = False
        self.current_language = "en"
        
        self.texts = {
            "en": {
                "title": "Salt v1.2.0-dev+5e0910v2",
                "mode_control": "Mode Control:",
                "suspend": "Suspended",
                "running": "Running",
                "save_config": "Save",
                "f6_toggle_mode": "F6: Mode",
                "f4_exit": "F4: Exit",
                "f1_help": "F1: Help",
                "mouse_actions": "Mouse Actions",
                "record_click": "Record Click",
                "hotkey": "Hotkey:",
                "delay_sec": "Delay (sec):",
                "start_recording": "Start",
                "mouse_action_list": "Mouse Record",
                "x_coord": "X",
                "y_coord": "Y",
                "key": "Key",
                "delay": "Delay",
                "button": "Button",
                "delete_selected": "Delete",
                "clear_list": "Clear",
                "key_mapping": "Key Mapping",
                "trigger_key": "From",
                "target_key": "To",
                "add_mapping": "Add",
                "key_mapping_list": "Key Mapping",
                "status_ready": "Ready",
                "status_edit_mode": "[Edit Mode] Ready",
                "status_work_mode": "[Work Mode] Running",
                "status_recording": "Recording in progress...",
                "status_recorded": "[Recorded] Mapped from {key} to (x:{x}, y:{y})",
                "status_mapped": "[Recorded] Mapped from {trigger} to {target}",
                "confirm_clear": "Warning",
                "confirm_clear_msg": "You are about to clear all action mappings in this list.\nYou can still cancel before clicking Confirm.",
                "confirm": "Confirm",
                "cancel": "Cancel",
                "warning": "Warning",
                "error": "Error",
                "invalid_key": "Invalid key name (e.g., 'a', 'ctrl+c', 'delete')",
                "fields_required": "Both fields are required",
                "save_success": "Configuration saved successfully!",
                "save_failed": "Save failed: {error}",
                "load_failed": "Load failed: {error}",
                "minimal_restore": "Standard Mode",
                "language": "Language",
                "help_title": "Help",
                "program_intro": "Program Introduction",
                "key_reference": "Key Reference Table",
                "intro_content": "Salt is an automation tool that allows you to record mouse positions and create keyboard shortcuts to trigger actions. You can map keys to simulate clicks at specific coordinates or remap one key to another. Press F6 to toggle between edit and work modes. In work mode, your configured shortcuts become active.",
                "record_instructions": "To record a mouse position:\n1. Enter a hotkey (e.g., 'q')\n2. Set delay if needed\n3. Click 'Start Recording'\n4. Click anywhere on screen\n\nTo create key mapping:\n1. Enter trigger key (e.g., 'c')\n2. Enter target key (e.g., 'delete')\n3. Click 'Add Mapping'",
                "copyright": "© 2024 Momster. All rights reserved."
            },
            "zh": {
                "title": "SSalt v1.2.0-dev+5e0910v2",
                "mode_control": "模式控制:",
                "suspend": "挂起",
                "running": "进行中",
                "save_config": "保存方案",
                "f6_toggle_mode": "F6: 切换模式",
                "f4_exit": "F4: 退出程序",
                "f1_help": "F1: 帮助",
                "mouse_actions": "鼠标动作",
                "record_click": "录制鼠标点击",
                "hotkey": "快捷键:",
                "delay_sec": "延迟(秒):",
                "start_recording": "开始录制",
                "mouse_action_list": "鼠标动作列表",
                "x_coord": "X坐标",
                "y_coord": "Y坐标",
                "key": "快捷键",
                "delay": "延迟",
                "button": "按键",
                "delete_selected": "删除选中",
                "clear_list": "清空列表",
                "key_mapping": "键盘映射",
                "trigger_key": "触发",
                "target_key": "目标",
                "add_mapping": "添加映射",
                "key_mapping_list": "键盘映射列表",
                "status_ready": "就绪",
                "status_edit_mode": "[编辑模式] 就绪",
                "status_work_mode": "[工作模式] 进行中",
                "status_recording": "录制正在进行",
                "status_recorded": "[录制] 已从 {key} 映射到 (x:{x}, y:{y})",
                "status_mapped": "[录制] 已从 {trigger} 映射到 {target}",
                "confirm_clear": "警告",
                "confirm_clear_msg": "您正在清空此列表下的所有动作映射。\n在点击确认之前，您还可以取消。",
                "confirm": "确认",
                "cancel": "取消",
                "warning": "警告",
                "error": "错误",
                "invalid_key": "无效的按键名称 (例如: 'a', 'ctrl+c', 'delete')",
                "fields_required": "需要填写两个字段",
                "save_success": "配置已保存成功!",
                "save_failed": "保存失败: {error}",
                "load_failed": "加载失败: {error}",
                "minimal_restore": "回到标准模式",
                "language": "语言",
                "help_title": "帮助",
                "program_intro": "程序介绍",
                "key_reference": "按键映射方案表",
                "intro_content": "Salt是一款自动化工具，允许记录鼠标位置并创建键盘快捷键来触发动作。\n您可以将按键映射到特定坐标模拟点击，或重映射一个键到另一个键。\n按 F6 在编辑模式和工作模式之间切换。在工作模式下，您配置的快捷键将被激活。",
                "record_instructions": "录制鼠标位置：\n1. 输入快捷键（例如 'q'）\n2. 设置延迟（可选）\n3. 点击\"开始录制\"\n4. 在屏幕任意位置点击\n\n创建按键映射：\n1. 输入触发键（例如 'c'）\n2. 输入目标键（例如 'delete'）\n3. 点击\"添加映射\"",
                "copyright": "© 2024 Momster，保留所有权利。"
            }
        }
        
        self.current_colors = {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'status_fg': '#a6adc8',
            'active_fg': '#a6e3a1',
            'pause_fg': '#f38ba8',
            'hint_fg': '#6c7086',
            'separator': '#313244',
            'button_hover': '#313244',
            'window_border': '#585b70',
            'confirm_button': '#a6e3a1',
            'scrollbar_bg': '#313244',
            'scrollbar_thumb': '#6c7086',
            'treeview_bg': '#181825',
            'treeview_fg': '#cdd6f4',
            'treeview_header_bg': '#11111b',
            'treeview_header_fg': '#ffffff',
            'treeview_selected_bg': '#89b4fa',
            'treeview_selected_fg': '#1e1e2e',
            'accent': '#89b4fa',
            'danger': '#f38ba8',
            'warning': '#f9e2af',
            'success': '#a6e3a1'
        }
        
        self.key_reference = {
            "Letters(字母)": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                       "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            "Numbers(数字)": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "Function Keys(功能键)": ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"],
            "Navigation(导航)": ["up", "down", "left", "right", "page up", "page down", "home", "end"],
            "Editing(编辑)": ["backspace", "delete", "insert", "enter", "tab", "space", "escape", "caps lock"],
            "Modifiers(控制)": ["ctrl", "alt", "shift", "windows"],
            "Symbols(符号)": ["`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/", 
                       "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", 
                       "{", "}", "|", ":", "\"", "<", ">", "?"],
            "Numpad(小键盘)": ["num 0", "num 1", "num 2", "num 3", "num 4", "num 5", "num 6", "num 7", 
                      "num 8", "num 9", "num +", "num -", "num *", "num /", "num enter", "num ."],
            "Special(特殊)": ["print screen", "scroll lock", "pause", "menu"]
        }
        
        self.create_splash_screen()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_splash_screen(self):
        self.splash_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.splash_frame.pack(fill=tk.BOTH, expand=True)
        
        icon_canvas = tk.Canvas(self.splash_frame, width=120, height=120, bg="#1e1e2e", highlightthickness=0)
        icon_canvas.place(relx=0.5, rely=0.4, anchor="center")
        
        icon_canvas.create_oval(15, 15, 105, 105, outline="#89b4fa", width=4)
        icon_canvas.create_text(60, 60, text="M", font=("Helvetica", 48, "bold"), fill="#a6e3a1")
        
        self.momster_label = tk.Label(
            self.splash_frame,
            text="Momster",
            font=("Helvetica", 48, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        )
        self.momster_label.place(relx=0.5, rely=0.65, anchor="center")
        
        self.animate_splash()
        
    def animate_splash(self):
        for i in range(0, 101, 5):
            alpha = i / 100
            color = self.interpolate_color("#1e1e2e", "#a6e3a1", alpha)
            self.momster_label.config(fg=color)
            self.root.update()
            time.sleep(0.01)
            
        time.sleep(0.3)
        
        for i in range(100, -1, -5):
            alpha = i / 100
            color = self.interpolate_color("#1e1e2e", "#a6e3a1", alpha)
            self.momster_label.config(fg=color)
            self.root.update()
            time.sleep(0.01)
            
        self.create_main_interface()
        
    def interpolate_color(self, start_hex, end_hex, alpha):
        start_rgb = tuple(int(start_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(end_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * alpha)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * alpha)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * alpha)
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def create_main_interface(self):
        self.splash_frame.destroy()
        
        self.main_frame = tk.Frame(
            self.root, 
            bg=self.current_colors['bg'], 
            padx=20, 
            pady=20,
            highlightthickness=1,
            highlightbackground=self.current_colors['window_border']
        )
        
        self.overlay = tk.Frame(self.root, bg="#1e1e2e")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.root.bind("<ButtonPress-1>", self.on_window_press)
        self.root.bind("<ButtonRelease-1>", self.on_window_release)
        self.root.bind("<B1-Motion>", self.on_window_motion)
        
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        
        self.create_widgets()
        
        self.load_data()
        
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)
        
        self.fade_in_main_interface()
        
        self.status_var.set(self.get_text("status_ready"))
        
    def fade_in_main_interface(self):
        steps = 10
        delay_ms = 15
        for i in range(steps, -1, -1):
            alpha = i / steps
            gray_val = int(30 + (224 * alpha))
            color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
            self.overlay.configure(bg=color)
            self.root.update()
            time.sleep(delay_ms / 1000.0)
        
        self.overlay.destroy()
        
    def on_window_press(self, event):
        control_widgets = [self.minimize_btn, self.close_btn, self.mode_button, self.language_btn]
        widget = event.widget
        if widget in control_widgets:
            return
            
        self.mouse_pressed = True
        self.press_start_x = event.x_root
        self.press_start_y = event.y_root
        self.is_dragging = False
        self.window_start_x = self.root.winfo_x()
        self.window_start_y = self.root.winfo_y()
    
    def on_window_motion(self, event):
        if not self.mouse_pressed:
            return
            
        dx = abs(event.x_root - self.press_start_x)
        dy = abs(event.y_root - self.press_start_y)
        
        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True
            new_x = self.window_start_x + (event.x_root - self.press_start_x)
            new_y = self.window_start_y + (event.y_root - self.press_start_y)
            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")
    
    def on_window_release(self, event):
        self.mouse_pressed = False
        
    def get_text(self, key):
        return self.texts[self.current_language].get(key, key)
        
    def toggle_language(self, event=None):
        self.current_language = "zh" if self.current_language == "en" else "en"
        self.refresh_interface()
        
    def refresh_interface(self):
        if self.is_minimal_mode:
            self.exit_minimal_mode()
            self.enter_minimal_mode()
        else:
            current_geometry = self.root.geometry()
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_main_interface()
            self.root.geometry(current_geometry)
            
    def show_help(self, event=None):
        help_window = tk.Toplevel(self.root)
        help_window.title(self.get_text("help_title"))
        help_window.geometry("650x550")
        help_window.configure(bg=self.current_colors['bg'])
        help_window.overrideredirect(True)
        help_window.attributes('-topmost', True)
        
        help_window.update_idletasks()
        width = help_window.winfo_width()
        height = help_window.winfo_height()
        x = (help_window.winfo_screenwidth() // 2) - (width // 2)
        y = (help_window.winfo_screenheight() // 2) - (height // 2)
        help_window.geometry(f"650x550+{x}+{y}")
        
        help_window.mouse_pressed = False
        help_window.is_dragging = False
        help_window.press_start_x = 0
        help_window.press_start_y = 0
        help_window.window_start_x = 0
        help_window.window_start_y = 0
        
        def on_help_press(event):
            help_window.mouse_pressed = True
            help_window.press_start_x = event.x_root
            help_window.press_start_y = event.y_root
            help_window.is_dragging = False
            help_window.window_start_x = help_window.winfo_x()
            help_window.window_start_y = help_window.winfo_y()
        
        def on_help_motion(event):
            if not help_window.mouse_pressed:
                return
                
            dx = abs(event.x_root - help_window.press_start_x)
            dy = abs(event.y_root - help_window.press_start_y)
            
            if dx > 5 or dy > 5:
                help_window.is_dragging = True
                new_x = help_window.window_start_x + (event.x_root - help_window.press_start_x)
                new_y = help_window.window_start_y + (event.y_root - help_window.press_start_y)
                help_window.geometry(f"+{int(new_x)}+{int(new_y)}")
        
        def on_help_release(event):
            help_window.mouse_pressed = False
            
        help_window.bind("<ButtonPress-1>", on_help_press)
        help_window.bind("<B1-Motion>", on_help_motion)
        help_window.bind("<ButtonRelease-1>", on_help_release)
        
        title_bar = tk.Frame(help_window, bg="#313244", height=35)
        title_bar.pack(fill="x", side="top")
        
        title_label = tk.Label(title_bar, text=self.get_text("help_title"), bg="#313244", fg="white", 
                              font=("微软雅黑", 11, "bold"))
        title_label.pack(side="left", padx=15, pady=6)
        
        close_btn = tk.Label(
            title_bar,
            text="×",
            font=("Helvetica", 14),
            fg="white",
            bg="#313244",
            padx=6,
            pady=0,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=5)
        close_btn.bind("<Button-1>", lambda e: help_window.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#f38ba8"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#313244"))
        
        notebook = ttk.Notebook(help_window, style="Custom.TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.TNotebook", background=self.current_colors['bg'])
        style.configure("Custom.TNotebook.Tab", 
                        background=self.current_colors['button_hover'],
                        foreground=self.current_colors['fg'],
                        padding=[10, 5],
                        font=("微软雅黑", 9))
        style.map("Custom.TNotebook.Tab", 
                  background=[("selected", self.current_colors['bg'])],
                  foreground=[("selected", self.current_colors['accent'])])
        
        intro_tab = tk.Frame(notebook, bg=self.current_colors['bg'], padx=10, pady=10)
        notebook.add(intro_tab, text=self.get_text("program_intro"))
        
        intro_text = tk.Text(intro_tab, bg=self.current_colors['treeview_bg'], fg=self.current_colors['fg'],
                            font=("微软雅黑", 10), wrap=tk.WORD, relief="flat", padx=10, pady=10, height=20)
        intro_content = self.get_text("intro_content") + "\n\n" + self.get_text("record_instructions")
        intro_text.insert(tk.END, intro_content)
        
        intro_text.insert(tk.END, "\n\n" + "-"*50 + "\n", "separator")
        intro_text.insert(tk.END, "Author: Momster\n", "author")
        intro_text.insert(tk.END, self.get_text("copyright") + "\n", "copyright")
        
        intro_text.tag_configure("separator", font=("微软雅黑", 10), foreground=self.current_colors['separator'])
        intro_text.tag_configure("author", font=("微软雅黑", 10, "bold"), foreground=self.current_colors['accent'])
        intro_text.tag_configure("copyright", font=("微软雅黑", 9, "italic"), foreground=self.current_colors['hint_fg'])
        intro_text.config(state=tk.DISABLED)
        
        intro_scrollbar = tk.Scrollbar(intro_tab, orient="vertical", command=intro_text.yview)
        intro_text.configure(yscrollcommand=intro_scrollbar.set)
        
        intro_text.pack(side="left", fill="both", expand=True)
        intro_scrollbar.pack(side="right", fill="y")
        
        key_tab = tk.Frame(notebook, bg=self.current_colors['bg'], padx=10, pady=10)
        notebook.add(key_tab, text=self.get_text("key_reference"))
        
        key_text = tk.Text(key_tab, bg=self.current_colors['treeview_bg'], fg=self.current_colors['fg'],
                          font=("微软雅黑", 10), wrap=tk.WORD, relief="flat", padx=10, pady=10, height=20)
        
        for category, keys in self.key_reference.items():
            key_text.insert(tk.END, f"{category}:\n", "category")
            key_text.insert(tk.END, "  " + ", ".join(keys) + "\n\n")
        
        key_text.insert(tk.END, "-"*50 + "\n", "separator")
        key_text.insert(tk.END, "Author: Momster\n", "author")
        key_text.insert(tk.END, self.get_text("copyright") + "\n", "copyright")
        
        key_text.tag_configure("category", font=("微软雅黑", 10, "bold"), foreground=self.current_colors['accent'])
        key_text.tag_configure("separator", font=("微软雅黑", 10), foreground=self.current_colors['separator'])
        key_text.tag_configure("author", font=("微软雅黑", 10, "bold"), foreground=self.current_colors['accent'])
        key_text.tag_configure("copyright", font=("微软雅黑", 9, "italic"), foreground=self.current_colors['hint_fg'])
        key_text.config(state=tk.DISABLED)
        
        key_scrollbar = tk.Scrollbar(key_tab, orient="vertical", command=key_text.yview)
        key_text.configure(yscrollcommand=key_scrollbar.set)
        
        key_text.pack(side="left", fill="both", expand=True)
        key_scrollbar.pack(side="right", fill="y")
        
        for widget in [title_label, intro_text, key_text]:
            widget.bind("<ButtonPress-1>", on_help_press)
            widget.bind("<B1-Motion>", on_help_motion)
            widget.bind("<ButtonRelease-1>", on_help_release)
        
    def create_widgets(self):
        title_bar = tk.Frame(self.main_frame, bg="#313244", relief="raised", bd=0, height=35)
        title_bar.pack(fill="x", side="top", pady=(0, 15))
        
        title_label = tk.Label(title_bar, text=self.get_text("title"), bg="#313244", fg="white", 
                              font=("微软雅黑", 11, "bold"))
        title_label.pack(side="left", padx=15, pady=6)
        
        control_frame = tk.Frame(title_bar, bg="#313244")
        control_frame.pack(side="right", padx=5)
        
        self.language_btn = tk.Label(
            control_frame,
            text=self.get_text("language"),
            font=("Helvetica", 9),
            fg="white",
            bg="#313244",
            padx=8,
            pady=5,
            cursor="hand2"
        )
        self.language_btn.pack(side="left", padx=2)
        self.language_btn.bind("<Button-1>", self.toggle_language)
        self.language_btn.bind("<Enter>", lambda e: self.language_btn.config(bg="#1e1e2e"))
        self.language_btn.bind("<Leave>", lambda e: self.language_btn.config(bg="#313244"))
        
        self.minimize_btn = tk.Label(
            control_frame,
            text="—",
            font=("Helvetica", 12),
            fg="white",
            bg="#313244",
            padx=8,
            pady=2,
            cursor="hand2"
        )
        self.minimize_btn.pack(side="left", padx=2)
        self.minimize_btn.bind("<Button-1>", self.toggle_minimal_mode)
        self.minimize_btn.bind("<Enter>", lambda e: self.minimize_btn.config(bg="#1e1e2e"))
        self.minimize_btn.bind("<Leave>", lambda e: self.minimize_btn.config(bg="#313244"))
        
        self.close_btn = tk.Label(
            control_frame,
            text="×",
            font=("Helvetica", 14),
            fg="white",
            bg="#313244",
            padx=6,
            pady=0,
            cursor="hand2"
        )
        self.close_btn.pack(side="left", padx=2)
        self.close_btn.bind("<Button-1>", self.quit_app)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(bg="#f38ba8"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(bg="#313244"))
        
        top_frame = tk.Frame(self.main_frame, bg=self.current_colors['bg'])
        top_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            top_frame,
            text=self.get_text("mode_control"),
            font=("微软雅黑", 10),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg']
        ).pack(side="left", padx=(0, 5))
        
        mode_text = self.get_text("suspend") if self.current_mode == "edit" else self.get_text("running")
        mode_color = self.current_colors['pause_fg'] if self.current_mode == "edit" else self.current_colors['active_fg']
        
        self.mode_button = tk.Label(
            top_frame,
            text=mode_text,
            font=("微软雅黑", 10, "bold"),
            fg=mode_color,
            bg=self.current_colors['bg'],
            padx=15,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        self.mode_button.pack(side="left", padx=(0, 10))
        self.mode_button.bind("<Button-1>", self.toggle_mode)
        self.mode_button.bind("<Enter>", lambda e: self.mode_button.config(bg=self.current_colors['button_hover']))
        self.mode_button.bind("<Leave>", lambda e: self.mode_button.config(bg=self.current_colors['bg']))
        
        self.save_button = tk.Label(
            top_frame,
            text=self.get_text("save_config"),
            font=("微软雅黑", 9),
            fg="#1e1e2e",
            bg="#89b4fa",
            padx=12,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        self.save_button.pack(side="right", padx=5)
        self.save_button.bind("<Button-1>", lambda e: self.save_data())
        self.save_button.bind("<Enter>", lambda e: self.save_button.config(bg="#585b70"))
        self.save_button.bind("<Leave>", lambda e: self.save_button.config(bg="#89b4fa"))
        
        hint_frame = tk.Frame(top_frame, bg=self.current_colors['bg'])
        hint_frame.pack(side="right", padx=20)
        tk.Label(hint_frame, text=self.get_text("f6_toggle_mode"), foreground=self.current_colors['hint_fg'], 
                 font=("微软雅黑", 9), bg=self.current_colors['bg']).pack(side="top")
        tk.Label(hint_frame, text=self.get_text("f4_exit"), foreground=self.current_colors['hint_fg'], 
                 font=("微软雅黑", 9), bg=self.current_colors['bg']).pack(side="top")
        tk.Label(hint_frame, text=self.get_text("f1_help"), foreground=self.current_colors['hint_fg'], 
                 font=("微软雅黑", 9), bg=self.current_colors['bg']).pack(side="top")
        
        notebook = ttk.Notebook(self.main_frame, style="Custom.TNotebook")
        notebook.pack(fill="both", expand=True, pady=5)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.TNotebook", background=self.current_colors['bg'])
        style.configure("Custom.TNotebook.Tab", 
                        background=self.current_colors['button_hover'],
                        foreground=self.current_colors['fg'],
                        padding=[10, 5],
                        font=("微软雅黑", 9))
        style.map("Custom.TNotebook.Tab", 
                  background=[("selected", self.current_colors['bg'])],
                  foreground=[("selected", self.current_colors['accent'])])
        
        mouse_tab = tk.Frame(notebook, bg=self.current_colors['bg'], padx=10, pady=10)
        notebook.add(mouse_tab, text=self.get_text("mouse_actions"))
        
        record_frame = tk.LabelFrame(mouse_tab, text=self.get_text("record_click"), bg=self.current_colors['bg'], 
                                   fg=self.current_colors['fg'], padx=10, pady=10,
                                   font=("微软雅黑", 9, "bold"))
        record_frame.pack(fill="x", pady=5)
        
        tk.Label(record_frame, text=self.get_text("hotkey"), bg=self.current_colors['bg'], 
                fg=self.current_colors['fg'], font=("微软雅黑", 9)).pack(side="left")
        self.key_entry = tk.Entry(record_frame, width=10, bg="#313244", fg="white", 
                                 insertbackground="white", relief="flat", font=("微软雅黑", 9))
        self.key_entry.pack(side="left", padx=5)
        
        tk.Label(record_frame, text=self.get_text("delay_sec"), bg=self.current_colors['bg'], 
                fg=self.current_colors['fg'], font=("微软雅黑", 9)).pack(side="left", padx=(15,5))
        self.delay_entry = tk.Entry(record_frame, width=8, bg="#313244", fg="white", 
                                   insertbackground="white", relief="flat", font=("微软雅黑", 9))
        self.delay_entry.pack(side="left", padx=5)
        self.delay_entry.insert(0, "1.0")
        
        self.record_button = tk.Label(
            record_frame,
            text=self.get_text("start_recording"),
            bg="#89b4fa",
            fg="#1e1e2e",
            padx=10,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.record_button.pack(side="left", padx=10)
        self.record_button.bind("<Button-1>", lambda e: self.start_recording())
        self.record_button.bind("<Enter>", lambda e: self.record_button.config(bg="#585b70"))
        self.record_button.bind("<Leave>", lambda e: self.record_button.config(bg="#89b4fa"))
        
        mouse_list_frame = tk.LabelFrame(mouse_tab, text=self.get_text("mouse_action_list"), bg=self.current_colors['bg'], 
                                       fg=self.current_colors['fg'], padx=10, pady=10,
                                       font=("微软雅黑", 9, "bold"))
        mouse_list_frame.pack(fill="both", expand=True, pady=5)
        
        style.configure("Custom.Treeview", 
                        background=self.current_colors['treeview_bg'],
                        foreground=self.current_colors['treeview_fg'],
                        fieldbackground=self.current_colors['treeview_bg'],
                        font=("微软雅黑", 9),
                        rowheight=26,
                        borderwidth=0)
        style.configure("Custom.Treeview.Heading", 
                        background=self.current_colors['treeview_header_bg'],
                        foreground=self.current_colors['treeview_header_fg'],
                        font=("微软雅黑", 9, "bold"),
                        relief="flat",
                        padding=4)
        style.map("Custom.Treeview", 
                 background=[('selected', self.current_colors['treeview_selected_bg'])],
                 foreground=[('selected', self.current_colors['treeview_selected_fg'])])
        
        mouse_columns = ("#", self.get_text("x_coord"), self.get_text("y_coord"), self.get_text("key"), 
                        self.get_text("delay"), self.get_text("button"))
        self.mouse_tree = ttk.Treeview(mouse_list_frame, columns=mouse_columns, show="headings", 
                                      height=8, style="Custom.Treeview")
        
        mouse_widths = {"#": 40, self.get_text("x_coord"): 70, self.get_text("y_coord"): 70, 
                       self.get_text("key"): 80, self.get_text("delay"): 60, self.get_text("button"): 60}
        for col in mouse_columns:
            self.mouse_tree.heading(col, text=col)
            self.mouse_tree.column(col, width=mouse_widths.get(col, 100), anchor="center")
        
        mouse_scroll = tk.Scrollbar(mouse_list_frame, orient="vertical", command=self.mouse_tree.yview, width=0)
        self.mouse_tree.configure(yscrollcommand=mouse_scroll.set)
        
        self.mouse_tree.pack(side="left", fill="both", expand=True)
        mouse_scroll.pack(side="right", fill="y")
        
        mouse_btn_frame = tk.Frame(mouse_list_frame, bg=self.current_colors['bg'])
        mouse_btn_frame.pack(side="bottom", fill="x", pady=(5, 0))
        
        button_container = tk.Frame(mouse_btn_frame, bg=self.current_colors['bg'])
        button_container.pack(side="left")
        
        delete_text = self.get_text("delete_selected")
        clear_text = self.get_text("clear_list")
        button_width = max(len(delete_text), len(clear_text)) + 4
        
        self.delete_mouse_btn = tk.Label(
            button_container,
            text=delete_text,
            bg="#f38ba8",
            fg="white",
            padx=15,
            pady=8,
            width=button_width,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.delete_mouse_btn.pack(side="top", pady=5)
        self.delete_mouse_btn.bind("<Button-1>", lambda e: self.delete_selected_mouse())
        self.delete_mouse_btn.bind("<Enter>", lambda e: self.delete_mouse_btn.config(bg="#eba0ac"))
        self.delete_mouse_btn.bind("<Leave>", lambda e: self.delete_mouse_btn.config(bg="#f38ba8"))
        
        self.clear_mouse_btn = tk.Label(
            button_container,
            text=clear_text,
            bg="#f38ba8",
            fg="white",
            padx=15,
            pady=8,
            width=button_width,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.clear_mouse_btn.pack(side="top", pady=5)
        self.clear_mouse_btn.bind("<Button-1>", lambda e: self.clear_mouse_list())
        self.clear_mouse_btn.bind("<Enter>", lambda e: self.clear_mouse_btn.config(bg="#eba0ac"))
        self.clear_mouse_btn.bind("<Leave>", lambda e: self.clear_mouse_btn.config(bg="#f38ba8"))
        
        keymap_tab = tk.Frame(notebook, bg=self.current_colors['bg'], padx=10, pady=10)
        notebook.add(keymap_tab, text=self.get_text("key_mapping"))
        
        keymap_input_frame = tk.LabelFrame(keymap_tab, text=self.get_text("key_mapping"), bg=self.current_colors['bg'], 
                                         fg=self.current_colors['fg'], padx=10, pady=10,
                                         font=("微软雅黑", 9, "bold"))
        keymap_input_frame.pack(fill="x", pady=5)
        
        tk.Label(keymap_input_frame, text=self.get_text("trigger_key"), bg=self.current_colors['bg'], 
                fg=self.current_colors['fg'], font=("微软雅黑", 9)).pack(side="left")
        self.trigger_key_entry = tk.Entry(keymap_input_frame, width=10, bg="#313244", fg="white", 
                                         insertbackground="white", relief="flat", font=("微软雅黑", 9))
        self.trigger_key_entry.pack(side="left", padx=5)
        
        tk.Label(keymap_input_frame, text="→ " + self.get_text("target_key"), bg=self.current_colors['bg'], 
                fg=self.current_colors['fg'], font=("微软雅黑", 9)).pack(side="left", padx=5)
        self.target_key_entry = tk.Entry(keymap_input_frame, width=10, bg="#313244", fg="white", 
                                        insertbackground="white", relief="flat", font=("微软雅黑", 9))
        self.target_key_entry.pack(side="left", padx=5)
        
        self.add_keymap_btn = tk.Label(
            keymap_input_frame,
            text=self.get_text("add_mapping"),
            bg="#89b4fa",
            fg="#1e1e2e",
            padx=10,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.add_keymap_btn.pack(side="left", padx=10)
        self.add_keymap_btn.bind("<Button-1>", lambda e: self.add_key_mapping())
        self.add_keymap_btn.bind("<Enter>", lambda e: self.add_keymap_btn.config(bg="#585b70"))
        self.add_keymap_btn.bind("<Leave>", lambda e: self.add_keymap_btn.config(bg="#89b4fa"))
        
        keymap_list_frame = tk.LabelFrame(keymap_tab, text=self.get_text("key_mapping_list"), bg=self.current_colors['bg'], 
                                        fg=self.current_colors['fg'], padx=10, pady=10,
                                        font=("微软雅黑", 9, "bold"))
        keymap_list_frame.pack(fill="both", expand=True, pady=5)
        
        keymap_columns = ("#", self.get_text("trigger_key"), self.get_text("target_key"))
        self.keymap_tree = ttk.Treeview(keymap_list_frame, columns=keymap_columns, show="headings", 
                                       height=8, style="Custom.Treeview")
        
        keymap_widths = {"#": 40, self.get_text("trigger_key"): 120, self.get_text("target_key"): 120}
        for col in keymap_columns:
            self.keymap_tree.heading(col, text=col)
            self.keymap_tree.column(col, width=keymap_widths.get(col, 120), anchor="center")
        
        keymap_scroll = tk.Scrollbar(keymap_list_frame, orient="vertical", command=self.keymap_tree.yview, width=0)
        self.keymap_tree.configure(yscrollcommand=keymap_scroll.set)
        
        self.keymap_tree.pack(side="left", fill="both", expand=True)
        keymap_scroll.pack(side="right", fill="y")
        
        keymap_btn_frame = tk.Frame(keymap_list_frame, bg=self.current_colors['bg'])
        keymap_btn_frame.pack(side="bottom", fill="x", pady=(5, 0))
        
        keymap_button_container = tk.Frame(keymap_btn_frame, bg=self.current_colors['bg'])
        keymap_button_container.pack(side="left")
        
        delete_text = self.get_text("delete_selected")
        clear_text = self.get_text("clear_list")
        button_width = max(len(delete_text), len(clear_text)) + 4
        
        self.delete_keymap_btn = tk.Label(
            keymap_button_container,
            text=delete_text,
            bg="#f38ba8",
            fg="white",
            padx=15,
            pady=8,
            width=button_width,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.delete_keymap_btn.pack(side="top", pady=5)
        self.delete_keymap_btn.bind("<Button-1>", lambda e: self.delete_selected_keymap())
        self.delete_keymap_btn.bind("<Enter>", lambda e: self.delete_keymap_btn.config(bg="#eba0ac"))
        self.delete_keymap_btn.bind("<Leave>", lambda e: self.delete_keymap_btn.config(bg="#f38ba8"))
        
        self.clear_keymap_btn = tk.Label(
            keymap_button_container,
            text=clear_text,
            bg="#f38ba8",
            fg="white",
            padx=15,
            pady=8,
            width=button_width,
            cursor="hand2",
            relief="raised",
            bd=1,
            font=("微软雅黑", 9, "bold")
        )
        self.clear_keymap_btn.pack(side="top", pady=5)
        self.clear_keymap_btn.bind("<Button-1>", lambda e: self.clear_keymap_list())
        self.clear_keymap_btn.bind("<Enter>", lambda e: self.clear_keymap_btn.config(bg="#eba0ac"))
        self.clear_keymap_btn.bind("<Leave>", lambda e: self.clear_keymap_btn.config(bg="#f38ba8"))
        
        bottom_frame = tk.Frame(self.main_frame, bg=self.current_colors['bg'])
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        status_frame = tk.LabelFrame(bottom_frame, text="Status", bg=self.current_colors['bg'], 
                                   fg=self.current_colors['fg'], padx=10, pady=10,
                                   font=("微软雅黑", 9, "bold"))
        status_frame.pack(side="right", fill="x", expand=True)
        
        self.status_var = tk.StringVar(value=self.get_text("status_ready"))
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               foreground="#89b4fa", font=("微软雅黑", 10),
                               bg=self.current_colors['bg'])
        status_label.pack(side="left", padx=10)
        
        self.update_mouse_treeview()
        self.update_keymap_treeview()
        
    def minimize_window(self, event):
        self.root.iconify()
        
    def quit_app(self, event=None):
        self.root.destroy()
        sys.exit(0)
        
    def toggle_mode(self, event=None):
        if self.current_mode == "edit":
            self.current_mode = "work"
            self.mode_button.config(text=self.get_text("running"), fg=self.current_colors['active_fg'])
            self.status_var.set(self.get_text("status_work_mode"))
            self.setup_all_shortcuts()
        else:
            self.current_mode = "edit"
            self.mode_button.config(text=self.get_text("suspend"), fg=self.current_colors['pause_fg'])
            self.status_var.set(self.get_text("status_edit_mode"))
            self.working = False
            self.remove_all_shortcuts()
            
    def setup_all_shortcuts(self):
        self.remove_all_shortcuts()
        self.position_handlers = {}
        self.keymap_handlers = {}

        for i, pos in enumerate(self.positions):
            key = pos.get("key", "F%s" % (i+1))
            try:
                handler = keyboard.add_hotkey(key, lambda x=pos["x"], y=pos["y"], btn=pos["button"]: self.click_position(x, y, btn))
                self.position_handlers[key] = handler
            except Exception:
                pass

        for i, km in enumerate(self.key_mappings):
            trigger = km.get("trigger", "")
            target = km.get("target", "")
            if trigger and target:
                try:
                    handler = keyboard.add_hotkey(trigger, lambda t=target: keyboard.press_and_release(t))
                    self.keymap_handlers[trigger] = handler
                except Exception:
                    pass

    def remove_all_shortcuts(self):
        if hasattr(self, 'position_handlers'):
            for key, handler in self.position_handlers.items():
                try:
                    keyboard.remove_hotkey(handler)
                except Exception:
                    pass
            self.position_handlers = {}

        if hasattr(self, 'keymap_handlers'):
            for key, handler in self.keymap_handlers.items():
                try:
                    keyboard.remove_hotkey(handler)
                except Exception:
                    pass
            self.keymap_handlers = {}

    def click_position(self, x, y, button):
        mouse_controller = mouse.Controller()
        
        original_x, original_y = mouse_controller.position
        
        mouse_controller.position = (x, y)
        if button == "left":
            mouse_controller.click(mouse.Button.left)
        elif button == "right":
            mouse_controller.click(mouse.Button.right)
        
        mouse_controller.position = (original_x, original_y)

    def start_recording(self):
        self.record_click = True
        self.status_var.set(self.get_text("status_recording"))

    def on_click(self, x, y, button, pressed):
        if pressed and self.record_click and self.current_mode == "edit":
            key = self.key_entry.get().strip() or "click"
            try:
                delay = float(self.delay_entry.get().strip() or "1.0")
            except:
                delay = 1.0

            self.positions.append({
                "x": x,
                "y": y,
                "key": key,
                "delay": delay,
                "button": str(button).split('.')[-1]
            })
            self.update_mouse_treeview()
            self.record_click = False
            status_msg = self.get_text("status_recorded").format(key=key, x=x, y=y)
            self.status_var.set(status_msg)

    def update_mouse_treeview(self):
        for item in self.mouse_tree.get_children():
            self.mouse_tree.delete(item)
        for i, pos in enumerate(self.positions):
            self.mouse_tree.insert("", "end", values=(
                i+1, pos["x"], pos["y"], pos["key"], pos["delay"], pos["button"]
            ))

    def update_keymap_treeview(self):
        for item in self.keymap_tree.get_children():
            self.keymap_tree.delete(item)
        for i, km in enumerate(self.key_mappings):
            self.keymap_tree.insert("", "end", values=(
                i+1, km["trigger"], km["target"]
            ))

    def delete_selected_mouse(self):
        selected = self.mouse_tree.selection()
        if not selected: return
        indices = [self.mouse_tree.index(item) for item in selected]
        for index in sorted(indices, reverse=True):
            if index < len(self.positions):
                del self.positions[index]
        self.update_mouse_treeview()

    def clear_mouse_list(self):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title(self.get_text("confirm_clear"))
        confirm_window.geometry("420x200")
        confirm_window.configure(bg=self.current_colors['bg'])
        confirm_window.overrideredirect(True)
        confirm_window.attributes('-topmost', True)
        
        confirm_window.update_idletasks()
        width = confirm_window.winfo_width()
        height = confirm_window.winfo_height()
        x = (confirm_window.winfo_screenwidth() // 2) - (width // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (height // 2)
        confirm_window.geometry(f"420x200+{x}+{y}")
        
        confirm_window.mouse_pressed = False
        confirm_window.is_dragging = False
        confirm_window.press_start_x = 0
        confirm_window.press_start_y = 0
        confirm_window.window_start_x = 0
        confirm_window.window_start_y = 0
        
        def on_confirm_press(event):
            confirm_window.mouse_pressed = True
            confirm_window.press_start_x = event.x_root
            confirm_window.press_start_y = event.y_root
            confirm_window.is_dragging = False
            confirm_window.window_start_x = confirm_window.winfo_x()
            confirm_window.window_start_y = confirm_window.winfo_y()
        
        def on_confirm_motion(event):
            if not confirm_window.mouse_pressed:
                return
                
            dx = abs(event.x_root - confirm_window.press_start_x)
            dy = abs(event.y_root - confirm_window.press_start_y)
            
            if dx > 5 or dy > 5:
                confirm_window.is_dragging = True
                new_x = confirm_window.window_start_x + (event.x_root - confirm_window.press_start_x)
                new_y = confirm_window.window_start_y + (event.y_root - confirm_window.press_start_y)
                confirm_window.geometry(f"+{int(new_x)}+{int(new_y)}")
        
        def on_confirm_release(event):
            confirm_window.mouse_pressed = False
            
        confirm_window.bind("<ButtonPress-1>", on_confirm_press)
        confirm_window.bind("<B1-Motion>", on_confirm_motion)
        confirm_window.bind("<ButtonRelease-1>", on_confirm_release)
        
        title_bar = tk.Frame(confirm_window, bg="#313244", height=30)
        title_bar.pack(fill="x", side="top")
        
        title_label = tk.Label(title_bar, text=self.get_text("confirm_clear"), bg="#313244", fg="white", 
                              font=("微软雅黑", 10, "bold"))
        title_label.pack(side="left", padx=15, pady=5)
        
        close_btn = tk.Label(
            title_bar,
            text="×",
            font=("Helvetica", 12),
            fg="white",
            bg="#313244",
            padx=6,
            pady=0,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=5)
        close_btn.bind("<Button-1>", lambda e: confirm_window.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#f38ba8"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#313244"))
        
        content_frame = tk.Frame(confirm_window, bg=self.current_colors['bg'], padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text=self.get_text("confirm_clear_msg"), 
                                bg=self.current_colors['bg'], fg=self.current_colors['fg'],
                                font=("微软雅黑", 10), wraplength=380, justify="center")
        message_label.pack(pady=20)
        
        button_frame = tk.Frame(content_frame, bg=self.current_colors['bg'])
        button_frame.pack(pady=15)
        
        confirm_btn = tk.Button(
            button_frame,
            text=self.get_text("confirm"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            padx=30,
            pady=12,
            cursor="hand2",
            relief="raised",
            bd=2,
            font=("微软雅黑", 11, "bold"),
            width=10,
            command=lambda: self.confirm_clear_mouse(confirm_window)
        )
        confirm_btn.pack(side="left", padx=20)
        
        cancel_btn = tk.Button(
            button_frame,
            text=self.get_text("cancel"),
            bg="#f38ba8",
            fg="white",
            padx=30,
            pady=12,
            cursor="hand2",
            relief="raised",
            bd=2,
            font=("微软雅黑", 11, "bold"),
            width=10,
            command=confirm_window.destroy
        )
        cancel_btn.pack(side="left", padx=20)
        
        for widget in [title_label, message_label, confirm_btn, cancel_btn, content_frame, button_frame]:
            widget.bind("<ButtonPress-1>", on_confirm_press)
            widget.bind("<B1-Motion>", on_confirm_motion)
            widget.bind("<ButtonRelease-1>", on_confirm_release)
        
    def confirm_clear_mouse(self, window):
        self.positions.clear()
        self.update_mouse_treeview()
        window.destroy()
        
    def add_key_mapping(self):
        trigger = self.trigger_key_entry.get().strip()
        target = self.target_key_entry.get().strip()
        if not trigger or not target:
            messagebox.showwarning(self.get_text("warning"), self.get_text("fields_required"))
            return
        try:
            keyboard.parse_hotkey(trigger)
            keyboard.parse_hotkey(target)
        except Exception:
            messagebox.showerror(self.get_text("error"), self.get_text("invalid_key"))
            return

        self.key_mappings.append({"trigger": trigger, "target": target})
        self.update_keymap_treeview()
        self.trigger_key_entry.delete(0, "end")
        self.target_key_entry.delete(0, "end")
        status_msg = self.get_text("status_mapped").format(trigger=trigger, target=target)
        self.status_var.set(status_msg)

    def delete_selected_keymap(self):
        selected = self.keymap_tree.selection()
        if not selected: return
        indices = [self.keymap_tree.index(item) for item in selected]
        for index in sorted(indices, reverse=True):
            if index < len(self.key_mappings):
                del self.key_mappings[index]
        self.update_keymap_treeview()

    def clear_keymap_list(self):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title(self.get_text("confirm_clear"))
        confirm_window.geometry("420x200")
        confirm_window.configure(bg=self.current_colors['bg'])
        confirm_window.overrideredirect(True)
        confirm_window.attributes('-topmost', True)
        
        confirm_window.update_idletasks()
        width = confirm_window.winfo_width()
        height = confirm_window.winfo_height()
        x = (confirm_window.winfo_screenwidth() // 2) - (width // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (height // 2)
        confirm_window.geometry(f"420x200+{x}+{y}")
        
        confirm_window.mouse_pressed = False
        confirm_window.is_dragging = False
        confirm_window.press_start_x = 0
        confirm_window.press_start_y = 0
        confirm_window.window_start_x = 0
        confirm_window.window_start_y = 0
        
        def on_confirm_press(event):
            confirm_window.mouse_pressed = True
            confirm_window.press_start_x = event.x_root
            confirm_window.press_start_y = event.y_root
            confirm_window.is_dragging = False
            confirm_window.window_start_x = confirm_window.winfo_x()
            confirm_window.window_start_y = confirm_window.winfo_y()
        
        def on_confirm_motion(event):
            if not confirm_window.mouse_pressed:
                return
                
            dx = abs(event.x_root - confirm_window.press_start_x)
            dy = abs(event.y_root - confirm_window.press_start_y)
            
            if dx > 5 or dy > 5:
                confirm_window.is_dragging = True
                new_x = confirm_window.window_start_x + (event.x_root - confirm_window.press_start_x)
                new_y = confirm_window.window_start_y + (event.y_root - confirm_window.press_start_y)
                confirm_window.geometry(f"+{int(new_x)}+{int(new_y)}")
        
        def on_confirm_release(event):
            confirm_window.mouse_pressed = False
            
        confirm_window.bind("<ButtonPress-1>", on_confirm_press)
        confirm_window.bind("<B1-Motion>", on_confirm_motion)
        confirm_window.bind("<ButtonRelease-1>", on_confirm_release)
        
        title_bar = tk.Frame(confirm_window, bg="#313244", height=30)
        title_bar.pack(fill="x", side="top")
        
        title_label = tk.Label(title_bar, text=self.get_text("confirm_clear"), bg="#313244", fg="white", 
                              font=("微软雅黑", 10, "bold"))
        title_label.pack(side="left", padx=15, pady=5)
        
        close_btn = tk.Label(
            title_bar,
            text="×",
            font=("Helvetica", 12),
            fg="white",
            bg="#313244",
            padx=6,
            pady=0,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=5)
        close_btn.bind("<Button-1>", lambda e: confirm_window.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#f38ba8"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#313244"))
        
        content_frame = tk.Frame(confirm_window, bg=self.current_colors['bg'], padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text=self.get_text("confirm_clear_msg"), 
                                bg=self.current_colors['bg'], fg=self.current_colors['fg'],
                                font=("微软雅黑", 10), wraplength=380, justify="center")
        message_label.pack(pady=20)
        
        button_frame = tk.Frame(content_frame, bg=self.current_colors['bg'])
        button_frame.pack(pady=15)
        
        confirm_btn = tk.Button(
            button_frame,
            text=self.get_text("confirm"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            padx=30,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2,
            font=("微软雅黑", 11, "bold"),
            width=10,
            command=lambda: self.confirm_clear_keymap(confirm_window)
        )
        confirm_btn.pack(side="left", padx=20)
        
        cancel_btn = tk.Button(
            button_frame,
            text=self.get_text("cancel"),
            bg="#f38ba8",
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2,
            font=("微软雅黑", 11, "bold"),
            width=10,
            command=confirm_window.destroy
        )
        cancel_btn.pack(side="left", padx=20)
        
        for widget in [title_label, message_label, confirm_btn, cancel_btn, content_frame, button_frame]:
            widget.bind("<ButtonPress-1>", on_confirm_press)
            widget.bind("<B1-Motion>", on_confirm_motion)
            widget.bind("<ButtonRelease-1>", on_confirm_release)
        
    def confirm_clear_keymap(self, window):
        self.key_mappings.clear()
        self.update_keymap_treeview()
        window.destroy()
        
    def save_data(self):
        data = {
            "positions": self.positions,
            "key_mappings": self.key_mappings
        }
        try:
            with open("mouse_agent_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.status_var.set(self.get_text("save_success"))
            messagebox.showinfo("Success", self.get_text("save_success"))
        except Exception as e:
            error_msg = self.get_text("save_failed").format(error=str(e))
            messagebox.showerror(self.get_text("error"), error_msg)

    def load_data(self):
        try:
            with open("mouse_agent_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except UnicodeDecodeError:
            try:
                with open("mouse_agent_data.json", "r", encoding="latin-1") as f:
                    content = f.read()
                    data = json.loads(content)
            except Exception:
                data = {}
        except FileNotFoundError:
            return
        except Exception as e:
            error_msg = self.get_text("load_failed").format(error=str(e))
            messagebox.showerror(self.get_text("error"), error_msg)
            return

        self.positions = data.get("positions", [])
        self.key_mappings = data.get("key_mappings", [])
        self.update_mouse_treeview()
        self.update_keymap_treeview()

    def toggle_minimal_mode(self, event=None):
        if not self.is_minimal_mode:
            self.enter_minimal_mode()
        else:
            self.exit_minimal_mode()

    def enter_minimal_mode(self):
        self.is_minimal_mode = True
        self.root.overrideredirect(False)
        self.root.geometry("240x110")
        self.center_window()
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        minimal_frame = tk.Frame(self.root, bg="#1e1e2e", padx=15, pady=15)
        minimal_frame.pack(fill="both", expand=True)
        
        button_frame = tk.Frame(minimal_frame, bg="#1e1e2e")
        button_frame.pack(expand=True)
        
        mode_text = self.get_text("suspend") if self.current_mode == "edit" else self.get_text("running")
        mode_color = self.current_colors['pause_fg'] if self.current_mode == "edit" else self.current_colors['active_fg']
        
        self.minimal_mode_button = tk.Label(
            button_frame,
            text=mode_text,
            font=("微软雅黑", 10, "bold"),
            fg=mode_color,
            bg=self.current_colors['bg'],
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        self.minimal_mode_button.pack(pady=(0, 8))
        self.minimal_mode_button.bind("<Button-1>", self.toggle_mode)
        self.minimal_mode_button.bind("<Enter>", lambda e: self.minimal_mode_button.config(bg=self.current_colors['button_hover']))
        self.minimal_mode_button.bind("<Leave>", lambda e: self.minimal_mode_button.config(bg=self.current_colors['bg']))
        
        self.restore_button = tk.Label(
            button_frame,
            text=self.get_text("minimal_restore"),
            font=("微软雅黑", 10, "bold"),
            fg="#1e1e2e",
            bg="#89b4fa",
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        self.restore_button.pack(pady=(8, 0))
        self.restore_button.bind("<Button-1>", lambda e: self.exit_minimal_mode())
        self.restore_button.bind("<Enter>", lambda e: self.restore_button.config(bg="#585b70"))
        self.restore_button.bind("<Leave>", lambda e: self.restore_button.config(bg="#89b4fa"))

    def exit_minimal_mode(self):
        self.is_minimal_mode = False
        self.root.overrideredirect(True)
        self.root.geometry("850x700")
        self.center_window()
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.create_main_interface()


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseAgent(root)
    root.mainloop()

