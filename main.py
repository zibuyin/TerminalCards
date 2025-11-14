import curses
from imageinterminal import display_image
import os
import json

def main(stdscr):
    # -------- Start of Initialization --------
    options = ["Choose Deck", "Create Deck", "Settings", "Credits", "Exit"]
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(0)   # Make getch() blocking
    stdscr.keypad(1)    # Enable special keys to be interpreted (like arrows)
    max_height, max_width = stdscr.getmaxyx()

    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    # Use built-in curses colors (works on all terminals)
    curses.init_color(curses.COLOR_BLUE, 0, 600, 1000) # Blue is broken in some terminals, use self defined
    curses.init_pair(1, curses.COLOR_RED, -1)     # Pair: FG:Red, BG:Default
    curses.init_pair(2, curses.COLOR_GREEN, -1)   # Pair: FG:Green, BG:Default
    curses.init_pair(3, curses.COLOR_BLUE, -1)    # Pair: FG:Blue, BG:Default
    curses.init_pair(4, curses.COLOR_WHITE, -1)   # Pair: FG:White, BG:Default

    # Backgrond highlight colors
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)     # Pair: FG:Red, BG:white
    curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_WHITE)   # Pair: FG:Green, BG:white
    curses.init_pair(13, curses.COLOR_BLUE, curses.COLOR_WHITE)    # Pair: FG:Blue, BG:white
    curses.init_pair(14, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Pair: FG:White, BG:white
    # -------- End of Initialization --------

    # -------- Start of show_splash function --------
    def filesystem_init():
        try:
            os.mkdir("cards")
        except FileExistsError:
            pass
        file = open("cards/decks.json", "a+")
        file.close()
    filesystem_init()
        
        
    def show_splash():
        # ASCII art stored as raw string to avoid escape sequence issues(cough cough... "\" break stuff")
        ascii_art = r"""
 _____                    _             _     ___              _     
/__   \___ _ __ _ __ ___ (_)_ __   __ _| |   / __\__ _ _ __ __| |___ 
  / /\/ _ \ '__| '_ ` _ \| | '_ \ / _` | |  / /  / _` | '__/ _` / __|
 / / |  __/ |  | | | | | | | | | | (_| | | / /__| (_| | | | (_| \__ \
 \/   \___|_|  |_| |_| |_|_|_| |_|\__,_|_| \____/\__,_|_|  \__,_|___/
        """
        
        stdscr.addstr(0, 0, ascii_art, curses.color_pair(3))
        
        
    # -------- End of show_splash function --------

    def backto_menu_loop():
        while True:
            if(stdscr.getkey().lower() == 'b'):
                selection_handler(menu_options("KEY_UP"))
                break

    
    # -------- Start of menu_options function --------
    def menu_options(key_input, selectedOption=0):
        stdscr.clear()
        show_splash()
        # Check for Enter key - it can be '\n', '\r', or KEY_ENTER 
        stdscr.addstr(7, 0, "Choose an option below to start:", curses.color_pair(2) | curses.A_BOLD)
        if key_input == "KEY_UP":
            if selectedOption > 0:
                selectedOption -= 1
        elif key_input == "KEY_DOWN":
            if selectedOption < len(options) - 1:
                selectedOption += 1
        
        elif key_input in ['\n', '\r', 'KEY_ENTER'] or key_input == curses.KEY_ENTER:
            stdscr.clear()
            show_splash()
            return selectedOption
            
        elif key_input == 'q':
            exit(0)
        
        # Display all options with highlighting for selected
        for i, option in enumerate(options):
            if i == selectedOption:
                stdscr.addstr(9 + i, 0, str(i+1) + f". {option}", curses.color_pair(3) | curses.A_STANDOUT)
            else:
                stdscr.addstr(9 + i, 0, str(i+1) + f". {option}", curses.color_pair(3))
        stdscr.addstr(9 + len(options) + 1, 0, "Or press [Q] to quit", curses.color_pair(2) | curses.A_BOLD)
        
        
        stdscr.refresh()
        return menu_options(stdscr.getkey(), selectedOption)

    # -------- Start of defining menu options handlers -------- 
    def choose_deck_handler():
        stdscr.addstr(7, 0, "Choose a deck below", curses.color_pair(2) | curses.A_BOLD)
        with open("cards/decks.json","r") as file:
            try:
                data = json.load(file)
                stdscr.addstr(9, 0, str(data["decks"][0]["friendlyName"]), curses.color_pair(4))
                # for i,deck in enumerate(decks):
                #     stdscr.addstr(9 + i, 0, f"{i+1}. {deck['name']}", curses.color_pair(4))
            except json.JSONDecodeError:
                stdscr.addstr(9, 0, "No decks found. Please create a deck first.", curses.color_pair(1))
        
        stdscr.addstr(max_height - 1, 0, "Press [B] to return...", curses.color_pair(2) | curses.A_BOLD)
        stdscr.refresh()
        backto_menu_loop()

        

    def create_deck_handler():
        stdscr.addstr(7, 0, "Create a deck", curses.color_pair(2) | curses.A_BOLD)
    def settings_handler():
        stdscr.addstr(7, 0, "Settings", curses.color_pair(2) | curses.A_BOLD)
    def credits_handler():
        stdscr.clear()
        
        show_splash()
        stdscr.addstr(6, 0, "─" * min(70, max_width - 1), curses.color_pair(3))
        stdscr.addstr(7, 0, "MIT License", curses.color_pair(2) | curses.A_BOLD)
        
        
        
        license_text = [
            "",
            "Copyright (c) 2025 Nathan Yin",
            "",
            "Permission is hereby granted, free of charge, to any person obtaining a copy",
            "of this software and associated documentation files (the \"Software\"), to deal",
            "in the Software without restriction, including without limitation the rights",
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
            "copies of the Software, and to permit persons to whom the Software is",
            "furnished to do so, subject to the following conditions:",
            "",
            "The above copyright notice and this permission notice shall be included in all",
            "copies or substantial portions of the Software.\n",
            "* Full License text available at https://opensource.org/licenses/MIT *"
        ]
        
        # Display license text, but only lines that fit on screen
        for i, line in enumerate(license_text):
            if 8 + i < max_height - 2:  # Leave room for the "Press any key" message
                try:
                    stdscr.addstr(7 + i, 0, line[:max_width - 1], curses.color_pair(4))
                except curses.error:
                    pass  # Skip if we can't write to this position
        stdscr.addstr(20, 0, "─" * min(70, max_width - 1), curses.color_pair(3))
        stdscr.addstr(21,0,"This project is depended on the following open source libraries:",curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(22,0,"curses: #TODO",curses.color_pair(4))
        stdscr.addstr(23,0,"image-in-terminal: https://pypi.org/project/image-in-terminal/",curses.color_pair(4))




        stdscr.addstr(max_height - 1, 0, "Press [B] to return...", curses.color_pair(2) | curses.A_BOLD)
        stdscr.refresh()
        backto_menu_loop()


                
            



    def exit_handler():
        exit(0)
    # -------- End of defining menu options handlers -------- 
    # Initial call to display menu and get selection
    def selection_handler(selectedOption):
        # Choose Desk
        if selectedOption == 0:
            choose_deck_handler()
        # Create Desk
        if selectedOption == 1:
            create_deck_handler()
        # Settings
        if selectedOption == 2:
            settings_handler()
        # Credits
        if selectedOption == 3:
            credits_handler()
        # Exit
        if selectedOption == 4:
            exit_handler()

    selection_handler(menu_options("KEY_UP"))
      

        
    # stdscr.addstr(7, 0, f"Final selected option index: {selectedOption}", curses.color_pair(2))
    stdscr.getch()
    stdscr.refresh()
        
    

    

curses.wrapper(main)