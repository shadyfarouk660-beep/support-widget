import os
import socket
import getpass
import requests
import threading
import customtkinter as ctk

# --- CONFIGURATION ---
WEBHOOK_URL = "https://hook.eu1.make.com/8ztvk6jl7j3t3fp3e37nw0dpvh15an9c"

class SupportWidget(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Instant IT Support")
        self.geometry("450x300")
        self.resizable(False, False)
        self.attributes("-topmost", True)  # Keeps window on top
        
        # UI Elements
        self.label = ctk.CTkLabel(self, text="Describe your issue below:", font=("Arial", 16, "bold"))
        self.label.pack(pady=(20, 5))

        self.textbox = ctk.CTkTextbox(self, width=400, height=120, activate_scrollbars=True)
        self.textbox.pack(pady=10)

        # Bind the standard Enter key inside the app to submit quickly
        self.textbox.bind("<Control-Return>", lambda event: self.send_ticket())

        self.submit_btn = ctk.CTkButton(self, text="Submit Ticket", command=self.send_ticket, fg_color="#1f77b4", hover_color="#145a8d")
        self.submit_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

    def get_metadata(self):
        return {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "os": os.name
        }

    def send_ticket(self):
        issue_text = self.textbox.get("1.0", "end-1c").strip()
        
        if not issue_text:
            self.status_label.configure(text="Please describe the issue first!", text_color="red")
            return

        self.submit_btn.configure(state="disabled", text="Sending...")
        
        payload = {
            "issue": issue_text,
            "metadata": self.get_metadata()
        }

        def network_request():
            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    self.status_label.configure(text="Ticket submitted successfully!", text_color="green")
                    self.textbox.delete("1.0", "end")
                else:
                    self.status_label.configure(text=f"Error: Server responded with {response.status_code}", text_color="red")
            except requests.exceptions.RequestException:
                self.status_label.configure(text="Network error. Failed to reach helpdesk.", text_color="red")
            finally:
                self.submit_btn.configure(state="normal", text="Submit Ticket")

        threading.Thread(target=network_request, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = SupportWidget()
    app.mainloop()

