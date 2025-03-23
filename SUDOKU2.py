import streamlit as st
import numpy as np
import random
import math

# Configurazione pagina
st.set_page_config(page_title="Sudoku Semplice 4x4")

# Inizializzazione dello stato della sessione
if 'board' not in st.session_state:
    st.session_state.board = None
if 'solution' not in st.session_state:
    st.session_state.solution = None
if 'original_board' not in st.session_state:
    st.session_state.original_board = None
if 'game_status' not in st.session_state:
    st.session_state.game_status = None  # Può essere None, "success", o "error"

# Funzioni per la generazione e risoluzione del Sudoku
def is_valid(board, row, col, num):
    """Verifica se un numero può essere inserito nella posizione data"""
    # Controlla riga
    for x in range(4):
        if board[row][x] == num:
            return False
    
    # Controlla colonna
    for x in range(4):
        if board[x][col] == num:
            return False
    
    # Controlla quadrante 2x2
    box_row = (row // 2) * 2
    box_col = (col // 2) * 2
    
    for i in range(2):
        for j in range(2):
            if board[box_row + i][box_col + j] == num:
                return False
    
    return True

def find_empty(board):
    """Trova una cella vuota nella griglia"""
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    """Risolve il Sudoku utilizzando backtracking"""
    board_copy = [row[:] for row in board]  # Crea una copia per evitare di modificare l'originale
    
    empty_cell = find_empty(board_copy)
    if not empty_cell:
        return board_copy  # Puzzle risolto
    
    row, col = empty_cell
    
    for num in range(1, 5):  # Numeri da 1 a 4 per griglia 4x4
        if is_valid(board_copy, row, col, num):
            board_copy[row][col] = num
            
            result = solve_sudoku(board_copy)
            if result:
                return result
            
            board_copy[row][col] = 0  # Backtrack
    
    return None

def generate_sudoku():
    """Genera un puzzle Sudoku 4x4"""
    # Crea una griglia vuota
    board = [[0 for _ in range(4)] for _ in range(4)]
    
    # Riempi alcune celle con numeri casuali
    for _ in range(4):  # Inserisci solo alcuni numeri iniziali
        row, col = random.randint(0, 3), random.randint(0, 3)
        num = random.randint(1, 4)
        if is_valid(board, row, col, num):
            board[row][col] = num
    
    # Risolvi per riempire il resto
    solved_board = solve_sudoku(board)
    if not solved_board:
        # Se non riusciamo a risolvere, riprova
        return generate_sudoku()
    
    # Crea il puzzle rimuovendo alcuni numeri
    puzzle = [row[:] for row in solved_board]
    
    # Rimuovi circa metà dei numeri
    cells = [(i, j) for i in range(4) for j in range(4)]
    random.shuffle(cells)
    
    for i in range(8):  # Rimuovi 8 celle (metà della griglia 4x4)
        if i < len(cells):
            row, col = cells[i]
            puzzle[row][col] = 0
    
    return puzzle, solved_board

def check_solution(current_board, solution_board):
    """Verifica se il Sudoku è stato risolto correttamente"""
    # Verifica che la griglia sia completamente riempita
    if find_empty(current_board):
        return False
    
    # Confronta con la soluzione corretta
    for i in range(4):
        for j in range(4):
            if current_board[i][j] != solution_board[i][j]:
                return False
    return True

def verify_board_validity(board):
    """Verifica se la tabella corrente rispetta le regole del Sudoku"""
    # Verifica se ci sono celle vuote
    if find_empty(board):
        return False
    
    # Verifica righe
    for row in range(4):
        if sorted([board[row][col] for col in range(4)]) != [1, 2, 3, 4]:
            return False
    
    # Verifica colonne
    for col in range(4):
        if sorted([board[row][col] for row in range(4)]) != [1, 2, 3, 4]:
            return False
    
    # Verifica quadranti 2x2
    for box_row in range(0, 4, 2):
        for box_col in range(0, 4, 2):
            box_values = []
            for i in range(2):
                for j in range(2):
                    box_values.append(board[box_row + i][box_col + j])
            if sorted(box_values) != [1, 2, 3, 4]:
                return False
    
    return True

# Funzione per gestire la verifica della soluzione
def verify_solution():
    if not st.session_state.board:
        return
    
    # Controlla se ci sono celle vuote
    has_empty = find_empty(st.session_state.board)
    if has_empty:
        st.session_state.game_status = "incomplete"
        return
    
    # Verifica con la soluzione originale
    is_correct = check_solution(st.session_state.board, st.session_state.solution)
    
    if is_correct:
        st.session_state.game_status = "success"
    else:
        # Verificare se la soluzione rispetta le regole del Sudoku anche se diversa dalla soluzione attesa
        if verify_board_validity(st.session_state.board):
            st.session_state.game_status = "valid_but_different"
        else:
            st.session_state.game_status = "error"

# Titolo app
st.title("Sudoku Semplice 4x4")

# Pulsanti in una riga
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Genera nuovo puzzle'):
        puzzle, solution = generate_sudoku()
        st.session_state.board = puzzle
        st.session_state.solution = solution
        st.session_state.original_board = [row[:] for row in puzzle]
        st.session_state.game_status = None

with col2:
    if st.session_state.solution and st.button('Mostra soluzione'):
        st.session_state.board = st.session_state.solution
        st.session_state.game_status = "solution_shown"

with col3:
    if st.session_state.board and st.button('Verifica soluzione'):
        verify_solution()

# Visualizza stato del gioco
if st.session_state.game_status == "success":
    st.balloons()  # Lancia palloncini per celebrare
    st.success("🤓 We have a numbers nerd here eh 🤓")
elif st.session_state.game_status == "error":
    st.error("🤠 don't shoot randomly cowboy 🤠")
elif st.session_state.game_status == "incomplete":
    st.warning("⚠️ Complete all cells before checking the solution.")
elif st.session_state.game_status == "valid_but_different":
    st.warning("⚠️ Your solution is good but different from the expected solution.")
elif st.session_state.game_status == "solution_shown":
    st.info("ℹ️ This is the correct solution to the puzzle.")

# Istruzioni
if st.session_state.board:
    st.write("Complete the puzzle by inserting numbers 1 to 4 in each empty cell.")
    
    # Creazione della griglia Sudoku con layout quadrato appropriato
    # Ogni riga è una riga di 4 celle
    for i in range(4):
        # Crea 4 colonne per ogni riga
        row_cols = st.columns(4)
        
        for j in range(4):
            with row_cols[j]:
                # Verifica se è una posizione originale (fissa)
                is_original = st.session_state.original_board[i][j] != 0
                
                # Stile con bordi più marcati per i quadranti 2x2
                box_style = "font-weight: bold; border: 1px solid #ddd; "
                
                # Aggiungi bordi più spessi per i quadranti 2x2
                if i % 2 == 0 and i > 0:
                    box_style += "border-top: 3px solid black; "
                if j % 2 == 0 and j > 0:
                    box_style += "border-left: 3px solid black; "
                
                # Valore corrente
                current_value = st.session_state.board[i][j]
                display_value = "" if current_value == 0 else str(current_value)
                
                # Stile diverso per numeri originali
                if is_original:
                    bg_color = "#f0f0f0"  # Grigio chiaro per i numeri originali
                    text_style = "font-weight: bold;"
                else:
                    bg_color = "white"
                    text_style = "color: blue;"
                
                # Se è una posizione originale, mostra solo il valore
                if is_original:
                    st.markdown(
                        f"<div style='text-align: center; height: 60px; line-height: 60px; "
                        f"font-size: 24px; background-color: {bg_color}; {box_style} {text_style}'>"
                        f"{display_value}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    # Crea input per l'utente
                    input_key = f"cell_{i}_{j}"
                    input_value = st.text_input(
                        "",
                        value=display_value,
                        key=input_key,
                        max_chars=1,
                        label_visibility="collapsed",
                    )
                    
                    # Elabora l'input dell'utente
                    if input_value and input_value.isdigit():
                        num = int(input_value)
                        if 1 <= num <= 4:
                            st.session_state.board[i][j] = num
                        else:
                            st.session_state.board[i][j] = 0
                    elif not input_value:
                        st.session_state.board[i][j] = 0
else:
    # Mostra istruzioni se non c'è un gioco in corso
    st.write("Clicca su 'Genera nuovo puzzle' per iniziare a giocare.")
    st.write("""
    4x4 Sudoku rules:
    1. Enter the numbers 1 to 4 in each empty cell
    2. Each row must contain the numbers 1 to 4 without repetition
    3. Each column must contain the numbers 1 to 4 without repetition
    4. Each 2x2 quadrant must contain the numbers 1 to 4 without repetitions
    “"”)
