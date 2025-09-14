import turtle as t
import random


class SnakeGame:
    def __init__(self):
        self.boundary = 600
        self.s = 0
        self.hs = self.load_high_score()
        self.snake = []
        self.direction = "stop"
        self.screen = self.screen_setup()

    def create_turtle(self, shape, color):
        obj = t.Turtle()
        obj.shape(shape)
        obj.color(color)
        obj.penup()
        return obj

    def screen_setup(self):
        screen = t.Screen()
        screen.setup(self.boundary, self.boundary)
        screen.bgcolor('black')
        screen.title('Snake Game')
        screen.tracer(0)
        return screen

    def create_snake(self):
        self.snake.append(self.create_turtle('square', 'green'))

    def right(self):
        if self.direction != "left":
            self.direction = "right"
            print('Right key pressed')

    def left(self):
        if self.direction != "right":
            self.direction = 'left'
            print('Left key pressed')

    def up(self):
        if self.direction != "down":
            self.direction = 'up'
            print('Up key pressed')

    def down(self):
        if self.direction != "up":
            self.direction = 'down'
            print('Down key pressed')

    def moving_snake(self):

        # screen = self.screen_setup() # Setting the screen obj

        self.screen.onkey(self.right, "Right")  # maping to the key press
        self.screen.onkey(self.up, "Up")  # maping to the key press
        self.screen.onkey(self.down, "Down")
        self.screen.onkey(self.left, "Left")
        self.screen.listen()  # to catch the events

    def continous_movement(self):

        def move():
            snake_head = self.snake[0]
            snake_head.penup()
            if self.direction == 'right':
                snake_head.setheading(0)
            elif self.direction == 'left':
                snake_head.setheading(180)
            elif self.direction == 'up':
                snake_head.setheading(90)
            elif self.direction == 'down':
                snake_head.setheading(270)

            for i in range(len(self.snake)-1, 0, -1):
                segment_x = self.snake[i-1].xcor()
                segment_y = self.snake[i-1].ycor()

                self.snake[i].setposition((segment_x, segment_y))

            if self.direction != 'stop':
                self.snake[0].fd(20)

            # screen = self.screen_setup()
            self.screen.update()
            self.screen.ontimer(move, 150)

        move()

    def add_segment(self):
        segment = self.create_turtle('square', 'yellow')
        segment.penup()
        self.snake.append(segment)

    def food(self):
        food = self.create_turtle('circle', 'red')
        food_x = random.randint(1, 300)
        food_y = random.randint(1, 300)
        food.goto(food_x, food_y)

        def eating_food():
            snake_head = self.snake[0]
            if snake_head.distance(food) < 20:
                food.goto(random.randint(-270, 270), random.randint(-270, 270))
                self.add_segment()
                self.s = self.s+1
                if self.s > int(self.hs):
                    self.store_high_score(self.s)
            # screen = self.screen_setup()
            self.screen.ontimer(eating_food, 100)
            # p.write(f"Score : {s}  High Score : {hs}", align="center", font
            # =("candara", 24, "bold"))

        eating_food()

    def collision(self):
        def check_collision():
            # snake head touching any body part will end the Game
            # screen = self.screen_setup()
            for segment in self.snake[1:]:
                if self.snake[0].distance(segment) < 10:
                    self.s = 0
                    # hs = 0

                    self.screen.bye()
            # snake head touching the boundary will also end the Game
                elif (self.snake[0].xcor() > 290
                      or self.snake[0].xcor() < -290
                      or self.snake[0].ycor() > 290
                      or self.snake[0].ycor() < -290):
                    # global s
                    # global hs
                    self.s = 0
                    # hs = 0
                    # screen = self.screen_setup()
                    self.screen.bye()

            self.screen.ontimer(check_collision, 20)
        check_collision()

    def score_display(self):
        # score display
        p = self.create_turtle('square', 'white')
        p.speed(0)
        p.penup()
        p.hideturtle()
        p.goto(0, 250)
        p.write("Score : 0  High Score : 0", align="center", font=("c\
andara", 24, "bold"))
        # screen = self.screen_setup()

        def show_score():
            # p.write(f"Score : {s}  High Score : {hs}", align="center",
            # font=("candara", 24, "bold"))
            if self.s > int(self.hs):
                self.hs = self.s
                p.clear()
                p.write(f"Score : {self.s}  High Score : {self.s}", align="cen\
ter", font=("candara", 24, "bold"))
            else:
                p.clear()
                p.write(f"Score : {self.s}  High Sc\
ore : {self.hs}", align="cen\
ter", font=("candara", 24, "bold"))
            self.screen.ontimer(show_score, 200)
        show_score()

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                score = f.read()
                return score
        except Exception as e:
            print(f"Error occured: {e}")
            return 0

    def store_high_score(self, hs):
        try:
            with open('high_score.txt', 'w') as f:
                high_score = f.write(str(hs))
                return high_score
        except Exception as e:
            print(f"Error occured: {e}")


def main():
    try:
        obj = SnakeGame()
        obj.create_snake()
        obj.moving_snake()
        obj.continous_movement()
        obj.food()
        obj.collision()
        obj.score_display()
        t.mainloop()  # 👈 Add this here to keep screen alive
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
