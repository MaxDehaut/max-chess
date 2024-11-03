# Python Chess Engine

## Table of contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [TODO](#todo)
* [Instructions](#instructions)
* [References](#references)

## Introduction

[Eddie's YouTube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

## Prerequisites

* pygame 2.0.1
* Python 3.10.10

## TODO

- [ ] Cleaning up the code - right now it is really messy.
- [ ] Using numpy arrays instead of 2d lists.
- [ ] Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
- [ ] Menu to select player vs player/computer.
- [ ] Allow dragging pieces.
- [ ] Resolve ambiguating moves (notation).

## How-to

1. Select whether you want to play versus computer, against another player locally, or watch the game of engine playing against itself by setting appropriate flags in lines 52 and 53 of `ChessMain.py`.
2. Run `ChessMain.py`.

**Additional moves:**
* Press `z` to undo a move.
* Press `r` to reset the game.

## References

* Supported colors: [pygame](https://www.pygame.org/docs/ref/color_list.html)
