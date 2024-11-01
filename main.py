"""
Main  file
"""
import chess.game as cg
import chess.AI as ai
import configuration as cfg
import pygame as p
import sys
from multiprocessing import Process, Queue


def animate_move(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square

    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count,
                    move.start_col + d_col * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)

        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * cfg.SQUARE_SIZE,
                            move.end_row * cfg.SQUARE_SIZE,
                            cfg.SQUARE_SIZE,
                            cfg.SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)

        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 \
                    if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * cfg.SQUARE_SIZE,
                                    enpassant_row * cfg.SQUARE_SIZE,
                                    cfg.SQUARE_SIZE,
                                    cfg. SQUARE_SIZE)
            screen.blit(cfg.IMAGES[move.piece_captured], end_square)

        # draw moving piece
        screen.blit(cfg.IMAGES[move.piece_moved],
                    p.Rect(col * cfg.SQUARE_SIZE,
                           row * cfg.SQUARE_SIZE,
                           cfg.SQUARE_SIZE,
                           cfg.SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_board(screen):
    """
    Draw the board
    """
    global colors
    colors = [p.Color(cfg.COLOR_WHITE), p.Color(cfg.COLOR_BLACK)]
    for row in range(cfg.DIMENSION):
        for column in range(cfg.DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * cfg.SQUARE_SIZE,
                                              row * cfg.SQUARE_SIZE,
                                              cfg.SQUARE_SIZE,
                                              cfg.SQUARE_SIZE))

def draw_endgame_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color(cfg.FONT_COLOR))
    text_location = p.Rect(0, 0,
                           cfg.BOARD_WIDTH,
                           cfg.BOARD_HEIGHT).move(cfg.BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                  cfg.BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color(cfg.FONT_COLOR))
    screen.blit(text_object, text_location.move(2, 2))

def draw_move_history(screen, current_game, font):
    """
    Draws the move history
    """
    move_history_rect = p.Rect(cfg.BOARD_WIDTH, 0, cfg.MOVE_PANEL_WIDTH, cfg.MOVE_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(cfg.COLOR_HISTORY), move_history_rect)
    move_history = current_game.move_history
    move_texts = []
    for i in range(0, len(move_history), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_history[i]) + " "
        if i + 1 < len(move_history):
            move_string += str(move_history[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding

    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color(cfg.FONT_COLOR))
        text_location = move_history_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def draw_pieces(screen, board):
    """
    Draw the pieces on the board
    """
    for row in range(cfg.DIMENSION):
        for column in range(cfg.DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(cfg.IMAGES[piece], p.Rect(column * cfg.SQUARE_SIZE,
                                                      row * cfg.SQUARE_SIZE,
                                                      cfg.SQUARE_SIZE,
                                                      cfg.SQUARE_SIZE))

def get_board_ready(screen, current_game, valid_moves, square_selected):
    """
    Prepare the board
    """
    draw_board(screen)
    set_highlighted(screen, current_game, valid_moves, square_selected)
    draw_pieces(screen, current_game.board)

def load_images():
    """
    Initialize the images
    """
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        cfg.IMAGES[piece] = p.transform.scale(p.image.load("images/" + cfg.IMAGES_SET + "/" + piece + ".png"), (cfg.SQUARE_SIZE, cfg.SQUARE_SIZE))

def main():
    """
    Starting point
    """
    p.init()
    screen = p.display.set_mode((cfg.BOARD_WIDTH + cfg.MOVE_PANEL_WIDTH, cfg.BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    move_history_font = p.font.SysFont("Arial", 14, False, False)
    load_images()

    current_game = cg.ChessGame()
    valid_moves = current_game.get_valid_moves()

    ai_thinking = False
    animate = False
    game_over = False
    move_finder_process = None
    move_made = False
    move_undone = False
    player_one = False
    player_two = False
    running = True

    square_selected = ()
    player_clicks = []

    while running:
        human_turn = (current_game.white_to_move and player_one) or (not current_game.white_to_move and player_two)

        for e in p.event.get():

            if e.type == p.QUIT:
                p.quit()
                sys.exit()

            elif e.type == p.MOUSEBUTTONDOWN:

                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // cfg.SQUARE_SIZE
                    row = location[1] // cfg.SQUARE_SIZE

                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)

                    if len(player_clicks) == 2 and human_turn:
                        move = cg.ChessMove(player_clicks[0], player_clicks[1], current_game.board)

                        for i in enumerate(valid_moves):

                            if move == valid_moves[i]:
                                current_game.move_a_piece(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []

                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:

                if e.key == p.K_z:  # undo when 'z' is pressed
                    current_game.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    current_game = cg.ChessGame()
                    valid_moves = current_game.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ai.findBestMove,
                                              args=(current_game,
                                                    valid_moves,
                                                    return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ai.findRandomMove(valid_moves)
                current_game.move_a_piece(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animate_move(current_game.move_history[-1], screen, current_game.board, clock)
            valid_moves = current_game.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        get_board_ready(screen, current_game, valid_moves, square_selected)

        if not game_over:
            draw_move_history(screen, current_game, move_history_font)

        if current_game.checkmate:
            game_over = True
            if current_game.white_to_move:
                draw_endgame_text(screen, "Black wins by checkmate")
            else:
                draw_endgame_text(screen, "White wins by checkmate")

        elif current_game.stalemate:
            game_over = True
            draw_endgame_text(screen, "Stalemate")

        clock.tick(cfg.MAX_FPS)
        p.display.flip()

def set_highlighted(screen, current_game, valid_moves, square_selected):
    """
    Highlight selected square
    """
    if (len(current_game.move_history)) > 0:
        last_move = current_game.move_history[-1]
        s = p.Surface((cfg.SQUARE_SIZE, cfg.SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color(cfg.COLOR_SELECTED))
        screen.blit(s, (last_move.end_col * cfg.SQUARE_SIZE, last_move.end_row * cfg.SQUARE_SIZE))

    if square_selected != ():
        row, col = square_selected

        if current_game.board[row][col][0] == (
                # square_selected is a piece that can be moved
                'w' if current_game.white_to_move else 'b'):
            s = p.Surface((cfg.SQUARE_SIZE, cfg.SQUARE_SIZE))

            # transparency value 0 -> transparent, 255 -> opaque
            s.set_alpha(100)
            s.fill(p.Color(cfg.COLOR_TARGET))
            screen.blit(s, (col * cfg.SQUARE_SIZE, row * cfg.SQUARE_SIZE))

            # highlight moves from that square
            s.fill(p.Color(cfg.COLOR_PATH))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * cfg.SQUARE_SIZE, move.end_row * cfg.SQUARE_SIZE))

if __name__ == "__main__":
    main()
