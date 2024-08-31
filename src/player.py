from src.config import *
from src.helpers import import_image, import_assets
from src.timer import Timer
from src.sprites import Shot, Explosion
from src.messages import Message


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, sound_manager, enemy_sprites, group):
        super().__init__(group)

        self.screen = screen
        self.sound_manager = sound_manager
        self.enemy_sprites = enemy_sprites
        self.group = group

        # Import assets
        self.ship_empty_frames = import_image('assets/img/ship/empty.png')
        self.ship_idle_frames = import_image('assets/img/ship/idle/0.png')
        self.ship_left_frames = import_assets('assets/img/ship/left/')
        self.ship_right_frames = import_assets('assets/img/ship/right/')
        self.god_mode_idle_frames = [self.ship_idle_frames, self.ship_empty_frames, self.ship_idle_frames, self.ship_empty_frames]
        self.god_mode_left_frames = [self.ship_left_frames[0], self.ship_empty_frames, self.ship_left_frames[1], self.ship_empty_frames]
        self.god_mode_right_frames = [self.ship_right_frames[0], self.ship_empty_frames, self.ship_right_frames[1], self.ship_empty_frames]
        self.frame_index = 0

        # Player image and rect
        self.image = self.ship_idle_frames
        self.rect = self.image.get_frect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)

        # Fumes img and rect
        self.fumes_frames = import_assets('assets/img/ship/fumes')
        self.god_mode_fumes_frames = [self.fumes_frames[0], self.ship_empty_frames, self.fumes_frames[1]]
        self.fumes_index = 0
        self.fumes_image = self.fumes_frames[self.fumes_index]
        self.fumes_rect = self.fumes_image.get_frect()

        # Data
        self.status = 'idle'
        self.speed = OBJECT_SPEEDS['player']
        self.current_energy = 100
        self.max_energy = 100
        self.lives = 4
        self.score = 0
        self.enemy_kill_count = 0

        # Shots
        self.shots_group = pygame.sprite.Group()
        self.shot_speed = 200
        self.shot_power = 10

        # Timers
        self.shot_timer = Timer(200)
        self.bump_timer = Timer(500)
        self.god_mode_timer = Timer(5000, self.reset_god_mode)

        self.first_shot_timer = pygame.time.get_ticks()
        self.first_shot_delay = 1000

        # Extra
        self.god_mode = False
        self.message = Message(self.screen, 'LIFE LOST', FONT20, 3000, (WIDTH / 2 - 54, HEIGHT / 2 - 19))

        # Joystick
        self.joystick_connected = False
        self.joystick = None
        self.check_joystick()

    def check_joystick(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick_connected = True

    def animate_player(self, frames, dt):
        self.frame_index += (10 if self.god_mode else 20) * dt
        if self.frame_index >= len(frames):
            self.frame_index = 2
        self.image = frames[int(self.frame_index)]

    def animate_fumes(self, dt):
        frames = self.god_mode_fumes_frames if self.god_mode else self.fumes_frames
        self.fumes_index += (10 if self.god_mode else 20) * dt
        if self.fumes_index >= len(frames):
            self.fumes_index = 0
        self.fumes_image = frames[int(self.fumes_index)]

    def animate(self, dt):
        frames = {
            'idle': self.god_mode_idle_frames if self.god_mode else self.ship_idle_frames,
            'left': self.god_mode_left_frames if self.god_mode else self.ship_left_frames,
            'right': self.god_mode_right_frames if self.god_mode else self.ship_right_frames,
        }

        if self.status == 'idle' and not self.god_mode:
            self.image = frames['idle']
            self.frame_index = 0
        else:
            self.animate_player(frames[self.status], dt)

        self.animate_fumes(dt)

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.y = -1 if keys[pygame.K_UP] else (1 if keys[pygame.K_DOWN] else 0)
        self.direction.x = -1 if keys[pygame.K_LEFT] else (1 if keys[pygame.K_RIGHT] else 0)

        if keys[pygame.K_LEFT]:
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.status = 'right'
        else:
            self.status = 'idle'

        if keys[pygame.K_SPACE] and not self.shot_timer.active:
            Shot(self.rect, self.shot_speed, self.shots_group, 'player')
            self.sound_manager.play_sound(SOUND_EFFECTS['player_shot'])
            self.shot_timer.activate()

        self.handle_joystick_input()

    def handle_joystick_input(self):
        if self.joystick_connected:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            # Override keyboard input with joystick input if it's significant
            if abs(axis_x) > 0.5:
                self.direction.x = -1 if axis_x < 0 else 1
                self.status = 'left' if axis_x < 0 else 'right'
            if abs(axis_y) > 0.5:
                self.direction.y = -1 if axis_y < 0 else 1

        if pygame.time.get_ticks() - self.first_shot_timer > self.first_shot_delay:
            if self.joystick and self.joystick.get_button(0) and not self.shot_timer.active:
                Shot(self.rect, self.shot_speed, self.shots_group, 'player')
                self.sound_manager.play_sound(SOUND_EFFECTS['player_shot'])
                self.shot_timer.activate()

    def move_fumes(self):
        if not self.god_mode:
            self.screen.blit(self.fumes_image, self.fumes_rect)
            self.fumes_rect.midtop = self.rect.midbottom[0], self.rect.midbottom[1] - 1

    def move(self, dt):
        self.move_fumes()

        if self.direction.magnitude() > 0:
            self.direction = round(self.direction.normalize())

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def move_boss_killed(self):
        self.image = self.ship_idle_frames
        self.pos.y -= 2
        self.rect.topleft = self.pos

    def stay_within_boundaries(self):
        if self.rect.left < 0:
            self.pos.x = self.rect.width / 2
        elif self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width / 2

        if self.rect.top < 0:
            self.pos.y = self.rect.height / 2
        elif self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height / 2

        self.rect.center = self.pos

    def check_collisions(self):
        # shots
        for shot in self.shots_group:
            hits = pygame.sprite.spritecollide(shot, self.enemy_sprites, False)
            if hits:
                shot.kill()
                for enemy in hits:
                    if enemy.energy > 0:
                        enemy.deduct_energy(self.shot_power)
                        self.score += enemy.shot_score
                    if enemy.energy <= 0:
                        self.enemy_kill_count += 1
                        self.score += enemy.kill_score

                    Explosion(enemy.rect.center, self.group)
                    self.sound_manager.play_sound(SOUND_EFFECTS['explosion'])
        # bumps
        if not self.bump_timer.active:
            bumps = pygame.sprite.spritecollide(self, self.enemy_sprites, False)
            for enemy in bumps:
                if not self.god_mode:
                    self.get_damage(enemy.bump_power)
                    Explosion(self.rect.center, self.group)
                    self.sound_manager.play_sound(SOUND_EFFECTS['explosion'])
                    self.bump_timer.activate()

    def get_damage(self, damage_value):
        if not self.god_mode and self.current_energy > 0:
            self.current_energy -= damage_value

    def deduct_life(self):
        if self.current_energy <= 0:
            self.current_energy = 0
            self.message.show()
            self.sound_manager.play_sound(SOUND_EFFECTS['lost_life'])
            self.lives -= 1
            self.current_energy = self.max_energy
            self.god_mode = True
            self.god_mode_timer.activate()

    def reset_god_mode(self):
        self.god_mode = False

    def reset(self):
        self.score = 0
        self.enemy_kill_count = 0
        self.lives = 4
        self.current_energy = 100
        self.rect = self.image.get_frect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.god_mode = False
        self.message.hide()
        self.shots_group.empty()
        self.first_shot_timer = pygame.time.get_ticks()

    def update_groups(self, dt):
        self.shots_group.update(dt)
        self.shots_group.draw(self.screen)

    def update_timers(self):
        self.shot_timer.update()
        self.bump_timer.update()
        self.god_mode_timer.update()

    def update(self, dt):
        self.update_timers()
        self.input()
        self.move(dt)
        self.animate(dt)
        self.stay_within_boundaries()
        self.update_groups(dt)
        self.check_collisions()
        self.deduct_life()
        self.message.update()
