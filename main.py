import arcade
import math
import random

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite by Angle Example"

MOVEMENT_SPEED = 5
ANGLE_SPEED = 5


class Player(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)


        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # -- Set up the walls

        # Create horizontal rows of boxes
        for x in range(32, SCREEN_WIDTH, 64):
            # Bottom edge
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

            # Top edge
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT - 32
            self.wall_list.append(wall)

        # Create vertical columns of boxes
        for y in range(96, SCREEN_HEIGHT, 64):
            # Left
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.center_x = 32
            wall.center_y = y
            self.wall_list.append(wall)

            # Right
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.center_x = SCREEN_WIDTH - 32
            wall.center_y = y
            self.wall_list.append(wall)

        # Create boxes in the middle
        for x in range(128, SCREEN_WIDTH, 196):
            for y in range(128, SCREEN_HEIGHT, 196):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                # wall.angle = 45
                self.wall_list.append(wall)

        # Create coins
        for i in range(10):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.25)
            coin.center_x = random.randrange(100, 700)
            coin.center_y = random.randrange(100, 500)
            while coin.change_x == 0 and coin.change_y == 0:
                coin.change_x = random.randrange(-4, 5)
                coin.change_y = random.randrange(-4, 5)

            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set up the player
        self.player_sprite = Player(":resources:images/space_shooter/playerShip1_green.png",
                                    SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        for coin in self.coin_list:

            coin.center_x += coin.change_x
            walls_hit = arcade.check_for_collision_with_list(coin, self.wall_list)
            for wall in walls_hit:
                if coin.change_x > 0:
                    coin.right = wall.left
                elif coin.change_x < 0:
                    coin.left = wall.right
            if len(walls_hit) > 0:
                coin.change_x *= -1

            coin.center_y += coin.change_y
            walls_hit = arcade.check_for_collision_with_list(coin, self.wall_list)
            for wall in walls_hit:
                if coin.change_y > 0:
                    coin.top = wall.bottom
                elif coin.change_y < 0:
                    coin.bottom = wall.top
            if len(walls_hit) > 0:
                coin.change_y *= -1

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Forward/back
        if key == arcade.key.UP:
            self.player_sprite.speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.speed = -MOVEMENT_SPEED

        # Rotate left/right
        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()