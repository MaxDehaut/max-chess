from stockfish import Stockfish

def main():
    """
    """
    stockfish = Stockfish(
        depth=18,
        parameters={ "Hash": 16, # Default size is 16 MB
                     "Minimum Thinking Time": 30,
                     "Threads": 2,
                     "UCI_Elo": 1350
                    })
    stockfish.get_board_visual()

if __name__ == "__main__":
    main()

# stockfish.get_best_move()
# stockfish.get_best_move(wtime=1000, btime=1000)
# stockfish.get_best_move_time(1000)
# stockfish.get_wdl_stats()