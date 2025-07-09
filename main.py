# -*- coding: utf-8 -*-
"""
Main entry: GUI for token creation on pump.fun
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pumpfun_api import create_token_with_avatar
import os
from config import API_KEY

class TokenCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coiner - Token Creator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主标题
        title_label = ttk.Label(self.root, text="Coiner - Token Creator", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Token名称
        ttk.Label(main_frame, text="Token Name:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
        self.name_entry = ttk.Entry(main_frame, font=("Arial", 12), width=40)
        self.name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Token Ticker
        ttk.Label(main_frame, text="Token Ticker:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
        self.ticker_entry = ttk.Entry(main_frame, font=("Arial", 12), width=40)
        self.ticker_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 池选择
        ttk.Label(main_frame, text="Pool Selection:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
        
        # 单池选择
        single_pool_frame = ttk.LabelFrame(main_frame, text="Single Pool", padding="5")
        single_pool_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.pool_var = tk.StringVar(value="pump")
        pool_frame = ttk.Frame(single_pool_frame)
        pool_frame.pack(fill=tk.X)
        
        pump_radio = ttk.Radiobutton(pool_frame, text="Pump", variable=self.pool_var, value="pump", command=self.on_pool_change)
        pump_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        bonk_radio = ttk.Radiobutton(pool_frame, text="Bonk", variable=self.pool_var, value="bonk", command=self.on_pool_change)
        bonk_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        moonshot_radio = ttk.Radiobutton(pool_frame, text="Moonshot", variable=self.pool_var, value="moonshot", command=self.on_pool_change)
        moonshot_radio.pack(side=tk.LEFT)
        
        # 多池选择
        multi_pool_frame = ttk.LabelFrame(main_frame, text="Multi-Pool (Create on multiple platforms)", padding="5")
        multi_pool_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.multi_pool_vars = {
            'pump': tk.BooleanVar(value=False),
            'bonk': tk.BooleanVar(value=False),
            'moonshot': tk.BooleanVar(value=False)
        }
        
        multi_pool_check_frame = ttk.Frame(multi_pool_frame)
        multi_pool_check_frame.pack(fill=tk.X)
        
        pump_check = ttk.Checkbutton(multi_pool_check_frame, text="Pump", variable=self.multi_pool_vars['pump'])
        pump_check.pack(side=tk.LEFT, padx=(0, 15))
        
        bonk_check = ttk.Checkbutton(multi_pool_check_frame, text="Bonk", variable=self.multi_pool_vars['bonk'])
        bonk_check.pack(side=tk.LEFT, padx=(0, 15))
        
        moonshot_check = ttk.Checkbutton(multi_pool_check_frame, text="Moonshot", variable=self.multi_pool_vars['moonshot'])
        moonshot_check.pack(side=tk.LEFT)
        
        # 选择模式
        self.mode_var = tk.StringVar(value="single")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 5))
        
        single_mode = ttk.Radiobutton(mode_frame, text="Single Pool Mode", variable=self.mode_var, value="single", command=self.on_mode_change)
        single_mode.pack(side=tk.LEFT, padx=(0, 15))
        
        multi_mode = ttk.Radiobutton(mode_frame, text="Multi-Pool Mode", variable=self.mode_var, value="multi", command=self.on_mode_change)
        multi_mode.pack(side=tk.LEFT)
        
        # 池说明
        self.pool_info = ttk.Label(main_frame, text="Pump池: 允许amount=0，使用pump.fun IPFS，计价单位SOL", font=("Arial", 9), foreground="blue")
        self.pool_info.pack(anchor=tk.W, pady=(0, 15))
        
        # 购买金额
        ttk.Label(main_frame, text="Buy Amount:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
        self.amount_entry = ttk.Entry(main_frame, font=("Arial", 12), width=40)
        self.amount_entry.insert(0, "0")
        self.amount_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 金额提示标签
        self.amount_hint = ttk.Label(main_frame, text="Pump池允许amount=0，Bonk池要求amount>0，Moonshot池要求amount>0", font=("Arial", 9), foreground="gray")
        self.amount_hint.pack(anchor=tk.W, pady=(0, 15))
        
        # 图片选择
        ttk.Label(main_frame, text="Avatar Image:", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
        
        image_frame = ttk.Frame(main_frame)
        image_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.image_path_var = tk.StringVar()
        self.image_entry = ttk.Entry(image_frame, textvariable=self.image_path_var, font=("Arial", 12))
        self.image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(image_frame, text="Browse", command=self.browse_image)
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 社交媒体链接（可选）
        social_frame = ttk.LabelFrame(main_frame, text="Social Media Links (Optional)", padding="10")
        social_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Website
        ttk.Label(social_frame, text="Website:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 4), padx=(0, 8))
        self.website_entry = ttk.Entry(social_frame, font=("Arial", 10), width=50)
        self.website_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 4))
        
        # X (Twitter)
        ttk.Label(social_frame, text="X (Twitter):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=(0, 4), padx=(0, 8))
        self.twitter_entry = ttk.Entry(social_frame, font=("Arial", 10), width=50)
        self.twitter_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 4))
        
        # Telegram
        ttk.Label(social_frame, text="Telegram:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=(0, 4), padx=(0, 8))
        self.telegram_entry = ttk.Entry(social_frame, font=("Arial", 10), width=50)
        self.telegram_entry.grid(row=2, column=1, sticky=tk.EW, pady=(0, 4))
        
        social_frame.columnconfigure(1, weight=1)
        
        # 代币描述（可选）
        desc_frame = ttk.LabelFrame(main_frame, text="Token Description (Optional)", padding="10")
        desc_frame.pack(fill=tk.X, pady=(0, 15))
        self.desc_text = tk.Text(desc_frame, height=3, font=("Arial", 10), wrap=tk.WORD)
        self.desc_text.pack(fill=tk.X)
        self.desc_text.delete("1.0", tk.END)  # 默认内容为空
        
        # 创建按钮
        create_btn = ttk.Button(main_frame, text="Create Token", command=self.create_token, style="Accent.TButton")
        create_btn.pack(pady=20)
        
        # 状态显示
        self.status_label = ttk.Label(main_frame, text="Ready to create token", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.result_text = tk.Text(result_frame, height=8, font=("Arial", 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def on_pool_change(self):
        """当池选择改变时的处理"""
        pool = self.pool_var.get()
        if pool == "bonk":
            # Bonk池要求amount > 0，设置默认值为0.1
            current_amount = self.amount_entry.get().strip()
            if not current_amount or float(current_amount) == 0:
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, "0.1")
            self.amount_hint.config(text="Bonk池要求amount>0，已自动设置为0.1 SOL", foreground="orange")
            self.pool_info.config(text="Bonk池: 要求amount>0，使用bonk.fun IPFS，计价单位SOL，优先级费用0.00005", foreground="orange")
        elif pool == "moonshot":
            # Moonshot池要求amount > 0，设置默认值为1
            current_amount = self.amount_entry.get().strip()
            if not current_amount or float(current_amount) == 0:
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, "1")
            self.amount_hint.config(text="Moonshot池要求amount>0，已自动设置为1 USDC", foreground="purple")
            self.pool_info.config(text="Moonshot池: 要求amount>0，使用bonk.fun IPFS，计价单位USDC，优先级费用0.00005", foreground="purple")
        else:
            # Pump池允许amount = 0
            self.amount_hint.config(text="Pump池允许amount=0，Bonk池要求amount>0，Moonshot池要求amount>0", foreground="gray")
            self.pool_info.config(text="Pump池: 允许amount=0，使用pump.fun IPFS，计价单位SOL，优先级费用0.0005", foreground="blue")
    
    def on_mode_change(self):
        """当模式选择改变时的处理"""
        mode = self.mode_var.get()
        if mode == "multi":
            # 多池模式：启用多池选择，禁用单池选择
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "Single Pool":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for radio in child.winfo_children():
                                if isinstance(radio, ttk.Radiobutton):
                                    radio.config(state="disabled")
            
            # 启用多池选择
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "Multi-Pool (Create on multiple platforms)":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for check in child.winfo_children():
                                if isinstance(check, ttk.Checkbutton):
                                    check.config(state="normal")
            
            self.pool_info.config(text="多池模式: 将在选中的平台上同时创建代币", foreground="green")
        else:
            # 单池模式：启用单池选择，禁用多池选择
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "Single Pool":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for radio in child.winfo_children():
                                if isinstance(radio, ttk.Radiobutton):
                                    radio.config(state="normal")
            
            # 禁用多池选择
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "Multi-Pool (Create on multiple platforms)":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for check in child.winfo_children():
                                if isinstance(check, ttk.Checkbutton):
                                    check.config(state="disabled")
            
            # 恢复单池的说明
            self.on_pool_change()
        
    def browse_image(self):
        """选择图片文件"""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Avatar Image",
            filetypes=filetypes
        )
        
        if filename:
            self.image_path_var.set(filename)
            
    def create_token(self):
        """创建代币"""
        # 获取输入值
        token_name = self.name_entry.get().strip()
        ticker = self.ticker_entry.get().strip()
        image_path = self.image_path_var.get().strip()
        mode = self.mode_var.get()
        
        # 获取社交媒体链接（可选）
        website = self.website_entry.get().strip()
        twitter = self.twitter_entry.get().strip()
        telegram = self.telegram_entry.get().strip()
        
        # 获取代币描述（可选）
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # 根据模式确定要使用的池
        if mode == "single":
            pools = [self.pool_var.get()]
        else:
            # 多池模式：获取选中的池
            pools = [pool_name for pool_name, var in self.multi_pool_vars.items() if var.get()]
            if not pools:
                messagebox.showerror("Error", "Please select at least one pool in multi-pool mode")
                return
        
        # 验证购买金额
        try:
            amount = float(self.amount_entry.get().strip())
            if amount < 0:
                messagebox.showerror("Error", "Buy amount cannot be negative")
                return
            # 多池模式下的金额验证
            if mode == "multi":
                for pool in pools:
                    if pool in ["bonk", "moonshot"] and amount <= 0:
                        messagebox.showerror("Error", f"{pool.capitalize()} pool requires buy amount > 0")
                        return
            else:
                # 单池模式下的金额验证
                pool = pools[0]
                if pool in ["bonk", "moonshot"] and amount <= 0:
                    messagebox.showerror("Error", f"{pool.capitalize()} pool requires buy amount > 0")
                    return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid buy amount")
            return
        
        # 验证输入
        if not token_name:
            messagebox.showerror("Error", "Please enter a token name")
            return
            
        if not ticker:
            messagebox.showerror("Error", "Please enter a token ticker")
            return
            
        if not image_path:
            messagebox.showerror("Error", "Please select an avatar image")
            return
            
        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"Image file not found: {image_path}")
            return
            
        # 检查API密钥
        if API_KEY == 'your-api-key-here':
            messagebox.showerror("Error", "Please configure your API key in .env file")
            return
            
        # 更新状态
        if mode == "single":
            self.status_label.config(text="Creating token...")
        else:
            self.status_label.config(text=f"Creating tokens on {len(pools)} platforms...")
        self.root.update()
        
        try:
            # 创建代币
            if mode == "single":
                # 单池模式
                pool = pools[0]
                result = create_token_with_avatar(token_name, ticker, image_path, amount, pool, website, twitter, telegram, description)
                
                # 显示结果
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Token Creation Result:\n\n{result}")
                
                if "successfully" in result.lower():
                    self.status_label.config(text="Token created successfully!")
                    messagebox.showinfo("Success", "Token created successfully!")
                else:
                    self.status_label.config(text="Token creation failed")
            else:
                # 多池模式
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Creating tokens on {len(pools)} platforms...\n\n")
                self.root.update()
                
                all_results = []
                for i, pool in enumerate(pools, 1):
                    self.status_label.config(text=f"Creating on {pool.capitalize()} ({i}/{len(pools)})...")
                    self.root.update()
                    
                    result = create_token_with_avatar(token_name, ticker, image_path, amount, pool, website, twitter, telegram, description)
                    all_results.append(f"{pool.capitalize()}: {result}")
                    
                    # 更新结果显示
                    self.result_text.delete(1.0, tk.END)
                    self.result_text.insert(tk.END, f"Multi-Pool Token Creation Results:\n\n")
                    for res in all_results:
                        self.result_text.insert(tk.END, f"{res}\n\n")
                    
                    self.root.update()
                
                # 检查是否有成功的
                success_count = sum(1 for res in all_results if "successfully" in res.lower())
                if success_count > 0:
                    self.status_label.config(text=f"Created on {success_count}/{len(pools)} platforms successfully!")
                    messagebox.showinfo("Success", f"Created on {success_count}/{len(pools)} platforms successfully!")
                else:
                    self.status_label.config(text="All token creations failed")
            
        except Exception as e:
            error_msg = f"Error creating token: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error:\n\n{error_msg}")
            
            self.status_label.config(text="Token creation failed")
            messagebox.showerror("Error", error_msg)

def main():
    root = tk.Tk()
    app = TokenCreatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 