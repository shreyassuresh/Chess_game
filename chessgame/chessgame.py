import streamlit as st
import copy

# Initialize the board
initial_board = [
    ["\u265C", "\u265E", "\u265D", "\u265B", "\u265A", "\u265D", "\u265E", "\u265C"],  # Black back rank
    ["\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F"],  # Black pawns
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # Empty row
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # Empty row
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # Empty row
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],  # Empty row
    ["\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659"],  # White pawns
    ["\u2656", "\u2658", "\u2657", "\u2655", "\u2654", "\u2657", "\u2658", "\u2656"]   # White back rank
]

# Utility functions
def render_board(board):
    """Render the chess board in Streamlit."""
    board_html = "<div style='display: grid; grid-template-columns: repeat(8, 1fr); width: 320px;'>"
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"
            board_html += f"<div style='width: 40px; height: 40px; background-color: {color}; display: flex; align-items: center; justify-content: center; font-size: 24px;'>{cell}</div>"
    board_html += "</div>"
    st.markdown(board_html, unsafe_allow_html=True)

def parse_move(move):
    start_col = ord(move[0]) - ord('a')
    start_row = 8 - int(move[1])
    end_col = ord(move[2]) - ord('a')
    end_row = 8 - int(move[3])
    return (start_row, start_col, end_row, end_col)

def move_piece(board, start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]
    board[start_row][start_col] = "  "
    board[end_row][end_col] = piece

def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece):
    direction = -1 if piece == "\u2659" else 1
    start_row_offset = 6 if piece == "\u2659" else 1

    if start_col == end_col and board[end_row][end_col] == "  ":
        if (end_row == start_row + direction):
            return True
        elif (start_row == start_row_offset and end_row == start_row + 2 * direction):
            if board[start_row + direction][start_col] == "  ":
                return True

    if abs(start_col - end_col) == 1 and end_row == start_row + direction and board[end_row][end_col] != "  ":
        return True

    return False

def is_valid_move(board, start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]
    if piece in ["\u2659", "\u265F"]:  # Pawn movement
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece)
    return True

def highlight_selected_piece(board, selected_square):
    highlighted_board = copy.deepcopy(board)
    row, col = selected_square
    highlighted_board[row][col] = f"<span style='background-color: yellow;'>{board[row][col]}</span>"
    return highlighted_board

# Streamlit app
def main():
    st.title("Chess Game")

    if "board" not in st.session_state:
        st.session_state.board = copy.deepcopy(initial_board)
    if "turn" not in st.session_state:
        st.session_state.turn = "White"
    if "selected_square" not in st.session_state:
        st.session_state.selected_square = None

    st.subheader(f"{st.session_state.turn}'s turn")

    # Handle piece selection
    selected_square = st.session_state.selected_square
    if selected_square:
        highlighted_board = highlight_selected_piece(st.session_state.board, selected_square)
        render_board(highlighted_board)
    else:
        render_board(st.session_state.board)

    col1, col2 = st.columns(2)

    with col1:
        select_square = st.text_input("Select a square (e.g., 'e2'):")
        if st.button("Select"):
            if len(select_square) == 2:
                row, col = parse_move(select_square + select_square)[0:2]
                if 0 <= row < 8 and 0 <= col < 8:
                    st.session_state.selected_square = (row, col)
                else:
                    st.error("Invalid square. Try again.")
            else:
                st.error("Invalid input. Enter a square like 'e2'.")

    with col2:
        target_square = st.text_input("Move to square (e.g., 'e4'):")
        if st.button("Move"):
            if selected_square and len(target_square) == 2:
                start_row, start_col = selected_square
                end_row, end_col = parse_move(target_square + target_square)[0:2]

                piece = st.session_state.board[start_row][start_col]
                if is_valid_move(st.session_state.board, start_row, start_col, end_row, end_col):
                    move_piece(st.session_state.board, start_row, start_col, end_row, end_col)
                    st.session_state.turn = "Black" if st.session_state.turn == "White" else "White"
                    st.session_state.selected_square = None
                else:
                    st.error("Invalid move. Try again.")
            else:
                st.error("Please select a valid piece and destination.")

if __name__ == "__main__":
    main()
    # this is just a prototype ....
