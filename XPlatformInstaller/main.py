import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from managers import get_manager


def detect_os_id():
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
        return None
    return None


class PackageGUI(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("Cross-Platform Package Manager")
        self.geometry("700x600")

        # Top buttons
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(pady=5)

        self.install_btn = tk.Button(
            self.action_frame, text="Install Programs", width=15, bg="#4CAF50", fg="black",
            command=self.install_prompt
        )
        self.install_btn.pack(side=tk.LEFT, padx=5)

        self.uninstall_btn = tk.Button(
            self.action_frame, text="Uninstall Programs", width=15, bg="#f44336", fg="black",
            command=self.uninstall_prompt
        )
        self.uninstall_btn.pack(side=tk.LEFT, padx=5)

        self.exit_btn = tk.Button(self.action_frame, text="Exit", width=12, command=self.destroy)
        self.exit_btn.pack(side=tk.LEFT, padx=5)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", lambda event: self.search_packages())

        # Scrollable package list frame
        self.list_frame = tk.Frame(self, bg="white")
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

        self.canvas = tk.Canvas(self.list_frame, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Selected packages listbox
        self.selected_frame = tk.Frame(self, bg="white", bd=1, relief=tk.SOLID)
        self.selected_frame.pack(fill=tk.BOTH, expand=False, pady=5, padx=10)

        self.selected_label = tk.Label(self.selected_frame, text="Selected Packages:", bg="white")
        self.selected_label.pack(anchor="w")

        self.selected_list = tk.Listbox(
            self.selected_frame, selectmode=tk.NONE, fg="black", bg="white", height=5
        )
        self.selected_list.pack(fill=tk.BOTH, expand=True)

        # Bottom run button
        self.run_btn = tk.Button(self, text="Run Selected", width=20, bg="#2196F3", fg="white",
                                 command=self.run_selected)
        self.run_btn.pack(pady=5)
        self.run_btn.config(state=tk.DISABLED)

        # State
        self.current_action = None
        self.all_packages = []
        self.selected_packages = {}

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def install_prompt(self):
        self.current_action = "install"
        self.run_btn.config(text="Install Selected")
        self.selected_packages.clear()
        self.search_var.set("")
        self.search_entry.config(state=tk.NORMAL)
        self.refresh_list()

    def uninstall_prompt(self):
        self.current_action = "uninstall"
        self.run_btn.config(text="Uninstall Selected")
        self.selected_packages.clear()
        self.search_var.set("")
        self.search_entry.config(state=tk.NORMAL)
        self.refresh_list()

    def refresh_list(self):
        query = self.search_var.get().strip().lower()
        # Load packages
        if self.current_action == "install":
            self.all_packages = self.manager.clean_package_list(
                self.manager.search_package(query) if query else []
            )
        else:
            installed = self.manager.list_installed_packages() or []
            # Filter installed packages by search query
            if query:
                self.all_packages = [(pkg, desc) for pkg, desc in installed if query in pkg.lower()]
            else:
                self.all_packages = installed

        # Remove previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Create checkbuttons without borders
        self.check_vars = {}
        for pkg, desc in self.all_packages:
            var = tk.BooleanVar(value=pkg in self.selected_packages)
            cb = tk.Checkbutton(
                self.scrollable_frame, text=f"{pkg} - {desc}" if desc else pkg,
                variable=var, bg="white", anchor="w",
                highlightthickness=0, bd=0, relief=tk.FLAT,
                selectcolor="white",
                command=lambda p=pkg, v=var: self.toggle_package(p, v)
            )
            cb.pack(fill=tk.X, anchor="w", padx=2, pady=1)
            self.check_vars[pkg] = var

        self.update_selected_listbox()
        self.update_run_button_state()

        # Scroll to top
        self.canvas.yview_moveto(0)

    def toggle_package(self, pkg, var):
        if var.get():
            self.selected_packages[pkg] = next((p for p in self.all_packages if p[0] == pkg), (pkg, ""))
        else:
            self.selected_packages.pop(pkg, None)
        self.update_selected_listbox()
        self.update_run_button_state()

    def update_selected_listbox(self):
        self.selected_list.delete(0, tk.END)
        for pkg, desc in self.selected_packages.values():
            display_text = f"{pkg} - {desc}" if desc else pkg
            self.selected_list.insert(tk.END, display_text)

    def update_run_button_state(self):
        self.run_btn.config(state=tk.NORMAL if self.selected_packages else tk.DISABLED)

    def search_packages(self):
        self.refresh_list()

    def run_selected(self):
        if not self.selected_packages:
            messagebox.showwarning("No Selection", "Please select at least one package.")
            return

        selected_list = list(self.selected_packages.values())
        cleaned = self.manager.clean_package_list(selected_list)
        if not cleaned:
            messagebox.showerror("Invalid Packages", "No valid packages selected.")
            return

        cmd = self.manager.generate_install_command(cleaned) if self.current_action == "install" \
            else self.manager.generate_uninstall_command(cleaned)

        confirm = messagebox.askyesno(f"Confirm {self.current_action}", f"Run command:\n{cmd}?")
        if confirm:
            subprocess.run(cmd, shell=True)
            messagebox.showinfo("Done", f"{self.current_action.capitalize()} completed!")

            # Clear selections, search bar, and scroll to top
            self.selected_packages.clear()
            self.search_var.set("")
            self.refresh_list()


def main():
    os_id = detect_os_id()
    if not os_id:
        messagebox.showerror("OS Detection Error", "Unable to detect operating system.")
        return

    try:
        manager = get_manager(os_id)
    except NotImplementedError as e:
        messagebox.showerror("Unsupported OS", str(e))
        return

    app = PackageGUI(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
