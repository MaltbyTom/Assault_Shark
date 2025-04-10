import pygame

# Split text into lines that fit within the surface width
def break_text_into_lines(text, font, surface_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_width, _ = font.size(test_line)
        if text_width > surface_width or word == "\n":
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines

def scroll_text_with_vanishing_point(font_name, start_font_size, font_color, surface, speed=1):
    """
    Scrolls the given text across the screen with a vanishing point effect.

    Args:
    - text (str): The large text string to display.
    - font_name (str): The name of the font (or a font file path) to use for rendering text.
    - start_font_size (int): The initial font size to start with.
    - font_color (tuple): The font color as an RGB tuple.
    - surface (pygame.Surface): The pygame surface (e.g., screen) to render text on.
    - speed (float): The speed at which the text scrolls.
    """
    # Define text, font, color
    text = """Assault Shark 
    \n \n The year is 2317, and the battleground has spread, not just beneath the waves, but high above in the skies.
    \n \n Science’s attempts to control nature have led to the creation of the ultimate weapon: bio-engineered creatures designed to fight in the most unforgiving of environments. 
    \n \n The most feared of them all? You. 
    \n \n The last surviving free eggheads, guardians of the fading spark of mankind's learning, eke out a precarious survival on near-orbit asteroid stations.  To regain Earth, they have plotted a dangerous mission. \n \n
    \n \n You must return to the skies, and strike down the evil mutant exo-marine jet creatures. Rescue more eggheads, reclaim the ancient fortresses of wisdom, and save Earth for a new age of enlightenment.
    \n \n You are the Shark Knight, the only remaining knight of the mystical order: pilots of jet-powered, bio-mechanical shark aircraft - a lethal fusion of oceanic predator and cutting-edge technology.  With advanced weaponry, agile jet propulsion, and the instincts of a true apex predator, you are the future's final hope against the plague of evil bio-craft.
    \n \n The skies are filled with deadly creatures: mutated squidships, transgenic manta blimps, rocket fish, and other monstrosities, each vying for dominion over the oceans and skies alike.  Supported by the artillery of the cryptofacist groundlings, the atmosphere has long been viewed as an impregnable death zone.
    \n \n Your mission: fight, survive, and conquer. Only one can rule the skies, and it’s time for the world to remember why the Shark is the ultimate predator.
    \n \n Out there, they’ll fear your bite.
    \n \n Welcome to the Assault Shark.
    \n \n Prepare for battle."""

    # Set up the initial font and break the text into lines
    font = pygame.font.Font(font_name, start_font_size)
    lines = break_text_into_lines(text, font, surface.get_width())
    
    # Reverse the lines so that they start from the top of the screen
    lines.reverse()
    
    return lines
    
