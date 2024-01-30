import sys,os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import font, messagebox
import ChessEngine, ChessAI
from multiprocessing import Process, Queue
import pygame as p

class MainGame:
   global selected_mode, radio, timer_combobox, timer_values
   def __init__(self, root):
      self.root=root
      self.BOARD_WIDTH = self.BOARD_HEIGHT = 512
      self.MOVE_LOG_PANEL_WIDTH = 250
      self.MOVE_LOG_PANEL_HEIGHT = self.BOARD_HEIGHT
      self.DIMENSION = 8
      self.SQUARE_SIZE = self.BOARD_HEIGHT // self.DIMENSION
      self.MAX_FPS = 1
      self.IMAGES = {}
      self.selected_time = timer_combobox.get()
      if self.selected_time != "No Timer":
         self.black_time_left = self.white_time_left = timer_values[self.selected_time]

   def loadImages(self):
      p.display.set_caption("Chess7Dee")
      Icon = p.image.load('images/bQ.png')
      p.display.set_icon(Icon)
      pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
      for piece in pieces:
         self.IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (self.SQUARE_SIZE, self.SQUARE_SIZE))

   def draw_timer(self, screen, black_time_left=00, white_time_left=00):
      font = p.font.Font(None, 30)
      white_timer = font.render(f"white's time: {black_time_left}s", True, p.Color("black"))
      black_timer = font.render(f"black's time: {white_time_left}s.", True, p.Color("white"))
      white_timer_rect = p.Rect(self.BOARD_WIDTH + self.MOVE_LOG_PANEL_WIDTH - 1.2*white_timer.get_width(), self.BOARD_HEIGHT - white_timer.get_height() - 20, white_timer.get_width() + 20, white_timer.get_height() + 20)
      black_timer_rect = p.Rect(self.BOARD_WIDTH + self.MOVE_LOG_PANEL_WIDTH - 1.2*black_timer.get_width(), white_timer_rect.y - black_timer.get_height() - 20, black_timer.get_width() + 20, black_timer.get_height() + 20)

      p.draw.rect(screen, p.Color("green"), white_timer_rect)
      p.draw.rect(screen, p.Color("blue"), black_timer_rect)
      p.draw.rect(screen, p.Color("yellow"), white_timer_rect, 1)
      p.draw.rect(screen, p.Color("yellow"), black_timer_rect, 1)

      text_rect_red = white_timer.get_rect()
      text_rect_white = black_timer.get_rect()
      text_rect_red.midtop = (white_timer_rect.centerx, white_timer_rect.y + 10)
      text_rect_white.midtop = (black_timer_rect.centerx, black_timer_rect.y + 10)

      screen.blit(white_timer, text_rect_red)
      screen.blit(black_timer, text_rect_white)

   def main(self):
      p.init()
      screen = p.display.set_mode((self.BOARD_WIDTH + self.MOVE_LOG_PANEL_WIDTH, self.BOARD_HEIGHT))
      clock = p.time.Clock()
      screen.fill(p.Color("white"))
      game_state = ChessEngine.GameState()
      valid_moves = game_state.getValidMoves()
      move_made = False
      animate = False
      self.loadImages()
      running = True
      square_selected = ()
      player_clicks = []
      game_over = False
      ai_thinking = False
      move_undone = False
      move_finder_process = None
      move_log_font = p.font.SysFont("Arial", 14, False, False)

      player = selected_mode.get()
      if player == 'multiplayer':
         player_one = True
         player_two = True
      else:
         chooseAs= radio.get()
         if chooseAs == 0:
            player_one = True
            player_two = False
         elif chooseAs == 1:
            player_one = False
            player_two = True

      while running:
         human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
         for e in p.event.get():
            if e.type == p.QUIT:
               if not game_over:
                  ans = tk.messagebox.askquestion('Resign','You will loose this game!')
                  if ans == "yes":
                     self.root.deiconify()
                     p.quit()
                  else:
                     pass
               else:
                  self.root.deiconify()
                  p.quit()
            elif e.type == p.MOUSEBUTTONDOWN:
               if not game_over:
                  location = p.mouse.get_pos()
                  col = location[0] // self.SQUARE_SIZE
                  row = location[1] // self.SQUARE_SIZE
                  if square_selected == (row, col) or col >= 8: 
                     square_selected = () 
                     player_clicks = []
                  else:
                     square_selected = (row, col)
                     player_clicks.append(square_selected)
                  if len(player_clicks) == 2 and human_turn:
                     move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                     for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                           game_state.makeMove(valid_moves[i])
                           move_made = True
                           animate = True
                           square_selected = ()
                           player_clicks = []
                     if not move_made:
                        player_clicks = [square_selected]
            elif e.type == p.KEYDOWN:
               if player != 'multiplayer':
                  if e.key == p.K_z:
                     game_state.undoMove()
                     move_made = True
                     animate = False
                     game_over = False
                     if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                     move_undone = True
               if e.key == p.K_r:
                  ans = tk.messagebox.askquestion('Re-start','All the parameters will be set to initial.')
                  if ans == 'yes':
                     game_state = ChessEngine.GameState()
                     valid_moves = game_state.getValidMoves()
                     square_selected = ()
                     player_clicks = []
                     move_made = False
                     animate = False
                     game_over = False
                     if self.selected_time != "No Timer":
                        self.black_time_left = self.white_time_left = timer_values[self.selected_time] 
                     if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                     move_undone = True
                  else:
                     pass
         if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
               ai_thinking = True
               return_queue = Queue()
               move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
               move_finder_process.start()
            if not move_finder_process.is_alive():
               ai_move = return_queue.get()
               if ai_move is None:
                  ai_move = ChessAI.findRandomMove(valid_moves)
               game_state.makeMove(ai_move)
               move_made = True
               animate = True
               ai_thinking = False
         if move_made:
            if animate:
               self.animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False
         self.drawGameState(screen, game_state, valid_moves, square_selected)
         if not game_over:
            self.drawMoveLog(screen, game_state, move_log_font)
            if self.selected_time != "No Timer":

               if game_state.white_to_move:
                  if self.black_time_left ==0:
                     self.drawEndGameText(screen,"Black wins by timeout!")
                     game_over = True
                  else:
                     self.black_time_left -= 1
               elif not game_state.white_to_move:
                  if self.white_time_left == 0:
                     self.drawEndGameText(screen,"White wins by timeout!")
                     game_over = True
                  else:
                     self.white_time_left -= 1

         if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
               self.drawEndGameText(screen, "Black wins by checkmate")
            else:
               self.drawEndGameText(screen, "White wins by checkmate")

         if self.selected_time != "No Timer":
            self.draw_timer(screen, self.black_time_left, self.white_time_left)
         p.display.flip()
         clock.tick(self.MAX_FPS)

   def drawGameState(self, screen, game_state, valid_moves, square_selected):
      self.drawBoard(screen)
      self.highlightSquares(screen, game_state, valid_moves, square_selected)
      self.drawPieces(screen, game_state.board)

   def drawBoard(self, screen):
      global colors
      self.colorWhite = p.Color("white")
      self.colorBlack = p.Color("light green")
      colors = [self.colorWhite, self.colorBlack]
      for row in range(self.DIMENSION):
         for column in range(self.DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

   def highlightSquares(self, screen, game_state, valid_moves, square_selected):
      if (len(game_state.move_log)) > 0:
         last_move = game_state.move_log[-1]
         s = p.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
         s.set_alpha(100)
         s.fill(p.Color('blue'))
         screen.blit(s, (last_move.end_col * self.SQUARE_SIZE, last_move.end_row * self.SQUARE_SIZE))
      if square_selected != ():
         row, col = square_selected
         if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            s = p.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('red'))
            screen.blit(s, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
            s.fill(p.Color('gold'))
            for move in valid_moves:
               if move.start_row == row and move.start_col == col:
                  screen.blit(s, (move.end_col * self.SQUARE_SIZE, move.end_row * self.SQUARE_SIZE))

   def drawPieces(self, screen, board):
      for row in range(self.DIMENSION):
         for column in range(self.DIMENSION):
            piece = board[row][column]
            if piece != "--":
               screen.blit(self.IMAGES[piece], p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

   def drawMoveLog(self, screen, game_state, font):
      move_log_rect = p.Rect(self.BOARD_WIDTH, 0, self.MOVE_LOG_PANEL_WIDTH, self.MOVE_LOG_PANEL_HEIGHT)
      p.draw.rect(screen, p.Color('black'), move_log_rect)
      move_log = game_state.move_log
      move_texts = []
      for i in range(0, len(move_log), 2):
         move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
         if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
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
         text_object = font.render(text, True, p.Color('white'))
         text_location = move_log_rect.move(padding, text_y)
         screen.blit(text_object, text_location)
         text_y += text_object.get_height() + line_spacing

   def drawEndGameText(self, screen, text):
      font = p.font.SysFont("Helvetica", 32, True, False)
      text_object = font.render(text, False, p.Color("gray"))
      text_location = p.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT).move(self.BOARD_WIDTH / 2 - text_object.get_width() / 2, self.BOARD_HEIGHT / 2 - text_object.get_height() / 2)
      screen.blit(text_object, text_location)
      text_object = font.render(text, True, p.Color('black'))
      screen.blit(text_object, text_location.move(2, 2))

   def animateMove(self, move, screen, board, clock):
      global colors
      d_row = move.end_row - move.start_row
      d_col = move.end_col - move.start_col
      frames_per_square = 10
      frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
      for frame in range(frame_count + 1):
         row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
         self.drawBoard(screen)
         self.drawPieces(screen, board)
         color = colors[(move.end_row + move.end_col) % 2]
         end_square = p.Rect(move.end_col * self.SQUARE_SIZE, move.end_row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
         p.draw.rect(screen, color, end_square)
         if move.piece_captured != '--':
               if move.is_enpassant_move:
                  enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                  end_square = p.Rect(move.end_col * self.SQUARE_SIZE, enpassant_row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
               screen.blit(self.IMAGES[move.piece_captured], end_square)
         screen.blit(self.IMAGES[move.piece_moved], p.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
         p.display.flip()
         clock.tick(60)

def homeScreen():
   global root, radio, selected_mode, timer_combobox, timer_values
   root= tk.Tk()
   root.title('Home Screen')
   root.geometry('800x400+400+20')
   img = PhotoImage(file='logo_img.png')
   root.iconphoto(False, img)
   root.resizable(False, False) 

   label_font = font.Font(size=34)
   btn_font = font.Font(size=20)
   heading=tk.Label(root, text="Chess7Dee", border='7px',foreground='Green', font=label_font)
   heading.pack(fill='x', padx=10)
   Label(root, image=img).pack(pady=20)

   mode= Label(root,text='Play with', font=btn_font)
   mode.pack(side='left', anchor='n', padx=10, pady=0)
   mode_setting = ['play with chess bot', 'multiplayer']
   selected_mode = tk.StringVar()
   mode_combobox = ttk.Combobox(root, textvariable=selected_mode, values=mode_setting, state="readonly")
   mode_combobox.pack(side='left', anchor='n')
   selected_mode.set(mode_setting[1])

   playeras = Label(root, text='As:')
   playeras.pack(side='left', anchor='n', padx=20)
   radio = IntVar()
   asWhite = Radiobutton(root, text="WHITE", value=0, variable=radio, state='disabled')
   asWhite.pack(ipadx=5,side='left', anchor='n')
   asBlack = Radiobutton(root, text="BLACK", value=1, variable=radio,  state='disabled')
   asBlack.pack(ipadx=5,side='left', anchor='n')
   def handle_mode_change(event):
      selected_option = selected_mode.get()
      if selected_option != "multiplayer":
         asWhite.config(text="WHITE")
         asBlack.config(text="BLACK")
         asWhite.config(state=tk.NORMAL)
         asBlack.config(state=tk.NORMAL)
      else:
         asWhite.config(text="player 1: WHITE")
         asBlack.config(text="player 2: BLACK")
         asWhite.config(state=tk.DISABLED)
         asBlack.config(state=tk.DISABLED)
   mode_combobox.bind("<<ComboboxSelected>>", handle_mode_change)

   timer_label = tk.Label(root, text="set Timer: -", font=("Arial", 16))
   timer_label.place(x=575, y=200)
   timer_values = {"No Timer":0,"Bullet: 2 min": 2*60, "Bullet: 3 min": 3*60,"Blitz: 5 min": 5*60, "Rapid: 10 min": 10*60, "Rapid: 15 min": 15*60, "Classical: 30 min": 30*60}
   timer_combobox = ttk.Combobox(root, values=list(timer_values.keys()), state='readonly')
   timer_combobox.place(x=575, y=230)
   timer_combobox.set("Bullet: 3 min")

   play = Button(root, text=" play Now ",background='light blue', command=loading_Screen, font=("Arial", 23))
   play.place(x=255, y=310,bordermode='inside', width=200)
   play = Button(root, text=" exit ",background='red', command=lambda: sys.exit(0), font=("Arial", 23))
   play.place(x=85, y=310,bordermode='inside', width=129)
   root.update()
   root.mainloop()

def loading_Screen():
   try:
      root.iconify()
      app = MainGame(root)
      app.main()
   except Exception as nofile:
      print("file not found at:-",nofile)

if __name__=="__main__":
   homeScreen()
