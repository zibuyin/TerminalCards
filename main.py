import curses
def main(stdscr):
    # -------- Start of Initialization --------
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(0)   # Make getch() blocking
    stdscr.keypad(1)    # Enable special keys to be interpreted (like arrows)
    height, width = stdscr.getmaxyx()  # Get terminal size


    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    # Use built-in curses colors (works on all terminals)
    curses.init_color(curses.COLOR_BLUE, 0, 600, 1000) # Blue is broken in some terminals, use self defined
    curses.init_pair(1, curses.COLOR_RED, -1)     # Pair: FG:Red, BG:Default
    curses.init_pair(2, curses.COLOR_GREEN, -1)   # Pair: FG:Green, BG:Default
    curses.init_pair(3, curses.COLOR_BLUE, -1)    # Pair: FG:Blue, BG:Default
    curses.init_pair(4, curses.COLOR_WHITE, -1)   # Pair: FG:White, BG:Default
    # -------- End of Initialization --------

    # -------- Start of show_splash function --------
    def show_splash():
        # ASCII art stored as raw string to avoid escape sequence issues
        ascii_art = r"""
 _____                    _             _     ___              _     
/__   \___ _ __ _ __ ___ (_)_ __   __ _| |   / __\__ _ _ __ __| |___ 
  / /\/ _ \ '__| '_ ` _ \| | '_ \ / _` | |  / /  / _` | '__/ _` / __|
 / / |  __/ |  | | | | | | | | | | (_| | | / /__| (_| | | | (_| \__ \
 \/   \___|_|  |_| |_| |_|_|_| |_|\__,_|_| \____/\__,_|_|  \__,_|___/
        """
        
        lines = ascii_art.strip().split('\n')
        max_line_width = max(len(line) for line in lines)
        start_y = (height - len(lines)) // 2
        for i, line in enumerate(lines):
            stdscr.addstr(start_y + i, (width - max_line_width) // 2, line, curses.color_pair(3))
        
        pressAnyKeyMsg = "Press any key to continue..."
        stdscr.addstr(height - 2, (width - len(pressAnyKeyMsg)) // 2, pressAnyKeyMsg, curses.color_pair(4) | curses.A_BOLD)



        stdscr.refresh()
        stdscr.getch()
    # -------- End of show_splash function --------

    show_splash()

curses.wrapper(main)