import math
import random
from src.helpers import import_assets
from src.config import *
from src.timer import Timer
from src.sprites import Shot, Explosion


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, screen, sound_manager, player, data, group):
        super().__init__(group)

        self.screen = screen
        self.sound_manager = sound_manager
        self.player = player
        self.group = group
        self.animation_speed = 20

        self.frames = import_assets(data['frames'])
        self.index = 0
        self.angle = 0
        self.energy = data['energy']
        self.bump_power = data['bump_power']
        self.shot_score = data['shot_score']
        self.kill_score = data['kill_score']
        self.can_shoot = data['can_shoot']

        self.shots_group = pygame.sprite.Group()
        self.shot_power = 20
        # self.shoot_timer = Timer(5000, self.shoot, repeat=True, autostart=True)

        self.image = self.frames[self.index]

    def animate(self, dt):
        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 0

        # Get the current frame and rotate it
        frame = self.frames[int(self.index)]
        self.image = pygame.transform.rotate(frame, self.angle)

        # Update rect after rotation to maintain position
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        if self.can_shoot:
            if 1 == random.choice([0, 0, 0, 0, 1]):
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                Shot(self.rect, self.shots_group, 'enemy', direction)

    def collisions(self):
        if not self.player.god_mode:
            for sprite in self.group[0].sprites():
                for shot in sprite.shots_group:
                    if pygame.sprite.collide_mask(shot, self.player):
                        shot.kill()
                        self.player.current_energy -= sprite.shot_power
                        Explosion(shot.rect.center, self.group[1])
                        self.sound_manager.play_sound(SOUND_EFFECTS['explosion'])

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power
        if self.energy <= 0:
            self.kill()

    def kill_off_screen(self):
        if (self.rect.bottom < -30 or self.rect.top > HEIGHT + 30 or
                self.rect.right < -30 or self.rect.left > WIDTH + 30):
            self.kill()

    def update(self, dt):
        # self.shoot_timer.update()
        self.animate(dt)
        # self.shoot()

        self.shots_group.update(dt)
        self.shots_group.draw(self.screen)
        self.collisions()
        self.kill_off_screen()


class Enemy(EnemyBase):
    def __init__(self, screen, sound_manager, player, enemy_type, enemy_speed, waypoints, rotate, group):
        data = ENEMY_DATA[enemy_type]
        super().__init__(screen, sound_manager, player, data, group)

        self.enemy_type = enemy_type
        self.speed = enemy_speed
        self.waypoints = waypoints
        self.rotate = rotate
        self.current_waypoint = 0

        self.pos = pygame.math.Vector2(waypoints[0])
        self.rect = self.image.get_rect(center=self.pos)

        self.rotated_images = self.pre_rotate_images(self.frames[int(self.index)], range(0, 360, 5))


    @staticmethod
    def pre_rotate_images(image, angles):
        rotated_images = {}
        for angle in angles:
            rotated_images[angle] = pygame.transform.rotate(image, angle)
        return rotated_images

    def move(self, dt):
        if self.current_waypoint < len(self.waypoints):
            target_x, target_y = self.waypoints[self.current_waypoint]
            dx, dy = target_x - self.pos.x, target_y - self.pos.y
            dist = math.hypot(dx, dy)

            if dist > 0:
                direction = pygame.math.Vector2(dx, dy).normalize()
                self.pos += direction * self.speed * dt

                # Calculate the angle and rotate the image
                if self.rotate:
                    self.angle = math.degrees(math.atan2(-dy, dx)) + 90

                # Update the rect to match new image
                self.rect = self.image.get_rect(center=self.pos)

            if dist < self.speed * dt:
                self.current_waypoint += 1

    def update(self, dt):
        super().update(dt)
        self.move(dt)


class Boss(EnemyBase):
    def __init__(self, screen, player, sound_manager, group):
        data = ENEMY_DATA['boss']
        super().__init__(screen, sound_manager, player, data, group)

        self.pos = pygame.math.Vector2(WIDTH / 2, 25)
        self.rect = self.image.get_rect(center=self.pos)

        self.direction = 1
        self.vert_speed = OBJECT_SPEEDS['boss']

    def move(self, dt):
        if self.pos.y >= 70:
            self.direction = -1
        elif self.pos.y <= 25:
            self.direction = 1

        self.pos.y += self.direction * self.vert_speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        super().update(dt)
        self.move(dt)
