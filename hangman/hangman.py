import pygame
from pygame.locals import *
import os
import random
from string import ascii_letters

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Hang-Man")

class Hangman():
    def __init__(self):
        with open(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\words.txt", "r") as file:
            words = file.read().split("\n")
            self.secret_word = random.choice(words)
            self.guessed_word = "*" * len(self.secret_word)
        # Load sound files
        self.win_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-cheering-crowd-loud-whistle-610.wav")
        self.lose_sound = pygame.mixer.Sound(r"C:\Users\sidsa_irhzlmw\OneDrive\Documents\cc++\game\hangman\new\sounds\mixkit-sad-game-over-trombone-471.wav")       
        
        self.wrong_guesses = []
        self.wrong_guess_count = 0
        self.taking_guess = True
        self.running = True
        self.screen = screen
        self.background_color = (155, 120, 70)
        self.gallow_color = (0, 0, 0)
        self.body_color = (255, 254, 175)
        self.font = pygame.font.SysFont("Courier New", 20)
        self.FPS = pygame.time.Clock()

    def guess(self, guess_letter):
        if guess_letter in ascii_letters:
            if guess_letter in self.secret_word and guess_letter not in self.guessed_word:
                self.right_guess(guess_letter)
            elif guess_letter not in self.secret_word and guess_letter not in self.wrong_guesses:
                self.wrong_guess(guess_letter)

    def draw_gallow(self):
        pygame.draw.rect(self.screen, self.gallow_color, pygame.Rect(75, 280, 120, 10))  # Stand
        pygame.draw.rect(self.screen, self.gallow_color, pygame.Rect(128, 40, 10, 240))  # Body
        pygame.draw.rect(self.screen, self.gallow_color, pygame.Rect(128, 40, 80, 10))   # Hanger
        pygame.draw.rect(self.screen, self.gallow_color, pygame.Rect(205, 40, 10, 30))   # Rope

    def draw_man_pieces(self):
        if self.wrong_guess_count >= 1:
            pygame.draw.circle(self.screen, self.body_color, [210, 85], 20)  # Head
        if self.wrong_guess_count >= 2:
            pygame.draw.rect(self.screen, self.body_color, pygame.Rect(206, 105, 8, 45))  # Body
        if self.wrong_guess_count >= 3:
            pygame.draw.line(self.screen, self.body_color, [183, 149], [200, 107], 6)  # Right arm
        if self.wrong_guess_count >= 4:
            pygame.draw.line(self.screen, self.body_color, [231, 149], [218, 107], 6)  # Left arm
        if self.wrong_guess_count >= 5:
            pygame.draw.line(self.screen, self.body_color, [189, 198], [208, 148], 6)  # Right leg
        if self.wrong_guess_count >= 6:
            pygame.draw.line(self.screen, self.body_color, [224, 198], [210, 148], 6)  # Left leg

    def wrong_guess(self, guess_letter):
        self.wrong_guesses.append(guess_letter)
        self.wrong_guess_count += 1
        self.draw_man_pieces()

    def right_guess(self, guess_letter):
        index_positions = [index for index, item in enumerate(self.secret_word) if item == guess_letter]
        for i in index_positions:
            self.guessed_word = self.guessed_word[0:i] + guess_letter + self.guessed_word[i+1:]
        screen.fill(pygame.Color(self.background_color), (10, 370, 390, 20))

    def loss(self):
        self.running = False
        screen.fill((255, 0, 0))  # Red background for loss screen
        self.lose_sound.play()
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        pygame.quit()

    def win(self):
        self.running = False
        screen.fill((0, 255, 0))  # Green background for win screen
        self.win_sound.play()
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        pygame.quit()

    def draw_hangman(self):
        self.draw_gallow()
        self.draw_man_pieces()

    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.taking_guess:
                        self.guess(event.unicode)

            if self.guessed_word == self.secret_word:
                self.win()
            elif self.wrong_guess_count >= 6:
                self.loss()

            screen.fill(self.background_color)
            self.draw_hangman()
            guessed_word = self.font.render(f"Guessed word: {self.guessed_word}", True, (0, 0, 138))
            screen.blit(guessed_word, (10, 370))
            wrong_guesses = self.font.render(f"Wrong guesses: {' '.join(map(str, self.wrong_guesses))}", True, (125, 0, 0))
            screen.blit(wrong_guesses, (10, 420))

            pygame.display.flip()
            self.FPS.tick(60)

        pygame.quit()

if __name__ == "__main__":
    h = Hangman()
    h.main()
