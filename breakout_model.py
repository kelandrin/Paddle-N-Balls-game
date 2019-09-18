import point

ORIGINAL_PADDLE_SIZE = .08
ORIGINAL_X_DELTA = .01
ORIGINAL_Y_DELTA = .02

class Ball:

    def __init__(self):

        self._center = point.from_frac(0,0)
        self._frac_radius = .015
        self._xdelta = ORIGINAL_X_DELTA
        self._ydelta = ORIGINAL_Y_DELTA

    def set_center(self, x: float, y: float):
        '''takes an x and y fractional coordinate and sets the center of the ball to those coordinates'''

        self._center = point.from_frac(x,y)

    def set_deltas(self, xdelta: float, ydelta: float):

        self._xdelta = xdelta
        self._ydelta = ydelta

    def corners(self) -> tuple:
        '''takes the center point and returns the top left and bottom right fractional coordinates for x and y'''

        frac_center_x, frac_center_y = self._center.as_frac()

        top_left_corner_x = frac_center_x - self._frac_radius
        top_left_corner_y = frac_center_y - self._frac_radius
        bottom_right_corner_x = frac_center_x + self._frac_radius
        bottom_right_corner_y = frac_center_y + self._frac_radius

        return (top_left_corner_x, top_left_corner_y, bottom_right_corner_x, bottom_right_corner_y)

    def move(self):

        current_x_center, current_y_center = self._center.as_frac()

        new_center_x = current_x_center + self._xdelta
        new_center_y = current_y_center + self._ydelta


        if new_center_x + self._frac_radius > 1.0:
            too_far_x = new_center_x + self._frac_radius - 1
            new_center_x = new_center_x - too_far_x
            self.bounce('x')

        if new_center_x - self._frac_radius < 0:
            too_far_x = -(new_center_x - self._frac_radius)
            new_center_x = new_center_x + too_far_x
            self.bounce('x')

        if new_center_y - self._frac_radius < 0:
            too_far_y = -(new_center_y - self._frac_radius)
            new_center_y = new_center_y + too_far_y
            self.bounce('y')


        self._center = point.from_frac(new_center_x,new_center_y)

    def bounce(self, bounce_direction: str):

        if bounce_direction == 'x':
            self._xdelta = -self._xdelta

        if bounce_direction == 'y':
            self._ydelta = -self._ydelta

    def _hit_floor(self) -> bool:

        current_x_center, current_y_center = self._center.as_frac()

        if current_y_center - (2 * self._frac_radius) > 1.0:
            return True


class Balls:

    def __init__(self):

        self.list = []
        self._num_balls = 0


    def _create_initial_ball(self) -> 'Ball':

        initial_ball = Ball()
        self._num_balls += 1

        return initial_ball


    def _add_ball_to_list(self, ball: 'Ball'):

        self.list.append(ball)

    def _start_game(self):

        initial_ball = self._create_initial_ball()
        self._add_ball_to_list(initial_ball)


    def _restart_game(self):

        initial_ball = self._create_initial_ball()
        self._add_ball_to_list(initial_ball)


    def _multi_ball_power_up(self, ball_that_hit_brick_center: 'Point'):

        x,y = ball_that_hit_brick_center.as_frac()

        while self._num_balls < 3:

            random_speed_multiplier = self.randomize_speed_multiplier()

            B = Ball()
            B.set_deltas(random_speed_multiplier * ORIGINAL_X_DELTA / 4, random_speed_multiplier * ORIGINAL_Y_DELTA / 4)
            B.set_center(x,y)
            self._num_balls += 1
            self.list.append(B)

            if self._check_for_same_deltas():
                self._delete_ball(B)


    def _check_for_same_deltas(self) -> bool:

        list_of_delta_tuple = []

        for ball in self.list:

            delta_tuple = (ball._xdelta, ball._ydelta)

            if delta_tuple in list_of_delta_tuple:

                return True

            else:

                list_of_delta_tuple.append(delta_tuple)

        if len(list_of_delta_tuple) == len(self.list):

            return False

    def randomize_speed_multiplier(self):

        import random

        while True:

            random_speed_multiplier = random.randint(-8, 8)
            if random_speed_multiplier != 0 and abs(random_speed_multiplier) > 1:

                return random_speed_multiplier


    def _delete_ball(self, ball: 'Ball'):

        self.list.remove(ball)
        self._num_balls -= 1




class Paddle:

    def __init__(self):

        self._width = ORIGINAL_PADDLE_SIZE
        self._height = .025
        self._topleft_corner = point.from_frac(0,0)
        self._bottomright_corner = point.from_frac(0,0)
        self._x_position= .5
        self._lengthened = False
        self._shortened = False


    def _position(self, frac_x_position: float):

        self._x_position = frac_x_position

    def corners(self) -> tuple:

        top_left_x, top_left_y = self._topleft_corner.as_frac()
        bottom_right_x, bottom_right_y = self._bottomright_corner.as_frac()

        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def move(self) -> tuple:

        new_top_left_x = self._x_position - (.5 * self._width)
        new_top_left_y = 1 - self._height
        new_bottom_right_x = self._x_position + (.5 * self._width)
        new_bottom_right_y = 1

        if new_top_left_x < 0:
            new_top_left_x = 0
            new_bottom_right_x = self._width

        if new_bottom_right_x > 1:
            new_bottom_right_x = 1
            new_top_left_x = 1 - self._width

        self._topleft_corner = point.from_frac(new_top_left_x, new_top_left_y)
        self._bottomright_corner = point.from_frac(new_bottom_right_x, new_bottom_right_y)

    def _lengthen_power_up(self):

        if self._shortened == True:
            self._width = ORIGINAL_PADDLE_SIZE
            self._shortened = False

        else:
            self._width = ORIGINAL_PADDLE_SIZE * 2
            self._lengthened = True


    def _shortened_power_up(self):

        if self._lengthened == True:
            self._width = ORIGINAL_PADDLE_SIZE
            self._lengthened = False

        else:
            self._width = ORIGINAL_PADDLE_SIZE / 2
            self._shortened = True

    def _original_size_paddle(self):

        self._width = ORIGINAL_PADDLE_SIZE
        self._shortened = False
        self._lengthened = False



class Brick:

    def __init__(self):

        self._topleft_corner = point.from_frac(0,0)
        self._bottomright_corner = point.from_frac(0,0)
        self._height = 0
        self._color = None
        self._hit_status = False
        self._lengthen_paddle_power_up = False
        self._shortened_paddle_power_up = False
        self._multi_ball_power_up = False

    def set_color(self, color:str):

        self._color = color

    def set_height(self, height: float):

        self._height = height

    def corners(self) -> tuple:

        top_left_x, top_left_y = self._topleft_corner.as_frac()
        bottom_right_x, bottom_right_y = self._bottomright_corner.as_frac()

        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def did_ball_bounce_off_top(self, ball: 'Ball', top_left_x: float, top_left_y: float, bottom_right_x: float, bottom_right_y: float) -> bool:

        current_x_center, current_y_center = ball._center.as_frac()

        if top_left_x <= current_x_center <= bottom_right_x \
                and top_left_y <= current_y_center + ball._frac_radius <= bottom_right_y:

            self._hit_status = True

            return True

    def did_ball_bounce_off_bottom(self, ball: 'Ball', top_left_x: float, top_left_y: float, bottom_right_x: float,
                                   bottom_right_y: float) -> bool:

        current_x_center, current_y_center = ball._center.as_frac()

        if top_left_x <= current_x_center <= bottom_right_x \
                and top_left_y <= current_y_center - ball._frac_radius <= bottom_right_y:

            self._hit_status = True

            return True

    def did_ball_bounce_off_left(self, ball: 'Ball', top_left_x: float, top_left_y: float, bottom_right_x: float, bottom_right_y: float) -> bool:

        current_x_center, current_y_center = ball._center.as_frac()

        if top_left_x <= current_x_center + ball._frac_radius <= bottom_right_x \
                and top_left_y <= current_y_center <= bottom_right_y:

            self._hit_status = True

            return True


    def did_ball_bounce_off_right(self, ball: 'Ball', top_left_x: float, top_left_y: float, bottom_right_x: float, bottom_right_y: float) -> bool:

        current_x_center, current_y_center = ball._center.as_frac()

        if top_left_x <= current_x_center - ball._frac_radius <= bottom_right_x \
                and top_left_y <= current_y_center <= bottom_right_y:

            self._hit_status = True

            return True


class Bricks:

    def __init__(self):

        self._list_of_colors = ['red','orange', 'yellow', 'green', '#10f2ea', 'blue', 'purple', 'pink', 'gray']
        self._num_rows = 9
        self._num_columns = 7
        self.list = self._create_list_of_bricks()


    def _create_list_of_bricks(self) -> list:

        import random

        top_gap = .05
        percentage_covered_by_bricks = .45
        list_of_bricks = []

        for row in range(self._num_rows):

            for col in range(self._num_columns):

                B = Brick()
                B.set_color(self._list_of_colors[row])
                B.set_height(percentage_covered_by_bricks/self._num_rows)

                top_left_x = col / self._num_columns
                top_left_y = top_gap + row * B._height
                bottom_right_x = (col + 1) / self._num_columns
                bottom_right_y = top_left_y + B._height

                B._topleft_corner = point.from_frac(top_left_x, top_left_y)
                B._bottomright_corner = point.from_frac(bottom_right_x, bottom_right_y)

                random_power_up_number = random.randint(1, 100)
                if 1 < random_power_up_number < 7:
                    B._lengthen_paddle_power_up = True

                if 7 < random_power_up_number < 14:
                    B._shortened_paddle_power_up = True

                if 14 < random_power_up_number < 20:
                    B._multi_ball_power_up = True

                list_of_bricks.append(B)

        return list_of_bricks

    def list_hit(self) -> list:

        list_of_bricks_hit = []

        for brick in self.list:

            if brick._hit_status == True:

                list_of_bricks_hit.append(brick)

        return list_of_bricks_hit

    def _delete_brick(self, brick: 'Brick'):

        self.list.remove(brick)


class BreakoutState:

    def __init__(self):

        self._balls = Balls()
        self._balls._start_game()

        self._paddle = Paddle()
        self._bricks = Bricks()

        self._lives = 3
        self._start = False
        self._pause = False
        self._gameover = False
        self._win = False

    def _initial_ball_center(self):

        for ball in self._balls.list:

            ball.set_center(self._paddle._x_position, 1 - self._paddle._height - ball._frac_radius)

    def _pause_ball_centers(self):

        for ball in self._balls.list:

            current_x_center, current_y_center = ball._center.as_frac()
            ball.set_center(current_x_center,current_y_center)


    def next_ball_frame(self):

        if self._start == True and self._pause == False:

            #if not self._did_win():

            for ball in self._balls.list:

                ball.move()

                if self._bounce_off_paddle():
                    ball.bounce('y')

                elif self._bounce_off_brick():

                    bricks_hit = self._bricks.list_hit()
                    for brick in bricks_hit:

                        if brick._lengthen_paddle_power_up == True and self._paddle._lengthened == False:

                            self._paddle._lengthen_power_up()

                        elif brick._shortened_paddle_power_up == True and self._paddle._shortened == False:

                            self._paddle._shortened_power_up()

                        elif brick._multi_ball_power_up == True and self._balls._num_balls < 3:

                            self._balls._multi_ball_power_up(ball._center)

                        self._bricks._delete_brick(brick)

                elif ball._hit_floor():

                    self._balls._delete_ball(ball)

                    if self._balls._num_balls == 0:

                        self._paddle._original_size_paddle()
                        self._subtract_life()

                        if self._lives > 0:
                            self._balls._restart_game()


                        else:
                            self._gameover = True

                    else:

                        continue

        elif self._start == True and self._pause == True:

            self._pause_ball_centers()



        elif self._start == False:

            self._initial_ball_center()






    def next_paddle_frame(self):

        self._paddle.move()


    def _bounce_off_paddle(self):

        for ball in self._balls.list:

            current_x_center, current_y_center = ball._center.as_frac()
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = self._paddle.corners()

            if 1 - self._paddle._height < current_y_center + ball._frac_radius \
                    and top_left_x < current_x_center < bottom_right_x:

                too_far_y = current_y_center + ball._frac_radius - (1 - self._paddle._height)
                current_y_center = current_y_center - too_far_y

                ball.set_center(current_x_center,current_y_center)

                return True


    def _bounce_off_brick(self):

        for ball in self._balls.list:

            for brick in self._bricks.list:

                current_x_center, current_y_center = ball._center.as_frac()
                top_left_x, top_left_y, bottom_right_x, bottom_right_y = brick.corners()

                if brick.did_ball_bounce_off_top(ball, top_left_x, top_left_y, bottom_right_x, bottom_right_y):

                    too_far_y = abs(current_y_center + ball._frac_radius - top_left_y)
                    current_y_center = current_y_center - too_far_y

                    ball.set_center(current_x_center, current_y_center)
                    ball.bounce('y')

                    return True

                elif brick.did_ball_bounce_off_bottom(ball, top_left_x, top_left_y, bottom_right_x, bottom_right_y):

                    too_far_y = abs(current_y_center - ball._frac_radius - bottom_right_y)
                    current_y_center = current_y_center + too_far_y

                    ball.set_center(current_x_center, current_y_center)
                    ball.bounce('y')
                    return True

                elif brick.did_ball_bounce_off_left(ball, top_left_x, top_left_y, bottom_right_x, bottom_right_y):

                    too_far_x = abs(current_x_center + ball._frac_radius - top_left_x)
                    current_x_center = current_x_center - too_far_x

                    ball.set_center(current_x_center, current_y_center)
                    ball.bounce('x')
                    return True

                elif brick.did_ball_bounce_off_right(ball, top_left_x, top_left_y, bottom_right_x, bottom_right_y):

                    too_far_x = abs(current_x_center - ball._frac_radius - bottom_right_x)
                    current_x_center = current_x_center + too_far_x

                    ball.set_center(current_x_center, current_y_center)
                    ball.bounce('x')
                    return True

    def _subtract_life(self):

        if len(self._balls.list) == 0:

            self._lives -= 1
            self._start = False

    def _did_win(self) -> bool:

        if len(self._bricks.list) == 0:

            self._win = True
            self._gameover = True

            return True




































'''multi balls, longer paddle, scoreboard with lives, settings menu in the beginning with easy medium and hard,
 choice of how many bricks'''



