import arcade
import os
import pickle
import numpy as np

from game_data import GameData

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "Monster Hunter"
SCREEN_BORDER_PADDING = 20

MOVEMENT_SPEED = 5
MONSTER_SPEED = 2
FIRE_RATE = 0.15

FILE_PATH = r'C:\Users\jpdodson\Box Sync\Programming\Python\Gaming\MonsterHunter'
SPRITES_PATH =r'C:\Users\jpdodson\Box Sync\Programming\Python\Gaming\MonsterHunter\Sprites'

START_SCENE_INDEX = 0
GAME_RUNNING_SCENE_INDEX = 1
WIN_SCENE_INDEX = 2
LOSE_SCENE_INDEX = 3


class Player(arcade.Sprite):

    def __init__(self, file_name, scale):
        super().__init__(file_name, scale)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class Monster(arcade.Sprite):

    def __init__(self, file_name, scale):
        super().__init__(file_name, scale)

        self.speed = MONSTER_SPEED

    def update(self):
        pass

    def move(self, player_x, player_y):
        dx = player_x - self.center_x
        dy = player_y - self.center_y

        self.center_x += dx/(np.sqrt(dx**2 + dy**2))*self.speed
        self.center_y += dy/(np.sqrt(dx**2 + dy**2))*self.speed


class MyGame(arcade.Window):

    def __init__(self, width, height, name):
        super().__init__(width, height, name)

        # self.file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(self.file_path)

        arcade.set_background_color(arcade.color.AMAZON)

        self.initialize_vars()
        self.make_sprites()
        self.setup_UI()

    def initialize_vars(self):
        self.level_timer = 0
        self.score = 0
        self.monsters_killed = 0
        self.time_since_bullet_fired = 0
        self.current_direction = 'right'
        self.win_game_bool = False
        self.current_scene = START_SCENE_INDEX
        self.game_loaded = False
        self.life_gained_arr = [(i+1)*i*5000 for i in range(99)]
        self.life_gained_index = 0
        self.difficulty_arr = [i*100 for i in range(100)]
        self.game_completed = False

        self.keyup_pressed = False
        self.keydown_pressed = False
        self.keyright_pressed = False
        self.keyleft_pressed = False
        self.keyspace_pressed = False

    def make_sprites(self):

        self.monsters_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()
        self.fading_heart_list = arcade.SpriteList()

        self.player = Player(os.path.join(SPRITES_PATH, 'player.png'), 0.25)
        self.player.center_x = SCREEN_WIDTH/2
        self.player.center_y = SCREEN_HEIGHT/2

        self.heart_sprite_list = arcade.SpriteList()
        for i in range(3):
            heart = arcade.Sprite(os.path.join(SPRITES_PATH, 'heart.png'), 0.3)
            heart.center_x = (SCREEN_BORDER_PADDING + (heart.width + 5)*len(self.heart_sprite_list))
            heart.center_y = SCREEN_HEIGHT - SCREEN_BORDER_PADDING
            self.heart_sprite_list.append(heart)

    def setup_UI(self):
        self.score_text = None

    def update(self, dt):

        # Only update if in game scene
        if self.current_scene == GAME_RUNNING_SCENE_INDEX:
            self.game_update(dt)

    def on_draw(self):
        arcade.start_render()

        if self.current_scene == START_SCENE_INDEX:
            self.draw_start_scene()
        elif self.current_scene == GAME_RUNNING_SCENE_INDEX:
            self.draw_game()
        elif (self.current_scene == WIN_SCENE_INDEX) or (self.current_scene == LOSE_SCENE_INDEX):
            self.complete_level()

    def game_update(self, dt):
        # Update sprites
        self.player.update()
        self.monsters_sprite_list.update()
        for monster in self.monsters_sprite_list:
            monster.update()
            monster.move(self.player.center_x, self.player.center_y)
        for bullet in self.bullet_sprite_list:
            bullet.update()
        for heart in self.heart_sprite_list:
            heart.update()

        # Monster spawning logic
        difficulty_index = 0
        for i in range(len(self.difficulty_arr)):
            if int(self.level_timer * 60) > self.difficulty_arr[i]:
                difficulty_index = i
            else:
                break

        if (int(self.level_timer * 60 % (100 - difficulty_index)) == 0):
            multi_spawning = int(np.round(difficulty_index / 20))
            for i in range(multi_spawning + 1):
                # Make monster
                monster = Monster(os.path.join(SPRITES_PATH, 'monster.png'), 0.15)
                monster.center_x = np.random.randint(0, SCREEN_WIDTH)
                monster.center_y = np.random.randint(0, SCREEN_HEIGHT)

                # Make red monsters
                red_monster_index = np.random.randint(100 - difficulty_index)
                if red_monster_index < 10:
                    monster_speed = MONSTER_SPEED * 2
                    monster.speed = monster_speed
                    monster.color = (255, 0, 0)

                # Handle monsters accidentally spawning on player
                monster_player_dist = ((self.player.center_x - monster.center_x)**2 +
                                       (self.player.center_y - monster.center_y)**2)**(1/2)
                monster_player_widths = ((self.player.width + monster.width)**2 +
                                         (self.player.width - monster.width)**2)**(1/2)
                if monster_player_dist < 4*monster_player_widths:
                    rand_int = np.random.randint(0, 3)
                    if rand_int == 0:
                        monster.center_x -= 2*monster_player_widths
                    elif rand_int == 1:
                        monster.center_x += 2*monster_player_widths
                    elif rand_int == 2:
                        monster.center_y -= 2*monster_player_widths
                    elif rand_int == 3:
                        monster.center_y += 2*monster_player_widths

                self.monsters_sprite_list.append(monster)

        # Check for bullet collision with monster
        for bullet in self.bullet_sprite_list:
            monster_hit_list = arcade.check_for_collision_with_list(bullet, self.monsters_sprite_list)
            for monster in monster_hit_list:
                monster.remove_from_sprite_lists()
                self.monsters_killed += 1
                self.score += 1000

        # Check for monster collision with player
        monster_hit_list = arcade.check_for_collision_with_list(self.player, self.monsters_sprite_list)
        if len(monster_hit_list) > 0:
            if len(self.heart_sprite_list) - 1 <= 0:
                self.win_game_bool = False
                self.complete_level()
            else:
                for monster in monster_hit_list:
                    monster.remove_from_sprite_lists()
                    self.heart_sprite_list.pop(-1)

        # Clean up bullet sprites
        for bullet in self.bullet_sprite_list:
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

        # Add life for score milestones
        if self.score > self.life_gained_arr[self.life_gained_index + 1]:
            # Handle hearts and lives
            heart = arcade.Sprite(os.path.join(SPRITES_PATH, 'heart.png'), 0.3)
            heart.center_x = (SCREEN_BORDER_PADDING + (heart.width + 5)*len(self.heart_sprite_list))
            heart.center_y = SCREEN_HEIGHT - SCREEN_BORDER_PADDING
            self.heart_sprite_list.append(heart)
            self.life_gained_index += 1

            # Fading heart
            heart = arcade.Sprite(os.path.join(SPRITES_PATH, 'heart.png'), 1.0)
            heart.center_x = SCREEN_WIDTH / 2
            heart.center_y = SCREEN_HEIGHT * 3/4
            self.fading_heart_list.append(heart)

        # Routine for fading hearts
        for heart in self.fading_heart_list:
            alpha = heart.alpha
            alpha -= 10
            if alpha <= 0:
                heart.remove_from_sprite_lists()
            else:
                heart.color = (255, 255, 255, alpha)
                heart.center_y += 5

        # Routine for holding spacebar to shoot
        if self.keyspace_pressed and self.time_since_bullet_fired > FIRE_RATE:
            self.time_since_bullet_fired = 0
            self.fire_bullet()

        # Update UI
        self.level_timer += dt
        self.score += dt * 60
        self.time_since_bullet_fired += dt

    def draw_game(self):
        # Draw UI
        self.scoretext_str = 'Score: ' + str(int(np.floor(self.score)))
        self.scoretext = arcade.draw_text(self.scoretext_str, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 30,
                                          arcade.color.WHITE,
                                          align="left", anchor_x="right", bold=True, font_size=16)

        # Draw Sprites
        self.player.draw()
        for monster in self.monsters_sprite_list:
            monster.draw()
        for bullet in self.bullet_sprite_list:
            bullet.draw()
        for heart in self.heart_sprite_list:
            heart.draw()
        for fading_heart in self.fading_heart_list:
            fading_heart.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Movement
        if self.current_scene == GAME_RUNNING_SCENE_INDEX:
            if key == arcade.key.UP:
                self.player.change_y = MOVEMENT_SPEED
                self.current_direction = 'up'
                self.keyup_pressed = True
            elif key == arcade.key.DOWN:
                self.player.change_y = -MOVEMENT_SPEED
                self.current_direction = 'down'
                self.keydown_pressed = True
            elif key == arcade.key.LEFT:
                self.current_direction = 'left'
                self.player.change_x = -MOVEMENT_SPEED
                self.keyleft_pressed = True
            elif key == arcade.key.RIGHT:
                self.current_direction = 'right'
                self.player.change_x = MOVEMENT_SPEED
                self.keyright_pressed = True

        # Shooting
        if key == arcade.key.SPACE:
            if self.current_scene == START_SCENE_INDEX:
                self.current_scene = GAME_RUNNING_SCENE_INDEX
            elif self.current_scene == LOSE_SCENE_INDEX:
                self.restart_game()
            elif (self.current_scene == GAME_RUNNING_SCENE_INDEX) and (self.time_since_bullet_fired > 0.15):
                self.keyspace_pressed = True
                self.time_since_bullet_fired = 0
                self.fire_bullet()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if self.current_scene == GAME_RUNNING_SCENE_INDEX:
            if key == arcade.key.UP:
                self.player.change_y = 0
                self.keyup_pressed = False
            elif key == arcade.key.DOWN:
                self.player.change_y = 0
                self.keydown_pressed = False
            elif key == arcade.key.LEFT:
                self.player.change_x = 0
                self.keyleft_pressed = False
            elif key == arcade.key.RIGHT:
                self.player.change_x = 0
                self.keyright_pressed = False
            elif key == arcade.key.SPACE:
                self.keyspace_pressed = False

            # Extra logic for holding down keys
            if self.keyup_pressed:
                self.player.change_y = MOVEMENT_SPEED
            if self.keydown_pressed:
                self.player.change_y = -MOVEMENT_SPEED
            if self.keyleft_pressed:
                self.player.change_x = -MOVEMENT_SPEED
            if self.keyright_pressed:
                self.player.change_x = MOVEMENT_SPEED
            if (self.keyspace_pressed) and (self.time_since_bullet_fired > FIRE_RATE):
                self.time_since_bullet_fired = 0
                self.fire_bullet()

    def fire_bullet(self):
        bullet = arcade.Sprite(os.path.join(SPRITES_PATH, 'bullet.png'), 0.05)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y

        if self.keyup_pressed and self.keyright_pressed:
            bullet.change_x = 10
            bullet.change_y = 10
        elif self.keyup_pressed and self.keyleft_pressed:
            bullet.change_x = -10
            bullet.change_y = 10
        elif self.keydown_pressed and self.keyright_pressed:
            bullet.change_x = 10
            bullet.change_y = -10
        elif self.keydown_pressed and self.keyleft_pressed:
            bullet.change_x = -10
            bullet.change_y = -10
        elif self.keyup_pressed:
            bullet.change_x = 0
            bullet.change_y = 10
        elif self.keydown_pressed:
            bullet.change_x = 0
            bullet.change_y = -10
        elif self.keyright_pressed:
            bullet.change_x = 10
            bullet.change_y = 0
        elif self.keyleft_pressed:
            bullet.change_x = -10
            bullet.change_y = 0
        elif self.current_direction == 'up':
            bullet.change_x = 0
            bullet.change_y = 10
        elif self.current_direction == 'down':
            bullet.change_x = 0
            bullet.change_y = -10
        elif self.current_direction == 'right':
            bullet.change_x = 10
            bullet.change_y = 0
        elif self.current_direction == 'left':
            bullet.change_x = -10
            bullet.change_y = 0

        self.bullet_sprite_list.append(bullet)

    def complete_level(self):
        if self.game_completed is False:
            highscore = GameData.get_key_value('highscore')
            if self.score > highscore:
                GameData.set_key_value('highscore', int(np.floor(self.score)))
                GameData.save_data()
            self.game_completed = True

        if self.win_game_bool:
            self.current_scene = WIN_SCENE_INDEX
            self.draw_win_scene()
        else:
            self.current_scene = LOSE_SCENE_INDEX
            self.draw_lose_scene()

    def draw_win_scene(self):
        pass

    def draw_lose_scene(self):
        texture = arcade.load_texture(os.path.join(SPRITES_PATH, 'lose_scene.png'))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, texture.width, texture.height, texture, 0)

        self.scoretext_str = 'Score: ' + str(int(np.floor(self.score)))
        self.scoretext = arcade.draw_text(self.scoretext_str, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.4,
                                          arcade.color.WHITE,
                                          align="center", anchor_x="center", bold=True, font_size=24)

        self.highscore_str = 'Highscore: ' + str(int(np.floor(GameData.data.get('highscore'))))
        self.highscore_text = arcade.draw_text(self.highscore_str, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 30,
                                          arcade.color.WHITE,
                                          align="left", anchor_x="right", bold=True, font_size=16)

    def draw_start_scene(self):
        """
        Draw an instruction page. Load the page as an image.
        """
        texture = arcade.load_texture(os.path.join(SPRITES_PATH, 'title_screen.png'))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, texture.width, texture.height, texture, 0)

    def restart_game(self):
        self.initialize_vars()
        self.make_sprites()
        self.current_scene = GAME_RUNNING_SCENE_INDEX


class DumbClass():
    '''
    Stores persistent data
    '''

    # Initializes data dictionary keys for saving and loading data
    NUM_ACHIEVEMENTS = 0
    FILE_NAME = 'GameData.pickle'
    initial_data = {
        'highscore': 0,
        'top10': [0 for i in range(10)],
        'achievements_complete': [False for j in range(NUM_ACHIEVEMENTS)]
    }
    data = initial_data

    @staticmethod
    def __init__():
        '''
        When GameData class is initialized, it tries to load previous GameData
        '''
        pass
        DumbClass.load_data()

    @staticmethod
    def save_data():
        '''
        Saves data
        '''
        try:
            with open(DumbClass.FILE_NAME, 'wb') as f:
                pickle.dump(DumbClass.data, f, pickle.HIGHEST_PROTOCOL)
        except:
            pass

    @staticmethod
    def load_data():
        '''
        Loads data
        '''
        data = None
        try:
            with open(DumbClass.FILE_NAME, 'rb') as f:
                data = pickle.load(f)
        except:
            pass

        #DumbClass.data = data

        return DumbClass.data


def main():
    GameData(SCREEN_TITLE)
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()