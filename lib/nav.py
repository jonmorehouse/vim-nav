import re
import sys

try:
    import vim
except ImportError:
    print "this must be called within the vim runtime..."
    sys.exit(1)


DELIMITERS = ['_', '-', ',', '|', '`', '(', ')', '[', ']', '>', '<', '/', '#', '*', '+']


def move(direction, count=1):
    if count == 0:
        return

    buf = vim.current.buffer
    (start_row, start_col) = vim.current.window.cursor

    # this is an edge case, if we are trying to move backwards from the top,
    # leftmost position we simply exit
    if start_row == 1 and start_col == 0 and direction == -1:
        return

    # check to make sure that the start character exists
    try:
        start_char = buf[start_row -1][start_col] 
    except IndexError:
        start_char = None
    
    # if the character is currently a whiteSpace, then we just walk to the
    # right until we find a non-whitespace character. A white space is either
    # an empty cursor / line or an actual space
    is_empty = start_char is None or re.match(r'\s', start_char) is not None

    row = start_row - 1
    # to start, we look one element to the right
    col = start_col + direction
    moved = 0

    while True:
        # check going out of bounds on the row, this denotes that we have
        # reached an edge of the file
        if row < 0:
            row = 0
            col = 0
            break
        elif row > len(buf) - 1:
            row = len(buf) - 1 
            col = len(buf[row]) - 1
            break

        # check going out of bounds on an individual line, as this denotes we
        # need to go up or down
        if col < 0:
            row -= 1
            col = len(buf[row]) - 1 
            continue
        elif col >= len(buf[row]):
            row += direction
            col = 0 if direction == 1 else len(buf[row])-1
            continue

        line = buf[row]
        char = buf[row][col]

        # we have an actual character which we can compare to our logic to see
        # if we should break
        # the start char was empty and our current one isn't
        if is_empty and not re.match(r'\s', char):
            break

        # when we hit an empty character, we need to act carefully. If we've
        # moved more than a single character, for instance throughout a word
        # then we want to go to the previous character.
        # if we hit a white space on the first element, then we want to keep
        # going to find the next non-whitespace element
        if re.match(r'\s', char) or re.match(r'\n', char):
            if moved > 0:
                col -= direction
                # if col is less than zero, it means we are moving forward and
                # the last position was the last character of the previous
                # line
                if col < 0 and row > 0:
                    row -= 1
                    col = len(buf[row])-1
                    # if col is greater, than we are moving from right to left
                    # (because this is a backwards step) and that means the logical
                    # previous position was the first character of the previous
                    # line
                elif col >= len(buf[row])-1 and row < len(buf)-2:
                    row += 1
                    col = 0
                break
            else:
                is_empty = True

        # if we've move more than one character, are going backwards and are on
        # the first element in a list then we can break 
        if col == 0 and direction == -1 and moved > 0:
            break

        # if we've moved more than one character to the right and are on the end of a line we can break
        if col == len(buf[row])-1 and direction == 1 and moved > 0:
            break

        # the current character has a different case than the start char
        if (char.lower() == char) != (start_char == start_char.lower()):
            break
            
        # if the current character is one of our delimiter characters break,
        # unless it is the same delimiter as before.
        should_continue = True
        for delimiter in DELIMITERS:
            if char == delimiter:
                if delimiter == start_char and moved > 0:
                    should_continue = False
                    break
                elif moved > 0:
                    should_continue = False
                    break

        if not should_continue:
            break

        col += direction
        moved += 1

    # move to the correct character
    vim.current.window.cursor = (row+1, col)


def forwards(count=1):
    move(1, count)


def backwards(count=1):
    move(-1, count)
