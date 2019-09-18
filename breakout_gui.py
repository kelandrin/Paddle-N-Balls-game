from tkinter import *
import breakout_model

class BreakoutApplication:

    def __init__(self):

        self._root_window = Tk()
        self._root_window.wm_title('BREAKOUT')
        self._root_window.after(40, self._next_frame)

        '''GAMESTATE'''

        self._gamestate = breakout_model.BreakoutState()

        '''CANVAS'''

        self._canvas = Canvas(master=self._root_window,
                              width=700, height=700,
                              background= 'black')
        self._canvas.grid(row = 2, column = 0, sticky = N + E + W + S)


        '''BINDS'''

        self._canvas.bind('<Configure>', self._on_canvas_resize)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Motion>', self._on_mouse_move)
        self._canvas.bind('<Enter>', self._on_mouse_enter)
        self._canvas.bind('<Leave>', self._on_mouse_leave)
        self._canvas.bind('<Button-2>', self._on_continue_clicked)
        self._canvas.bind_all('<Key>', self._on_spacebar_press)


        '''ROW AND COLUMN CONFIGURES'''

        self._root_window.columnconfigure(0, weight=1)
        self._root_window.rowconfigure(0, weight=0)
        self._root_window.rowconfigure(1, weight=0)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.rowconfigure(3, weight=0)

        self._make_display_buttons()

    def _make_display_buttons(self):
        self._make_scoreboard()
        self._make_title_label()

    def _make_title_label(self):
        '''creates the title label at the top of the screen'''

        self._title_label = Label(master=self._root_window, text='BREAKOUT',
                                  font=('Times New Roman', 30), bg='#10f2ea', fg='black', width=75, relief='raised')
        self._title_label.grid(row=0, column=0, sticky=N + E + W + S)

    def _make_scoreboard(self):
        '''creates the number of lives label as well as the number of remaining bricks'''

        '''LIVES LABEL'''
        self._lives_label = Label(master= self._root_window, text='Lives: 0',
                                               font=(None, 28), relief='raised')
        self._lives_label.grid(row=1, column=0, sticky= W)

        '''NUM BRICKS LABEL'''
        self._num_bricks_label = Label(master=self._root_window, text='Remaining Bricks: 0',
                                               font=(None, 28), relief='raised')
        self._num_bricks_label.grid(row=1, column=0, sticky= E)

    def _update_scoreboard(self):
        '''updates what the score is on the board'''

        lives = self._gamestate._lives
        bricks_left = len(self._gamestate._bricks.list)

        self._lives_label['text'] = f'Lives: {lives}'
        self._num_bricks_label['text'] = f'Remaining Bricks: {bricks_left}'

    def _make_game_over_label(self):

        self._game_over_label = Label(master=self._end_screen_frame,
                                      text=f'GAME OVER!',font=('Times New Roman', 50), bg='#10f2ea', width=50, height = 5)
        self._game_over_label.grid(row = 0, column = 0, sticky = N + E + W + S)

    def _make_play_again_button(self):

        self._play_again_button = Button(master=self._end_screen_frame,
                                         text=f'Play Again', font=('Times New Roman', 20), bg='#10f2ea', width=20,
                                         pady=30,
                                         command=self._on_continue_clicked)
        self._play_again_button.grid(row=4, column=0, sticky=N + E + W + S)

    def _make_win_label(self):

        self._game_over_label = Label(master=self._end_screen_frame,
                                      text=f'YOU WIN!', font=('Times New Roman', 50), bg='#10f2ea', width=50,
                                      height=5)
        self._game_over_label.grid(row=0, column=0, sticky=N + E + W + S)



    def _make_end_screen(self):

        self._end_screen_frame = Frame(master = self._root_window)
        self._end_screen_frame.grid(row = 2, column = 0)
        self._end_screen_frame.focus_set()
        self._make_play_again_button()
        self._gamestate.start = False

        if self._gamestate._win == True:

            self._make_win_label()

        else:

            self._make_game_over_label()


    def _destroy_endscreen(self):

        self._end_screen_frame.destroy()
        self._play_again_button.destroy()
        self._game_over_label.destroy()



    def _draw_ball(self, ball: 'Ball'):

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y = ball.corners()

        self._canvas.create_oval(
            canvas_width * top_left_corner_x, canvas_height * top_left_corner_y,
            canvas_width * bottom_right_corner_x, canvas_height * bottom_right_corner_y,
            fill='red', outline='Gray')

    def _draw_paddle(self):

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y = self._gamestate._paddle.corners()

        self._canvas.create_rectangle(
            canvas_width * top_left_corner_x, canvas_height * top_left_corner_y,
            canvas_width * bottom_right_corner_x, canvas_height * bottom_right_corner_y,
            fill='#10f2ea', outline='White')

    def _draw_brick(self, brick: 'Brick'):

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y = brick.corners()

        self._canvas.create_rectangle(
            canvas_width * top_left_corner_x, canvas_height * top_left_corner_y,
            canvas_width * bottom_right_corner_x, canvas_height * bottom_right_corner_y,
            fill= brick._color, outline='White')

        if brick._lengthen_paddle_power_up == True:

            top_left_x = (canvas_width * top_left_corner_x) + (.1 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            top_left_y = (canvas_height * top_left_corner_y) + (.40 * canvas_height * (bottom_right_corner_y - top_left_corner_y))
            bottom_right_x = (canvas_width * bottom_right_corner_x) - (.1 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            bottom_right_y = (canvas_height * bottom_right_corner_y) - (.40 * canvas_height *(bottom_right_corner_y - top_left_corner_y))

            self._canvas.create_rectangle(
                top_left_x,top_left_y,bottom_right_x,bottom_right_y,
                fill='black', outline='White')


        if brick._shortened_paddle_power_up == True:

            top_left_x = (canvas_width * top_left_corner_x) + (.4 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            top_left_y = (canvas_height * top_left_corner_y) + (.4 * canvas_height * (bottom_right_corner_y - top_left_corner_y))
            bottom_right_x = (canvas_width * bottom_right_corner_x) - (.4 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            bottom_right_y = (canvas_height * bottom_right_corner_y) - (.4 * canvas_height * (bottom_right_corner_y - top_left_corner_y))

            self._canvas.create_rectangle(
                top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                fill='black', outline='White')

        if brick._multi_ball_power_up == True:

            first_top_left_x = (canvas_width * top_left_corner_x) + (.35 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            first_top_left_y = (canvas_height * top_left_corner_y) + (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))
            first_bottom_right_x = (canvas_width * bottom_right_corner_x) - (.55 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            first_bottom_right_y = (canvas_height * bottom_right_corner_y) - (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))

            second_top_left_x = (canvas_width * top_left_corner_x) + (.45 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            second_top_left_y = (canvas_height * top_left_corner_y) + (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))
            second_bottom_right_x = (canvas_width * bottom_right_corner_x) - (.45 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            second_bottom_right_y = (canvas_height * bottom_right_corner_y) - (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))

            third_top_left_x = (canvas_width * top_left_corner_x) + (.55 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            third_top_left_y = (canvas_height * top_left_corner_y) + (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))
            third_bottom_right_x = (canvas_width * bottom_right_corner_x) - (.35 * canvas_width * (bottom_right_corner_x - top_left_corner_x))
            third_bottom_right_y = (canvas_height * bottom_right_corner_y) - (.25 * canvas_height * (bottom_right_corner_y - top_left_corner_y))

            self._canvas.create_oval(
                first_top_left_x, first_top_left_y, first_bottom_right_x, first_bottom_right_y,
                fill='black', outline='White')

            self._canvas.create_oval(
                second_top_left_x, second_top_left_y, second_bottom_right_x, second_bottom_right_y,
                fill='black', outline='White')

            self._canvas.create_oval(
                third_top_left_x, third_top_left_y, third_bottom_right_x, third_bottom_right_y,
                fill='black', outline='White')





    def _draw_all_bricks(self):

        for brick in self._gamestate._bricks.list:

            self._draw_brick(brick)

    def _draw_all_balls(self):

        for ball in self._gamestate._balls.list:

            self._draw_ball(ball)


    def _draw_frame(self):

        self._canvas.delete(ALL)
        self._draw_paddle()
        self._draw_all_balls()
        self._draw_all_bricks()
        self._update_scoreboard()

        if self._gamestate._gameover == True:
            self._make_end_screen()


    def _next_frame(self):

        self._gamestate.next_ball_frame()
        self._gamestate.next_paddle_frame()
        self._draw_frame()
        self._root_window.after(40, self._next_frame)


    def _on_canvas_resize(self, event: Event):

        self._make_display_buttons()
        self._draw_frame()

    def _on_canvas_clicked(self, event: Event):

        if self._gamestate._gameover == False:

            self._gamestate._start = True

    def _on_continue_clicked(self, event: Event):
        print('click')

        self._gamestate._lives = 3
        self._gamestate._gameover = False
        self._destroy_endscreen()

    def _on_spacebar_press(self, event: Event):

        if event.keysym == 'space':

            self._gamestate._pause = True




        #pause the game, bring up a menu to continue, or save game, if save game is clicked then display a saved note and
        # an exit button which closes the game or continue lets you keep playing

    def _on_mouse_move(self, event: Event):

        canvas_width = self._canvas.winfo_width()

        self._paddle_position = event.x / canvas_width
        self._gamestate._paddle._position(self._paddle_position)

    def _on_mouse_leave(self, event: Event):
        print('i just left')
        self._gamestate._pause = True


    def _on_mouse_enter(self, event: Event):
        print('i just entered')
        self._gamestate._pause = False



    def run(self) -> None:
        '''runs the mainloop'''

        self._root_window.mainloop()



if __name__ == '__main__':
    GameAPP = BreakoutApplication().run()
















'''self._make_menu_settings_button = Button(master=self._root_window, text='CLICK TO START',
                                               font=('Times New Roman', 30), anchor='center',
                                               padx=7, pady=7, command=self._on_settings_button_clicked)

      self._make_menu_settings_button.grid(row=2, column=0)'''