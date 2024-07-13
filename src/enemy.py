import random
from src.helpers import import_assets
from src.config import *
from src.timer import Timer
from src.sprites import Shot, Explosion


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, sound_manager, player, enemy_size, current_level, group):
        super().__init__(group)

        self.screen = screen
        self.sound_manager = sound_manager
        self.player = player
        self.enemy_size = enemy_size
        self.current_level = current_level
        self.group = group
        self.animation_speed = 20

        data = ENEMY_DATA[enemy_size]
        self.frames = import_assets(data['frames'])
        self.index = 0
        self.energy = data['energy']
        self.bump_power = data['bump_power']
        self.shot_score = data['shot_score']
        self.kill_score = data['kill_score']
        self.can_shoot = data['can_shoot']
        self.enemy_speed = ENEMY_LEVEL_DATA[self.current_level]['speed'][self.enemy_size]

        self.pos = pygame.math.Vector2(random.randint(10, WIDTH - 10), 0)

        self.shots_group = pygame.sprite.Group()
        self.shot_power = 20
        self.shoot_timer = Timer(1000, self.shoot, repeat=True, autostart=True)

        self.image = self.frames[self.index]
        self.rect = self.image.get_frect(midbottom=self.pos)

        self.waypoints = [
            pygame.math.Vector2(random.randint(10, WIDTH - 10), random.randint(10, HEIGHT))
            for _ in range(3)
        ]
        self.current_waypoint = 0

    def animate(self, dt):
        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def move(self, dt):
        if self.current_waypoint < len(self.waypoints):
            target = self.waypoints[self.current_waypoint]
            direction = target - self.pos
            distance = direction.length()

            if distance > 0:
                direction.normalize_ip()
                self.pos += direction * self.enemy_speed * dt
                self.rect.midbottom = round(self.pos)

                if distance < self.enemy_speed * dt:
                    self.current_waypoint += 1
        else:
            self.pos.y += self.enemy_speed * dt
            self.rect.midbottom = round(self.pos)

    def collisions(self):
        if not self.player.god_mode:
            for sprite in self.group[0].sprites():
                for shot in sprite.shots_group:
                    hits = pygame.sprite.collide_mask(shot, self.player)
                    if hits:
                        shot.kill()
                        self.player.current_energy -= sprite.shot_power
                        Explosion(shot.rect.center, self.group[1])
                        self.sound_manager.play_sound(SOUND_EFFECTS['explosion'])

    def shoot(self):
        if self.can_shoot:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            if dx > 0 and dy > 0:
                direction = pygame.math.Vector2(dx, dy).normalize()
                Shot(self.rect, self.shots_group, 'enemy', direction)
                self.shoot_timer.activate()

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power
        if self.energy <= 0:
            self.kill()

    def kill_off_screen(self):
        if self.rect.top > HEIGHT * 2 or self.rect.right < 0 or self.rect.left > WIDTH + 20:
            self.kill()

    def update(self, dt):
        self.shoot_timer.update()
        self.animate(dt)
        self.move(dt)
        self.kill_off_screen()
        self.shots_group.update(dt)
        self.shots_group.draw(self.screen)
        self.collisions()


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen, bg_img_width, window_height, player_rect, *args):
        super().__init__(*args)

        self.screen = screen
        self.bg_img_width = bg_img_width
        self.window_height = window_height
        self.player_rect = player_rect

        self.boss_img_1 = pygame.image.load("assets/img/boss/boss_1.png").convert_alpha()
        self.boss_img_2 = pygame.image.load("assets/img/boss/boss_2.png").convert_alpha()
        self.boss_frames = [self.boss_img_1, self.boss_img_2]
        self.boss_index = 0
        self.image = self.boss_frames[self.boss_index]
        self.rect = self.image.get_rect(center=(self.bg_img_width // 2, 10))

        self.energy = 300
        self.shot_power = 25
        self.bump_power = 60
        self.shot_score = 48
        self.kill_score = 5000
        self.can_shoot = True

        self.direction = 1
        self.vert_speed = 1

        self.shots = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()

    def animate(self):
        self.boss_index += 0.5
        if self.boss_index >= len(self.boss_frames):
            self.boss_index = 0
        self.image = self.boss_frames[int(self.boss_index)]

    def movement(self):
        if self.rect.y >= self.window_height - 100:
            self.direction = -1  # Move up when close to the bottom
        elif self.rect.y <= 10:
            self.direction = 1  # Move down when close to the top

        self.rect.y += self.direction * self.vert_speed

    def shoot(self):
        cur_time = pygame.time.get_ticks()
        shot_timing = random.randint(800, 1800)

        if cur_time - self.last_shot_time >= shot_timing and self.can_shoot:
            dx = self.player_rect.x - self.rect.x
            dy = self.player_rect.y - self.rect.y

            # Calculate the angle to the player for each bullet
            angle = math.atan2(dy, dx)

            # Calculate the direction vectors for each bullet based on the angles
            direction = (math.cos(angle), math.sin(angle))

            # Create two bullets with their respective directions
            shot = EnemyShot("boss", self.rect.center, self.window_height, self.bg_img_width, direction)

            self.shots.add(shot)
            self.last_shot_time = cur_time

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power

    def dead(self):
        if self.energy <= 0:
            self.kill()
            self.shots.empty()

    def update(self):
        self.animate()
        self.movement()
        self.shoot()
        self.dead()
        self.shots.draw(self.screen)
        self.shots.update()