import com_keyboard as win_kb
import time
import logging
from logging_config import setup_logging
import pop_wins as pwin

SC_UP    = 0x48
SC_LEFT  = 0x4B
SC_RIGHT = 0x4D
SC_DOWN  = 0x50

SC_F5 = 0x3F 
SC_CTRL=0x1D
SC_SPACE=0x39

# Example usage
if __name__ == "__main__":
    setup_logging()
    time.sleep(3)
 
    print("starting mouse tracking...")
    #pwin.info("Mouse Tracking", "The program will now track mouse position and color. Check the logs for details.")

    pwin.show_hud("Starting...", x=400, y=50)

    for i in range(5):
        pwin.update_hud(f"Step {i+1}/5")
        time.sleep(1)

    pwin.update_hud("Done!")
    time.sleep(2)

    
    while True:
        mouse_pos = win_kb.get_mouse_pos()
        mouse_pixel = win_kb.get_pixel(mouse_pos[0], mouse_pos[1])
        mouse_color = win_kb.get_color(mouse_pos[0], mouse_pos[1])
        #print(f"Mouse Position: {mouse_pos}, Pixel Color: {mouse_pixel}, Color Number: {mouse_color}")
        logging.critical(f"Mouse Position: {mouse_pos}, Pixel Color: {mouse_pixel}, Color Number: {mouse_color}")
        time.sleep(1)