import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    # class constants to represent each type of AnimatedSprite
    standard_img = None
    frame_width = 32
    frame_height = 32
    frame_list = None
    initialized = False
    num_sprites = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        
        if not self.initialized:
            self.total_frames = self.standard_img.get_rect().width / self.frame_width
            self.frame_height = self.standard_img.get_rect().height
            self.init_animation()
        self.current_frame = 0
        self.timer = pygame.time.get_ticks()
        self.image = self.frame_list[0]
        self.rect = pygame.Rect(0,0,self.frame_width,self.frame_height)
        self.frame_delay = 200
        self.dx = 0
        self.dy = 0
        self.rect.center = pos
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.loops = 0
        AnimatedSprite.num_sprites += 1
    def init_animation(self):
        self.frame_list = []
        for i in range(self.total_frames):
            self.frame_list.append(self.standard_img.subsurface(pygame.Rect(i * self.frame_width,0,self.frame_width,self.frame_height)))
        self.initialized = True
    def step_animation(self):
        self.current_frame += 1
        if self.current_frame >= self.total_frames:
            self.current_frame = 0
            self.loops += 1
        # define source rect and blit correct portion of standard image to image
        self.image = self.frame_list[self.current_frame]
    def update(self):
        current_time = pygame.time.get_ticks()
        self.centerx += self.dx
        self.centery += self.dy
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        if current_time - self.timer > self.frame_delay:
            self.step_animation()
            self.timer = current_time
      #  if self.rect.bottom < self.upper_bound or self.rect.top > self.lower_bound:
       #     self.kill()
    def kill(self):
        pygame.sprite.Sprite.kill(self)
        self.die()
    def die(self):
        pass
