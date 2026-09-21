# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# The game starts here.

label start:
    show screen sistema_civitas
    "Hoy es un día tranquilo en la ciudad."
    "Demasiado tranquilo, de hecho..."
    "Voy a seguir caminando hacia la universidad mientras reviso mis cosas."
    "Parece que no hay nada interesante por hacer hoy."

    while banco.hay_mas():
        "tal vez debería revisar mi teléfono para ver si hay algo nuevo."
    return

