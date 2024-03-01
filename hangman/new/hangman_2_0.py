import pygame
import os
import random
from string import ascii_uppercase
from spriteloader import SpriteSheet

pygame.init()
pygame.font.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Initialize pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman Game")

scale = 1
# Load fonts
font_small = pygame.font.SysFont(None, 36)
font_large = pygame.font.SysFont(None, 72)

# Load sound effects
correct_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-correct-answer-tone-2870.wav")
win_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-cheering-crowd-loud-whistle-610.wav")
lose_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-sad-game-over-trombone-471.wav")

class HangmanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Initialize Pygame window
        pygame.display.set_caption("Hangman Game")

        scale = 1
        # Load fonts
        self.font_small = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 72)

        # Load images
        # Load images
        hang_1_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hang_1.png')
        hang_2_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hang_2.png')
        hang_3_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hangman_3.png')
        hang_4_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hang_4.png')
        hang_5_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hangman_5.png')
        hang_6_asset = pygame.image.load(r'C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sprites\hang_6.png')

        hang_1_sheet = SpriteSheet(hang_1_asset)
        hang_2_sheet = SpriteSheet(hang_2_asset)
        hang_3_sheet = SpriteSheet(hang_3_asset)
        hang_4_sheet = SpriteSheet(hang_4_asset)
        hang_5_sheet = SpriteSheet(hang_5_asset)
        hang_6_sheet = SpriteSheet(hang_6_asset)

        hang_1_frames = [hang_1_sheet.get_img(frame, 600, 790, scale, BLACK) for frame in range(14)]
        hang_2_frames = [hang_2_sheet.get_img(frame, 600, 790, scale, BLACK) for frame in range(7)]
        hang_3_frames = [hang_3_sheet.get_img(frame, 600, 790, scale, BLACK) for frame in range(27)]
        hang_4_frames = [hang_4_sheet.get_img(frame, 600, 800, scale, BLACK) for frame in range(18)]
        hang_5_frames = [hang_5_sheet.get_img(frame, 600, 790, scale, BLACK) for frame in range(9)]
        hang_6_frames = [hang_6_sheet.get_img(frame, 600, 790, scale, BLACK) for frame in range(22)]

        # Load sound effects
        self.correct_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-correct-answer-tone-2870.wav")
        self.win_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-cheering-crowd-loud-whistle-610.wav")
        self.lose_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-sad-game-over-trombone-471.wav")

        self.hangman_frames = [hang_1_frames, hang_2_frames, hang_3_frames, hang_4_frames, hang_5_frames, hang_6_frames]

        self.words = self.load_words_from_file(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\words.txt")
        self.secret_word = random.choice(self.words)
        self.guessed_word = "*" * len(self.secret_word)
        self.wrong_guesses = []
        self.max_wrong_guesses = 6
        self.current_hangman_frame = 0
        self.guesses_left = self.max_wrong_guesses
        self.timer = 60
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.game_won = False

    def load_words_from_file(self, filename):
        with open(filename, "r") as file:
            words = file.read().split("\n")
        return words

    def draw_hangman(self):
        # Draw black border around the screen
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        # Draw HANGMAN title at the top center
        self.draw_text("HANGMAN", font_large, BLACK, SCREEN_WIDTH // 2, 50)

        if not self.game_over and not self.game_won:
            if 0 <= self.current_hangman_frame < len(self.hangman_frames):  # Ensure current_hangman_frame is valid
                frames = self.hangman_frames[self.current_hangman_frame]
                if frames:
                    sprite_width = frames[0].get_width()
                    sprite_height = frames[0].get_height()
                    x = (SCREEN_WIDTH - sprite_width) // 2
                    y = (SCREEN_HEIGHT - sprite_height) // 2

                    # Calculate frame delay based on animation speed
                    frame_delay = 100  # Adjust as needed

                    for i, frame in enumerate(frames):
                        self.screen.blit(frame, (x, y))
                        self.draw_text(f"Guesses left: {self.guesses_left}", font_small, BLACK, 100, 100)  # Draw guesses left
                        self.draw_text(f"Secret Word: {self.display_secret_word()}", font_small, BLACK, 200, 150)  # Adjusted x-coordinate
                        self.draw_text(f"Guessed Letters: {', '.join(self.wrong_guesses)}", font_small, BLACK, 200, 200)  # Adjusted x-coordinate
                        pygame.display.update()

                        # Add a delay between frames for smoother animation
                        pygame.time.delay(frame_delay)

                        # Check if it's the last frame of the animation
                        if i == len(frames) - 1:
                            pygame.time.delay(frame_delay * 5)  # Longer delay at the end of the animation

        else:
            if 0 <= self.current_hangman_frame < len(self.hangman_frames):  # Ensure current_hangman_frame is valid
                last_frame = self.hangman_frames[self.current_hangman_frame][-1]
                sprite_width = last_frame.get_width()
                sprite_height = last_frame.get_height()
                x = (SCREEN_WIDTH - sprite_width) // 2
                y = (SCREEN_HEIGHT - sprite_height) // 2

                self.screen.blit(last_frame, (x, y))
                self.draw_text(f"Guesses left: {self.guesses_left}", font_small, BLACK, 100, 100)  # Draw guesses left
                self.draw_text(f"Secret Word: {self.display_secret_word()}", font_small, BLACK, 100, 150)  # Draw secret word
                self.draw_text(f"Guessed Letters: {', '.join(self.wrong_guesses)}", font_small, BLACK, 100, 200)  # Draw guessed letters



              

    def display_secret_word(self):
        displayed_word = ""
        for char, guess in zip(self.secret_word, self.guessed_word):
            if guess != "*":
                displayed_word += guess + " "
            else:
                displayed_word += "_ "  # Replace "*" with "_ " for unrevealed letters
        return displayed_word.strip()




    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)



    def handle_guess(self, guess_letter):
        if guess_letter in ascii_uppercase:  # Check if the pressed key is a valid uppercase letter
            if guess_letter in self.secret_word.upper():  # Check if the guessed letter is in the secret word (ignoring case)
                self.update_guessed_word(guess_letter)
                correct_sound.play()
                if self.guessed_word == self.secret_word:
                    self.game_won = True
            else:
                self.wrong_guesses.append(guess_letter)
                self.current_hangman_frame += 1
                self.guesses_left -= 1
                if self.current_hangman_frame == self.max_wrong_guesses:
                    self.game_over = True
                    lose_sound.play()


    def update_guessed_word(self, guess_letter):
        updated_word = ""
        for char in self.secret_word:
            if char.upper() == guess_letter:
                updated_word += char
            else:
                updated_word += "*" if char not in self.guessed_word else char
        self.guessed_word = updated_word



    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_word = "*" * len(self.secret_word)
        self.wrong_guesses = []
        self.current_hangman_frame = 0
        self.guesses_left = self.max_wrong_guesses
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.game_won = False

    def run(self):
        while True:
            self.handle_events()

            self.screen.fill(WHITE)

            self.draw_hangman()

            if not self.game_over and not self.game_won:
                self.draw_text(f"Running", font_small, BLACK, 100, 50)
            elif self.game_won:
                self.draw_text("Congratulations! You win!", font_large, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                win_sound.play()
            else:
                self.draw_text("Game over! You lose!", font_large, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                lose_sound.play()
                pygame.display.update()
                pygame.time.delay(2000)

            pygame.display.update()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if not self.game_over and not self.game_won:
                    self.handle_guess(event.unicode.upper())
                elif event.key == pygame.K_RETURN:
                    self.reset_game()

  


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
