#!/usr/bin/env python3
import curses
import time
import random
import string
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image
import os
import sys

# --- Helper Functions ---

def draw_vpn_status(stdscr, start_y, start_x, is_connected, blink_state):
    """Draws the VPN logo and its status."""
    logo_text = "VPN"
    if is_connected:
        # Solid blue when connected
        stdscr.addstr(start_y, start_x, logo_text, curses.color_pair(1) | curses.A_BOLD)
    else:
        # Blinking when connecting
        if blink_state:
            stdscr.addstr(start_y, start_x, logo_text, curses.color_pair(2) | curses.A_BOLD)
        else:
            stdscr.addstr(start_y, start_x, logo_text, curses.color_pair(3) | curses.A_BOLD) # Dimmed white

def generate_barcode_image(code):
    """Generates a barcode image and returns it as ASCII art."""
    try:
        # Generate a Code128 barcode
        bc = barcode.get('code128', code, writer=ImageWriter())
        
        # Save to a temporary in-memory file
        temp_file = BytesIO()
        bc.write(temp_file)
        temp_file.seek(0)
        
        # Open with PIL to convert to ASCII
        img = Image.open(temp_file)
        img = img.convert('L') # Convert to grayscale
        
        # Resize for terminal
        width, height = img.size
        aspect_ratio = height / width
        new_width = 40
        new_height = int(aspect_ratio * new_width * 0.5) # 0.5 to adjust for character height
        img = img.resize((new_width, new_height))
        
        # Convert to ASCII
        pixels = img.getdata()
        ascii_str = ''
        for pixel in pixels:
            ascii_str += '█' if pixel < 128 else ' '
        
        # Split into lines
        ascii_lines = [ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)]
        return ascii_lines
    except Exception:
        # Fallback if barcode library is not installed or fails
        return ["||||||||||||||||||||||||||||||||||||", "||||||||||||||||||||||||||||||||||||"]

def get_random_payment_code():
    """Generates a random payment reference code."""
    return f"CB-{random.randint(100000, 999999)}"

def get_random_amount():
    """Generates a random transaction amount."""
    return f"\${random.randint(50, 9999):,}"

# --- Screen Drawing Functions ---

def draw_main_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Title
    title = "Encrypted Bank"
    stdscr.addstr(2, (w // 2) - len(title) // 2, title, curses.A_BOLD | curses.color_pair(1))
    
    # Subtitle
    subtitle = "Secure Transaction Terminal"
    stdscr.addstr(3, (w // 2) - len(subtitle) // 2, subtitle)
    
    # Menu Options
    menu_items = [
        "1. Bank-to-bank transfer",
        "2. Cash To Bitcoin",
        "3. Deposit",
        "4. Dirty to Clean"
    ]
    
    start_y = h // 2 - len(menu_items) // 2
    for i, item in enumerate(menu_items):
        stdscr.addstr(start_y + i, (w // 2) - len(item) // 2, item)
        
    # Instructions
    instructions = "Enter an option [1-4] or 'q' to quit."
    stdscr.addstr(h - 3, (w // 2) - len(instructions) // 2, instructions)

def draw_bank_transfer(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    title = "Bank-to-Bank Transfer"
    stdscr.addstr(2, (w // 2) - len(title) // 2, title, curses.A_BOLD | curses.color_pair(1))
    
    payment_method = "Payment Method: Bank Transfer (ACH)"
    stdscr.addstr(h // 2 - 4, (w // 2) - len(payment_method) // 2, payment_method)
    
    amount = get_random_amount()
    amount_text = f"Amount: {amount}"
    stdscr.addstr(h // 2 - 2, (w // 2) - len(amount_text) // 2, amount_text)
    
    message = "Connect your bank to complete this payment securely. 🔒"
    stdscr.addstr(h // 2, (w // 2) - len(message) // 2, message)
    
    powered = "Powered by (EB)"
    stdscr.addstr(h // 2 + 2, (w // 2) - len(powered) // 2, powered)
    
    # Buttons
    btn1 = "[ Continue to Bank Login ]"
    btn2 = "[ Enter Bank Details Manually ]"
    stdscr.addstr(h // 2 + 4, (w // 2) - len(btn1) // 2, btn1, curses.color_pair(2))
    stdscr.addstr(h // 2 + 6, (w // 2) - len(btn2) // 2, btn2, curses.color_pair(2))

    stdscr.addstr(h - 3, (w // 2) - 15, "Press 'b' to go back.")

def draw_cash_to_bitcoin(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    title = "Cash to Bitcoin"
    stdscr.addstr(2, (w // 2) - len(title) // 2, title, curses.A_BOLD | curses.color_pair(1))
    
    amount = get_random_amount()
    amount_text = f"Amount: {amount}"
    stdscr.addstr(4, (w // 2) - len(amount_text) // 2, amount_text)
    
    info = "Send cash using one of the supported methods below. Once payment is received, Bitcoin will be sent to your wallet."
    stdscr.addstr(6, 2, info)
    
    step1 = "Step 1: Get Your Payment Code"
    stdscr.addstr(8, 2, step1, curses.A_BOLD)
    
    code = get_random_payment_code()
    code_text = f"Payment Reference Code: {code}"
    stdscr.addstr(9, 2, code_text)
    
    step2 = "Step 2: Pay with Cash"
    stdscr.addstr(11, 2, step2, curses.A_BOLD)
    
    locations = "Go to any participating location: * Walmart * CVS * 7-Eleven"
    stdscr.addstr(12, 2, locations)
    
    barcode_label = "Show the cashier this barcode:"
    stdscr.addstr(14, 2, barcode_label)
    
    # Draw barcode
    barcode_lines = generate_barcode_image(code)
    start_y = 15
    for line in barcode_lines:
        stdscr.addstr(start_y, (w // 2) - len(line) // 2, line, curses.color_pair(4))
        start_y += 1
        
    step3 = "Step 3: Receive Bitcoin"
    stdscr.addstr(start_y + 1, 2, step3, curses.A_BOLD)
    
    wallet_prompt = "Enter your Bitcoin wallet address:"
    stdscr.addstr(start_y + 2, 2, wallet_prompt)
    
    processing = "Processing time: 10–60 minutes after cash is received"
    stdscr.addstr(start_y + 4, 2, processing)
    
    non_refund = "Payments are non-refundable"
    stdscr.addstr(start_y + 5, 2, non_refund, curses.A_DIM)
    
    stdscr.addstr(h - 3, (w // 2) - 15, "Press 'b' to go back.")

def draw_deposit(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    title = "Deposit Funds"
    stdscr.addstr(2, (w // 2) - len(title) // 2, title, curses.A_BOLD | curses.color_pair(1))
    
    amount_prompt = "Amount: \$"
    stdscr.addstr(h // 2 - 6, (w // 2) - 20, amount_prompt)
    
    # Create a field for user input
    curses.echo()
    win = curses.newwin(1, 20, h // 2 - 6, (w // 2) - 20 + len(amount_prompt))
    win.refresh()
    
    method_prompt = "Choose Deposit Method:"
    stdscr.addstr(h // 2 - 4, (w // 2) - 20, method_prompt, curses.A_BOLD)
    
    methods =
