# coding: utf-8
"""
Interactive menu to select items
"""

import curses

EXIT_KEYS = [113, 27, 127, 10]
SPACE_KEY = 32


def show_options(
    title="TodoForge List",
    subtitle="Toggle tasks as completed or not",
    items=[],
    callback=None,
):
    screen = curses.initscr()

    def checked(todo):
        return todo.get("done")

    try:
        curses.start_color()
        curses.use_default_colors()

        curses.noecho()

        curses.curs_set(0)

        screen.keypad(1)

        curses.init_pair(1, curses.COLOR_GREEN, -1)
        highlighted = curses.color_pair(1)

        curses.init_pair(2, curses.COLOR_CYAN, -1)
        subtitle_style = curses.color_pair(2)

        curses.init_pair(3, curses.COLOR_WHITE, -1)
        info_style = curses.color_pair(3)

        current_pos = 0
        offset_y = 5

        while True:
            items_sorted = sorted(items, key=checked)

            no_items = len(items) if len(items) < 10 else 10
            if no_items == 0:
                return items

            screen.refresh()

            screen.addstr(2, 7, title, curses.A_BOLD | highlighted)
            screen.addstr(3, 7, subtitle, subtitle_style)

            pos = 0

            for item in items_sorted[:10]:
                is_done = item.get("done")
                status = " ✓ " if is_done else " x "

                if pos == current_pos:
                    screen.addstr(
                        pos + offset_y,
                        4,
                        "❯ {}  {}".format(status, item["title"]),
                        highlighted,
                    )
                else:
                    screen.addstr(
                        pos + offset_y, 4, "  {}  {}".format(status, item["title"])
                    )

                pos += 1

            if len(items) > 10:
                screen.addstr(pos + offset_y, 4, "   ...", info_style)

            screen.addstr(pos + offset_y + 3, 7, "<SPACE>", curses.A_BOLD | info_style)
            screen.addstr(pos + offset_y + 3, 18, "to toggle", info_style)

            screen.addstr(pos + offset_y + 4, 7, "<k, j>", curses.A_BOLD | info_style)
            screen.addstr(pos + offset_y + 4, 18, "navigate up and down", info_style)

            screen.addstr(pos + offset_y + 5, 7, "<q>", curses.A_BOLD | info_style)
            screen.addstr(pos + offset_y + 5, 18, "to exit", info_style)

            key = screen.getch()

            screen.erase()

            if key in (curses.KEY_DOWN, ord("j")):
                current_pos = current_pos + 1 if current_pos + 1 < no_items else 0
            elif key in (curses.KEY_UP, ord("k")):
                current_pos = current_pos - 1 if current_pos > 0 else no_items - 1
            elif key == SPACE_KEY:
                item_index = items.index(items_sorted[current_pos])
                items = callback(items, item_index)
            elif key in EXIT_KEYS:
                return items
    finally:
        curses.endwin()
