#!/usr/bin/env python3
import curses
import time
import random
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

# ---------- Helper Functions ----------

def draw_vpn_status(stdscr, y, x, connected):
    text = "VPN"
    color = curses.color_pair(2 if connected else 3)
    stdscr.addstr(y, x, text, color | curses.A_BOLD)

def generate_barcode_image(code):
    try:
        bc = barcode.get("code128", code, writer=ImageWriter())
        buf = BytesIO()
        bc.write(buf)
        buf.seek(0)

        img = Image.open(buf).convert("L")
        img = img.resize((40, 10))

        pixels = img.getdata()
        chars = ["█" if p < 128 else " " for p in pixels]
        lines = ["".join(chars[i:i+40]) for i in range(0, len(chars), 40)]
        return lines
    except Exception:
        return ["||||||||||||||||||||||||||||||||||||"]

def get_random_payment_code():
    return f"CB-{random.randint(100000,999999)}"

def get_random_amount():
    return f"${random.randint(50,9999):,}"

# ---------- Screens ----------

def draw_main_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "Encrypted Bank"
    stdscr.addstr(2, w//2 - len(title)//2, title, curses.A_BOLD | curses.color_pair(1))

    options = [
        "1. Bank-to-Bank Transfer",
        "2. Cash to Bitcoin",
        "3. Deposit",
        "4. Dirty to Clean",
        "Q. Quit"
    ]

    for i, opt in enumerate(options):
        stdscr.addstr(6 + i, w//2 - len(opt)//2, opt)

    stdscr.refresh()

def draw_bank_transfer(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(2, w//2 - 12, "Bank-to-Bank Transfer", curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(6, w//2 - 15, f"Amount: {get_random_amount()}")
    stdscr.addstr(8, w//2 - 25, "Connect your bank to continue securely 🔒")

    stdscr.addstr(h-2, 2, "Press any key to go back")
    stdscr.refresh()
    stdscr.getch()

def draw_cash_to_bitcoin(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    code = get_random_payment_code()

    stdscr.addstr(2, w//2 - 10, "Cash to Bitcoin", curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(4, 2, f"Amount: {get_random_amount()}")
    stdscr.addstr(6, 2, f"Payment Code: {code}")

    lines = generate_barcode_image(code)
    y = 8
    for line in lines:
        stdscr.addstr(y, w//2 - len(line)//2, line)
        y += 1

    stdscr.addstr(h-2, 2, "Press any key to go back")
    stdscr.refresh()
    stdscr.getch()

def draw_deposit(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(2, w//2 - 6, "Deposit", curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(5, 2, "Choose deposit method:")

    methods = ["Cash", "Bank Transfer", "Crypto"]
    for i, m in enumerate(methods):
        stdscr.addstr(7 + i, 4, f"- {m}")

    stdscr.addstr(h-2, 2, "Press any key to go back")
    stdscr.refresh()
    stdscr.getch()

def draw_dirty_clean(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(2, w//2 - 10, "Dirty → Clean Monitor", curses.A_BOLD | curses.color_pair(1))
    for i in range(5):
        amt = get_random_amount()
        stdscr.addstr(5 + i, 4, f"TX {i+1}: {amt} → CLEAN ✔")
        stdscr.refresh()
        time.sleep(0.4)

    stdscr.addstr(h-2, 2, "Press any key to go back")
    stdscr.getch()

# ---------- Main ----------

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        draw_main_menu(stdscr)
        draw_vpn_status(stdscr, 0, 2, True)
        key = stdscr.getkey().lower()

        if key == "1":
            draw_bank_transfer(stdscr)
        elif key == "2":
            draw_cash_to_bitcoin(stdscr)
        elif key == "3":
            draw_deposit(stdscr)
        elif key == "4":
            draw_dirty_clean(stdscr)
        elif key == "q":
            break

if __name__ == "__main__":
    curses.wrapper(main)
