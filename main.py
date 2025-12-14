import pygame as py
import sys
import math
import random

py.init()
py.mixer.init()

try:
    py.mixer.music.load("assets/omori.mp3")
    py.mixer.music.set_volume(0.3)
    py.mixer.music.play(-1)
except py.error as e:
    print(f"⚠️ Could not load music: {e}")
    print("🎮 Game will continue without music...")

screen = py.display.set_mode((800, 600))
py.display.set_caption("✨Care for Pet✨")
clock = py.time.Clock()

try:
    bg = py.image.load("assets/background2.jpeg")
    background = py.transform.scale(bg, (800, 600))
except py.error as e:
    background = py.Surface((800, 600))
    background.fill((255, 192, 203))

try:
    happy = py.transform.scale(py.image.load("assets/happy.png"), (350, 350))
    hungry = py.transform.scale(py.image.load("assets/hungry.png"), (350, 350))
    sad = py.transform.scale(py.image.load("assets/sad.png"), (350, 350))
    sleep = py.transform.scale(py.image.load("assets/sleep.png"), (350, 350))
    sleepy = py.transform.scale(py.image.load("assets/love.png"), (350, 350))
except py.error as e:
    happy = py.Surface((350, 350))
    happy.fill((255, 255, 0))
    hungry = sad = sleep = sleepy = happy

petX, petY = 210, 180
pet_state = "happy"
message = "✨ Welcome! Click the numbers to care for your kitty ✨"
time = 0
pet_bob_offset = 0
happiness_level = 5
hunger_level = 3
energy_level = 4
love_level = 2

SOFT_PINK = (255, 20, 147)
LAVENDER = (138, 43, 226)
CREAM = (255, 253, 245)
ROSE_GOLD = (184, 115, 51)
MINT_GREEN = (60, 179, 113)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (105, 105, 105)
BUTTON_PINK = (255, 105, 180)
BUTTON_PURPLE = (186, 85, 211)
BUTTON_GREEN = (50, 205, 50)
BUTTON_BLUE = (70, 130, 180)
BUTTON_ORANGE = (255, 140, 0)

try:
    title_font = py.font.Font("assets/bubblegum.ttf", 28)
    message_font = py.font.Font("assets/bubblegum.ttf", 20)
    ui_font = py.font.Font("assets/bubblegum.ttf", 16)
    button_font = py.font.Font("assets/bubblegum.ttf", 18)
except:
    title_font = py.font.Font(None, 28)
    message_font = py.font.Font(None, 20)
    ui_font = py.font.Font(None, 16)
    button_font = py.font.Font(None, 18)

def draw_stat_bar(screen, x, y, width, height, value, max_value, color, label):
    py.draw.rect(screen, DARK_GRAY, (x-2, y-2, width+4, height+4), border_radius=12)
    py.draw.rect(screen, WHITE, (x, y, width, height), border_radius=10)
    fill_width = int((value / max_value) * width)
    py.draw.rect(screen, color, (x, y, fill_width, height), border_radius=10)
    py.draw.rect(screen, WHITE, (x, y, width, height), 3, border_radius=10)
    label_text = ui_font.render(f"{label}: {value}/{max_value}", True, WHITE)
    label_bg = py.Rect(x, y - 30, label_text.get_width() + 10, 25)
    py.draw.rect(screen, color, label_bg, border_radius=8)
    py.draw.rect(screen, WHITE, label_bg, 2, border_radius=8)
    screen.blit(label_text, (x + 5, y - 28))

def draw_retro_button(screen, x, y, width, height, text, color, text_color=WHITE):
    shadow_rect = py.Rect(x + 4, y + 4, width, height)
    py.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=15)
    button_rect = py.Rect(x, y, width, height)
    py.draw.rect(screen, color, button_rect, border_radius=15)
    highlight_rect = py.Rect(x + 2, y + 2, width - 4, height // 2)
    lighter_color = tuple(min(255, c + 40) for c in color)
    py.draw.rect(screen, lighter_color, highlight_rect, border_radius=10)
    py.draw.rect(screen, WHITE, button_rect, 3, border_radius=15)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_elegant_dialogue_box(screen, message):
    box_rect = py.Rect(50, 520, 700, 60)
    shadow_surf = py.Surface((box_rect.width + 6, box_rect.height + 6))
    shadow_surf.set_alpha(30)
    shadow_surf.fill(SOFT_PINK)
    screen.blit(shadow_surf, (box_rect.x + 3, box_rect.y + 3))
    py.draw.rect(screen, CREAM, box_rect, border_radius=15)
    py.draw.rect(screen, SOFT_PINK, box_rect, 3, border_radius=15)
    text = message_font.render(message, True, SOFT_PINK)
    text_rect = text.get_rect(center=(box_rect.centerx, box_rect.centery))
    screen.blit(text, text_rect)

running = True

while running:
    time += 1
    screen.blit(background, (0, 0))
    pet_bob_offset = math.sin(time * 0.05) * 8
    current_pet_y = petY + pet_bob_offset

    if pet_state == "happy":
        screen.blit(happy, (petX, current_pet_y))
    elif pet_state == "hungry":
        screen.blit(hungry, (petX, current_pet_y))
    elif pet_state == "sad":
        screen.blit(sad, (petX, current_pet_y))
    elif pet_state == "sleep":
        screen.blit(sleep, (petX, current_pet_y))
    elif pet_state == "sleepy":
        screen.blit(sleepy, (petX, current_pet_y))

    draw_stat_bar(screen, 50, 50, 180, 25, happiness_level, 10, SOFT_PINK, "💖 Happy")
    draw_stat_bar(screen, 50, 100, 180, 25, hunger_level, 10, MINT_GREEN, "🍎 Fed")
    draw_stat_bar(screen, 50, 150, 180, 25, energy_level, 10, LAVENDER, "⚡ Energy")
    draw_stat_bar(screen, 50, 200, 180, 25, love_level, 10, ROSE_GOLD, "💕 Love")

    draw_elegant_dialogue_box(screen, message)

    button_y = 280
    button_spacing = 50
    draw_retro_button(screen, 570, button_y, 180, 50, "1. MUNCH TIME! 🍎", BUTTON_GREEN)
    draw_retro_button(screen, 570, button_y + button_spacing, 180, 50, "2. IGNORE MODE 💔", BUTTON_BLUE)
    draw_retro_button(screen, 570, button_y + button_spacing*2, 180, 50, "3. LOVEY-DOVEY 💖", BUTTON_PINK)
    draw_retro_button(screen, 570, button_y + button_spacing*3, 180, 50, "4. SLEEPY VIBES 😴", BUTTON_PURPLE)
    draw_retro_button(screen, 570, button_y + button_spacing*4, 180, 50, "5. PLAYTIME! 🎉", BUTTON_ORANGE)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_1:
                pet_state = "hungry"
                message = "🍎 CHOMP CHOMP! Yummy food makes me super happy! 🥰"
                hunger_level = min(10, hunger_level + 3)
                happiness_level = min(10, happiness_level + 1)
            elif event.key == py.K_2:
                pet_state = "sad"
                message = "💔 Meow... why so mean? I just want attention... 😢"
                happiness_level = max(0, happiness_level - 2)
                love_level = max(0, love_level - 1)
            elif event.key == py.K_3:
                pet_state = "sleepy"
                message = "💖 OMG I LOVE YOU SOOO MUCH! You're my favorite human! ✨"
                love_level = min(10, love_level + 3)
                happiness_level = min(10, happiness_level + 2)
            elif event.key == py.K_4:
                pet_state = "sleep"
                message = "😴 Zzz... dreaming of treats and cuddles... 🌙"
                energy_level = min(10, energy_level + 4)
                happiness_level = min(10, happiness_level + 1)
            elif event.key == py.K_5:
                pet_state = "happy"
                message = "😊 WHEEE! Playing is the BEST! Let's do it again! 🎉"
                happiness_level = min(10, happiness_level + 3)
                energy_level = max(0, energy_level - 1)

    if time % 300 == 0:
        hunger_level = max(0, hunger_level - 1)
        energy_level = max(0, energy_level - 1)
        if happiness_level > 5:
            happiness_level = max(0, happiness_level - 1)

        # Auto-update pet state based on needs
        if hunger_level < 3:
            pet_state = "hungry"
            message = "🥺 I'm feeling hungry..."
        elif energy_level < 3:
            pet_state = "sleep"
            message = "💤 I'm getting sleepy..."
        elif happiness_level < 3:
            pet_state = "sad"
            message = "😿 Feeling a little down..."
        else:
            pet_state = "happy"
            message = "😺 I'm feeling great!"

    py.display.flip()
    clock.tick(30)

py.quit()
sys.exit()
