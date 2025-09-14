import turtle as t
import random


class Snake:
    def __init__(self, create_turtle_func):
        self.snake = []
        self.create_turtle = create_turtle_func
        self.create_initial_snake()
        self.direction = "stop"

    def create_initial_snake(self):
        segment = self.create_turtle('square', 'green')
        self.snake.append(segment)

    def collides_with_self(self):
        head = self.snake[0]
        for segment in self.snake[1:]:
            if head.distance(segment) < 10:
                return True
        return False

    def move(self):
        if self.direction == 'stop':
            return

        for i in range(len(self.snake)-1, 0, -1):
            seg_x = self.snake[i-1].xcor()
            seg_y = self.snake[i-1].ycor()
            self.snake[i].goto(seg_x, seg_y)

        head = self.snake[0]
        if self.direction == 'right':
            head.setheading(0)
        elif self.direction == 'left':
            head.setheading(180)
        elif self.direction == 'up':
            head.setheading(90)
        elif self.direction == 'down':
            head.setheading(270)
        head.forward(20)

    def grow(self):
        last_segment = self.snake[-1]
        x, y = last_segment.position()
        segment = self.create_turtle('square', 'yellow')
        segment.goto(x, y)
        self.snake.append(segment)

    def set_direction(self, direction):
        opposite = {'up': 'down', 'down': 'up', 'left': 'right',
                    'right': 'left'}
        # Prevent snake from moving in the opposite direction directly
        if self.direction != opposite.get(direction):
            self.direction = direction

    def collide(self):
        head = self.snake[0]
        for segment in self.snake[1:]:
            if head.distance(segment) < 20:
                return True
        return False

    def get_head_position(self):
        return self.segments[0].position()


class Food:
    def __init__(self, create_turtle_func, boundary):
        self.create_turtle = create_turtle_func
        self.food = self.create_turtle('circle', 'red')
        self.boundary = boundary
        self.place_food()

    def place_food(self):
        x = random.randint(-self.boundary // 2 + 20, self.boundary // 2 - 20)
        y = random.randint(-self.boundary // 2 + 20, self.boundary // 2 - 20)
        self.food.goto(x, y)

    def refresh(self):
        self.place_food()

    def get_position(self):
        return self.food.position()


class SnakeGame:
    def __init__(self, boundary=600):
        self.boundary = boundary
        self.screen = self.setup_screen()
        self.score = 0
        self.high_score = self.load_high_score()
        self.snake = Snake(self.create_turtle)
        self.food = Food(self.create_turtle, self.boundary)
        self.setup_controls()
        self.score_pen = self.create_score_pen()
        self.running = True
        self.d = 0.2

    def create_turtle(self, shape, color):
        obj = t.Turtle()
        obj.shape(shape)
        obj.color(color)
        obj.penup()
        return obj

    def setup_screen(self):
        screen = t.Screen()
        screen.setup(self.boundary, self.boundary)
        screen.bgcolor('black')
        screen.title('Snake Game')
        screen.tracer(0)
        return screen

    def create_score_pen(self):
        pen = self.create_turtle('square', 'white')
        pen.hideturtle()
        pen.goto(0, self.boundary//2 - 40)
        pen.write(f"Score: {self.score}  High Sc\
ore: {self.high_score}", align="center", font=("Arial", 24, "normal"))
        return pen

    def update_score(self):
        self.score_pen.clear()
        self.score_pen.write(f"Sco\
re: {self.score}  High Score: {self.high_score}", align="center", font=("Ari\
al", 24, "normal"))

    def setup_controls(self):
        self.screen.listen()
        self.screen.onkey(lambda: self.change_direction("up"), "Up")
        self.screen.onkey(lambda: self.change_direction("down"), "Down")
        self.screen.onkey(lambda: self.change_direction("left"), "Left")
        self.screen.onkey(lambda: self.change_direction("right"), "Right")

    def change_direction(self, direction):
        # Prevent reversing direction
        opposites = {"up": "down", "down": "up", "left": "right",
                     "right": "left"}
        if self.snake.direction != opposites.get(direction):
            self.snake.direction = direction

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except Exception as e:
            print(e)
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    def check_collisions(self):
        head = self.snake.snake[0]
        x, y = head.xcor(), head.ycor()

        # Check wall collision
        if (
            x > self.boundary/2 - 10
            or x < -self.boundary/2 + 10
            or y > self.boundary/2 - 10
            or y < -self.boundary/2 + 10
        ):

            self.game_over()

        # Check self collision
        if self.snake.collides_with_self():
            self.game_over()

        if head.distance(self.food.food) < 20:
            self.food.refresh()
            self.snake.grow()
            self.d -= 0.01
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.update_score()

    def game_over(self):
        self.running = False
        self.screen.clear()
        self.screen.bgcolor('black')
        self.screen.title('Game Over')
        pen = self.create_turtle('square', 'white')
        pen.hideturtle()
        pen.write(f"Game Over! Final Score: {self.score}", align="cent\
er", font=("Arial", 30, "normal"))

    def game_loop(self):
        if self.running:
            self.snake.move()
            self.check_collisions()
            self.screen.update()
            self.screen.ontimer(self.game_loop, int(self.d * 1000))

    def run(self):
        self.game_loop()
        self.screen.mainloop()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
