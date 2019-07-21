import boto3
import os
import sys
import pygame

from aiy.board import Board, Led

client = boto3.client('lex-runtime')
inputFile = 'request.wav'
FULFILLED = 'Fulfilled'
isFollowingUp = False

def listen():
  os.system('sox -v 0.99 -d -t wavpcm -c 1 -b 16 -r 16000 -e signed-integer --endian little - silence 1 0 1% 5 0.3t 2% > ' + inputFile)

def post_audio_to_lex():
  with open(inputFile, 'rb') as f:
    file_content = f.read()

  response = client.post_content(
    botName='MachineTemperature',
    botAlias='prod',
    userId='lexTesting',
    contentType='audio/l16; rate=16000; channels=1',
    inputStream=file_content
  )

  speak(response['audioStream'])

  global isFollowingUp
  isFollowingUp = response['dialogState'] != FULFILLED

def speak(audio):
  os.environ["SDL_VIDEODRIVER"] = "dummy"
  pygame.init()
  pygame.display.set_mode((1,1))
  pygame.mixer.music.load(audio)
  pygame.mixer.music.play(0)

  clock = pygame.time.Clock()
  clock.tick(10)
  while pygame.mixer.music.get_busy():
      pygame.event.poll()
      clock.tick(10)
  pygame.display.quit()
  pygame.quit()


with Board() as board:

  while True:
    board.led.brightness = 0.1
    board.led.state = Led.ON

    if isFollowingUp == False:
      board.button.wait_for_press()
      isFollowingUp = True

    if isFollowingUp == True:
      board.led.brightness = 1
      listen()
      board.led.state = Led.PULSE_SLOW
      post_audio_to_lex()
