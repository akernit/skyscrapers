"""
Skyscrapers is a logic game in the placement of houses. In this game you need
to place buildings of different heights on the game board so that the number of
visible buildings from a certain position (the number with the arrow is a hint)
was equal to the number in the hint. The arrow in the tooltip indicates the
direction in which you want to look. The address of the repository in the GitHub
repository:
https://github.com/akernit/skyscrapers
"""

def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    lst = [x.strip() for x in open('{}'.format(path), 'r').readlines()]
    return lst


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    input_line = input_line[1:-1]
    if not input_line:
        return False
    else:
        count = 1

    max_value = input_line[0]

    for element_1 in input_line:

        if element_1 > max_value:
            max_value = element_1
            count += 1
        else:
            continue

        if count == pivot:
            return True
    else:
        return False


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game
    board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5',\
    '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215',\
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215',\
    '*35214*', '*41532*', '*2*1***'])
    False
    """
    board_data = "".join(element_1[1:-1] for idx, element_1 in enumerate(board)\
    if not (idx == 1 or idx == len(board) - 1))
    return False if board_data.count('?') > 0 else True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215',\
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215',\
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215',\
    '*35214*', '*41532*', '*2*1***'])
    False
    """

    for idx, lst in enumerate(board):
        if idx in range(1, len(board) - 1):
            current_lst = sorted(list(set(lst[1:-1])))
            if len(current_lst) != len(sorted(list(lst[1:-1]))):
                return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
    '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
    '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
    '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    if len(board) < 4:
        raise ValueError('Invalid array length was entered')

    def check(_block):

        status = False
        if _block[0].isdigit() and _block[-1].isdigit():
            status = True

        for pivot_idx, pivot in enumerate((_block[0], _block[-1])):
            if pivot.isdigit():
                if pivot_idx == 0:
                    pivot = int(_block[0])
                    input_line = _block[1:-1]
                else:
                    pivot = int(_block[-1])
                    input_line = list(reversed(_block[1:-1]))
            else:
                continue

            if pivot == 1 and not input_line:
                return True

            count = 1
            max_value = input_line[0]

            for element_1 in input_line:
                if element_1 > max_value:
                    max_value = element_1
                    count += 1

                if count == pivot:
                    if status:
                        status = False
                    break
            else:
                return False
        return True

    for idx, block in enumerate(board):

        if block[0] == block[-1] == '*' or idx in (0, len(board)):
            continue

        if not check(block):
            return False

    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of
    unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical
    case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*542315', '*35214*',\
    '*41532*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*',\
    '*41532*', '*2*1***'])
    False
    """
    if len(board) < 4:
        raise ValueError('Invalid array length was entered')

    for i in range(len(board)):
        block = []
        for j in range(len(board[i])):
            block.append(board[j][i])

        board.append("".join(x for x in block))

    board = board[int(len(board) / 2):]

    if len(board) < 4:
        raise ValueError('Invalid array length was entered')

    def check(_block):

        status = False
        if _block[0].isdigit() and _block[-1].isdigit():
            status = True

        for pivot_idx, pivot in enumerate((_block[0], _block[-1])):
            if pivot.isdigit():
                if pivot_idx == 0:
                    pivot = int(_block[0])
                    input_line = _block[1:-1]
                else:
                    pivot = int(_block[-1])
                    input_line = list(reversed(_block[1:-1]))
            else:
                continue

            if pivot == 1 and input_line:
                return True

            count = 1
            max_value = input_line[0]

            for element_1 in input_line:
                if element_1 > max_value:
                    max_value = element_1
                    count += 1

                if count == pivot:
                    if status:
                        status = False
                    break
            else:
                return False
        return True

    def is_unique(_board):

        for _idx, lst in enumerate(_board):
            if _idx in range(1, len(_board) - 1):
                current_lst = sorted(list(set(lst[1:-1])))
                if len(current_lst) != len(sorted(list(lst[1:-1]))):
                    return False

        return True

    for idx, block in enumerate(board):

        if block[0] == block[-1] == '*' or idx in (0, len(board)):
            continue

        if not check(block):
            return False

    return True and is_unique(board)


def check_skyscrapers(input_path: str):
    """
    Main function to check.txt the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """

    def check(_block):

        status = False
        if _block[0].isdigit() and _block[-1].isdigit():
            status = True

        for pivot_idx, pivot in enumerate((_block[0], _block[-1])):
            if pivot.isdigit():
                if pivot_idx == 0:
                    pivot = int(_block[0])
                    input_line = _block[1:-1]
                else:
                    pivot = int(_block[-1])
                    input_line = list(reversed(_block[1:-1]))
            else:
                continue

            if pivot == 1 and not input_line:
                return True

            count = 1
            max_value = input_line[0]

            for element_1 in input_line:
                if element_1 > max_value:
                    max_value = element_1
                    count += 1

                if count == pivot:
                    if status:
                        status = False
                    break
            else:
                return False
        return True

    rows = [x.strip() for x in open('{}'.format(input_path), 'r').readlines()]

    main_board_data = "".join(element_1[1:-1] for idx, element_1 in\
    enumerate(rows) if not (idx == 1 or idx == len(rows) - 1))
    if main_board_data.count('?') > 0:
        return False

    for idx, lst in enumerate(rows):
        if idx in range(1, len(rows) - 1):
            current_lst = sorted(list(set(lst[1:-1])))
            if len(current_lst) != len(sorted(lst[1:-1])):
                return False

    if len(rows) < 4:
        raise ValueError('Invalid array length was entered')

    for i in range(len(rows)):
        block = []
        for j in range(len(rows[i])):
            block.append(rows[j][i])

        rows.append("".join(x for x in block))

    columns = rows[int(len(rows) / 2):]

    rows_columns = rows + columns

    for idx, block in enumerate(rows_columns):

        if block[0] == block[-1] == '*' or idx in (0, len(rows_columns)):
            continue

        if not check(block):
            return False

    return True


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
