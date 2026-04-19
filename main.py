import sounddevice as sd
import scipy.io.wavfile as wav
from pygame import*
from random import*
from numpy import*
init()
window_size = 1200, 700
window = display.set_mode(window_size)
bird = Rect(50, 500, 100, 100)
bird_img = image.load('bird.jpg')
bird_img = transform.scale(bird_img, (100, 100))
bird = bird_img.get_rect()
fs = 16000
block = 256
mic_level= 0.0
y_vel = 0.0
gravity = 0.03
THRESH = 0.06
impulse = -2.0
def generate_pipes(count, pipe_width= 140, gap = 280, min_heigh = 50, max_heigh = 440, distance = 800):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height =  randint(min_heigh, max_heigh)
        top_pipe = Rect(start_x,0,pipe_width,height)
        bottom_pipe = Rect(start_x, height+ gap, pipe_width, window_size[1]- (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return  pipes
def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(sqrt(mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

pipes = generate_pipes((150))
wait = 40
lose = False
with sd.InputStream(samplerate = fs, channels = 1, blocksize = block, callback = audio_cb):
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
        window.fill((255, 255, 255))
        window.blit(bird_img, bird)
        if bird.top < 0 or bird.bottom > 700:
            bird.y = 0

        if len(pipes) < 0:
            pipes += generate_pipes(150)

        if lose and wait > 1:
            for pipe in pipes:
                pipe.x +=15
            wait -= 1
        else:
            lose = False
            wait = 40

        for pipe in pipes:
            if not lose:
                pipe.x -= 1
            draw.rect(window, "green",pipe)
            if pipe.x <= -100:
                pipes.remove(pipe)
            if bird.colliderect(pipe):
                lose = True

        display.update()
        if mic_level > THRESH:
            y_vel = impulse
        y_vel += gravity
        bird.y += int(y_vel)
        keys = key.get_pressed()
        if keys[K_w]: bird.y -= 2
        if keys[K_s]: bird.y += 2