# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# The game starts here.

label start:
    "Ciudad Nova, día de elecciones..."

    call nueva_publicacion

    "Reputación: [stats['reputacion']]"

    call nueva_publicacion

    "Fin del día."
    return

