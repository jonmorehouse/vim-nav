import re
import sys

try:
    import vim
except ImportError:
    print "this must be called within the vim runtime..."
    sys.exit(1)


DELIMITERS = ['_', '-', ',', '|', '`', '(', ')', '[', ']']


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
        try:
            line = buf[row]
        except IndexError:
            # we reached the end of the file
            row = row-direction
            col = len(buf[row])
            break

        try:
            char = line[col]
        except IndexError:
            # we reached the end of the line, onto the next line
            row = row + direction
            col = 0
            continue

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
            # if we've moved more than a single character then go back to the
            # previous element if it is in the range on the current line
            if moved > 0 and col-direction > 0 and col-direction < len(line):
                col -= direction
                break
            else:
                is_empty = True

        # the current character has a different case than the start char
        if (char.lower() == char) != (start_char == start_char.lower()):
            break
            
        # if the current character is one of our delimiter characters break!
        if char in DELIMITERS:
            break

        # no match, we just move to the right once
        col += direction
        moved += 1

    # move to the correct character
    vim.current.window.cursor = (row+1, col)


def forwards(count=1):
    move(1, count)


def backwards(count=1):
    move(-1, count)
