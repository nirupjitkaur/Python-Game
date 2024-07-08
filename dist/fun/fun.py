import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

pygame.init()

width, height = 1400, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pendulum Simulation with Energy Graphs")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SLIDER= (137, 148, 153)
BACKGROUND_COLOR = WHITE
BOB_COLOR = RED
LBLUE = (135, 206, 235)
VIOLET = (173, 216, 230)
DARK_GREEN= (21,176,21)
CARROT=(245,122, 138)
GREY=(200,200,200)

B=(70,102,255)
BACK_BUTTON = (150, 150, 150)



GRADIENT_COLORS = [
    (204, 249, 255), 
    (124, 232, 255),  
    (85, 208, 255),   
    (0, 172, 223),    
    (0, 128, 191)     
]

# Function to interpolate colors vertically
def interpolate_color(color1, color2, interval):
    return tuple(int(color1[channel] + (color2[channel] - color1[channel]) * interval) for channel in range(3))


def draw_vertical_gradient(screen, colors):               #For home screen
    rect = pygame.Rect(0, 0, width, height)
    gradient = pygame.Surface((width, height))
    num_colors = len(colors)
    section_height = height / (num_colors - 1)
    
   
    for i in range(num_colors - 1):
        color_start = colors[i]
        color_end = colors[i + 1]
        
        
        for y in range(int(section_height * i), int(section_height * (i + 1))):
            interval = (y - section_height * i) / section_height
            color = interpolate_color(color_start, color_end, interval)
            pygame.draw.line(gradient, color, (0, y), (width, y))
    
    screen.blit(gradient, rect)

    
pivot_x = width // 2
pivot_y = 150
arm_length = 150
angle = math.pi / 4
angular_velocity = 0
angular_acceleration = 0
mass_radius = 5
gravity = 9.8


font = pygame.font.Font(None, 30)

bold_font = pygame.font.Font('Algerian Regular.ttf', 60)  

history_length = 300
pe_history = []
ke_history = []

slider_width = 300
slider_height = 5
slider_spacing = 70

length_slider = pygame.Rect(50, 100, slider_width, slider_height)
mass_slider = pygame.Rect(50, 200, slider_width, slider_height)
gravity_slider = pygame.Rect(50, 300, slider_width, slider_height)
angle_slider = pygame.Rect(50, 400, slider_width, slider_height)

length_knob_x = length_slider.x + int(arm_length)
mass_knob_x = mass_slider.x + int(mass_radius)
gravity_knob_x = gravity_slider.x + int(gravity * 10)
angle_knob_x = angle_slider.x + int((angle / (2 * math.pi)) * slider_width)

dragging_length = False
dragging_mass = False
dragging_gravity = False
dragging_angle = False
logo1 = pygame.image.load("csio.png")
logo1 = pygame.transform.scale(logo1, (150, 130))  

logo2 = pygame.image.load("new.png")
logo2 = pygame.transform.scale(logo2, (210, 120)) 

logo3 = pygame.image.load("csir.png")
logo3 = pygame.transform.scale(logo3, (200, 170)) 


logo1_pos = (50, 50)
logo2_pos = (width // 2 - 100, 50) 
logo3_pos = (width - 250, 50)

clock = pygame.time.Clock()
running = True
running_simulation = False

def calculate_max_speed():
    return 2 * math.pi * math.sqrt(arm_length * gravity)

max_speed = calculate_max_speed()

initial_length_knob_x = length_knob_x
initial_mass_knob_x = mass_knob_x
initial_gravity_knob_x = gravity_knob_x
initial_angle_knob_x = angle_knob_x

info_window_rect = pygame.Rect(400, 20, 950, 650)   
    
button_width = 200
button_height = 50
button_spacing= 30
button_x = info_window_rect.x + 160
button_y_start = info_window_rect.y + 50

button1_rect = pygame.Rect(button_x, button_y_start, button_width, button_height)
button2_rect = pygame.Rect(button_x + button_width + button_spacing, button_y_start, button_width, button_height)
button3_rect = pygame.Rect(button_x + 2 * (button_width + button_spacing), button_y_start, button_width, button_height)


# Render text for buttons
button_font = pygame.font.Font(None, 36)
button1_text = button_font.render("Objective", True, BLACK)
button2_text = button_font.render("Science", True, BLACK)
button3_text = button_font.render("Description", True, BLACK)

info_window_open = False

PAGE_OBJECTIVE = 1
PAGE_SCIENCE = 2
PAGE_DESCRIPTION = 3
current_page = None

def render_text_list(screen, font, text_list, pos, color=BLACK, font_size=10):
    x, y = pos
    font = pygame.font.Font(None, font_size)
    for line in text_list:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height() 

homepage = True

COLORS = [
    (99, 229, 255),   
    (138, 236, 255),  
    (177, 242, 255),  
    (216, 249, 255)   
]

def draw_vertical_gradient2(screen, colors):            # SIMULATION PAGE
    rect = pygame.Rect(0, 0, width, height)
    gradient = pygame.Surface((width, height))
    num_colors = len(colors)
    section_height = height / (num_colors - 1)

    for i in range(num_colors - 1):
        color_start = colors[i]
        color_end = colors[i + 1]

        for y in range(int(section_height * i), int(section_height * (i + 1))):
            interval = (y - section_height * i) / section_height
            color = interpolate_color(color_start, color_end, interval)
            pygame.draw.line(gradient, color, (0, y), (width, y))

    screen.blit(gradient, rect)

def draw_linear_gradient_rect(screen, rect, colors):        #credits text
    start_color = colors[0]
    end_color = colors[1]
    x, y, w, h = rect

    for i in range(w):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / w))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / w))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / w))
        pygame.draw.line(screen, (r, g, b), (x + i, y), (x + i, y + h))


LIGHT_BLUE_START = (183, 233, 247)  
LIGHT_BLUE_END = (219, 243, 250)    



def draw_gradient_background(screen, rect, start_color, end_color):      
    x, y, w, h = rect
    step_r = (end_color[0] - start_color[0]) / h
    step_g = (end_color[1] - start_color[1]) / h
    step_b = (end_color[2] - start_color[2]) / h

    for i in range(h):
        r = int(start_color[0] + step_r * i)
        g = int(start_color[1] + step_g * i)
        b = int(start_color[2] + step_b * i)
        pygame.draw.line(screen, (r, g, b), (x, y + i), (x + w, y + i))

credits_font_size = 25
credits_font = pygame.font.Font(None, credits_font_size)

tutorial_window_open = False

def render_text_list_info(screen, font, text_list, pos, color=BLACK, font_size=30):
    x, y = pos
    font = pygame.font.Font(None, font_size)
    for line in text_list:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height() 

def render_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
    

def show_tutorial_window(screen):
    tutorial_window_rect = pygame.Rect(0, 0, 1400, 700)
    pygame.draw.rect(screen, WHITE, tutorial_window_rect)
    draw_vertical_gradient(screen, GRADIENT_COLORS) 

    tutorial_text = [
        "                                             TUTORIAL:",
        "",
        "                   Welcome to the Pendulum Simulation Tutorial!",
        "",
        "      This simulation allows you to interactively explore the dynamics of a pendulum. You can",
        "      adjust the parameters listed below using sliders, observe the pendulum's motion, view ",
        "      real-time energy graphs, and access additional information.",
        "",
        "Controls: There are sliders for length of string, mass of bob, gravity and initial angle of pendulum.",
        "Displayed Metrics: The metrics (time period, max speed, current angle) vary based on the slider values.",
        "Energy Graph: The energy graph displays the kinetic energy (KE) and potential energy (PE) of the pendulum","over time.",
"Information Button (i): Provides detailed explanations and formulas related to pendulum dynamics.",
"",
"Getting Started:", "",
"1. Use the sliders to adjust the parameters as desired.",
"2. Click Start to begin the simulation or Stop to pause it.",
"3. Click Reset to return the parameters to their default values.",
"4. Click the i button for additional information.",
"5. Click Back to return to the home screen.",
"",
"Explore different combinations to observe how each parameter affects the pendulum's motion!",
"",
"Example Scenario:",
"",
"length of pendulum (L) = 1 meter, Mass of pendulum bob (m) = 0.5 kg,",
"Acceleration due to gravity (g)= 9.81 m/s2, Initial angle= 30°",
"The time period is given by: T=2π(√(L/g))",
"Substituting the values in the formula: T= 2.01 seconds",
"So, the pendulum completes one full swing in approximately 2.01 seconds.",
"The max. speed is given by: Vmax= √2gL(1-cos(\u03B8))",
"Substituting the values in the formula: Vmax= 0.67 m/s",
"Therefore, the maximum speed of the pendulum bob is approximately 0.67 m/s.",
"The initial angle is 30°",
"Throughout its motion, the pendulum will oscillate between -30° to +30° reaching",
        "different angles at different times as it swings.",
    ]

    render_text_list_info(screen, font, tutorial_text, (400, 10), BLACK, font_size=25)
    
   
    pygame.draw.rect(screen, SLIDER, back_button_rect1)
    render_text(screen, "Back", font, BLACK, (back_button_rect1.left + 25, back_button_rect1.top + 15))


    return back_button_rect1

while running:
    screen.fill(BACKGROUND_COLOR)
    
    if homepage:
        

        draw_vertical_gradient(screen, GRADIENT_COLORS)
        screen.blit(logo1, logo1_pos)
        screen.blit(logo2, logo2_pos)
        screen.blit(logo3, logo3_pos)
        
        bold_heading_text = bold_font.render("PENDULUM SIMULATION", True, BLACK)
        heading_rect = bold_heading_text.get_rect(center=(width // 2, height // 2.5))
        screen.blit(bold_heading_text, heading_rect)
        
        left_image = pygame.image.load("10.png")
        left_image = pygame.transform.scale(left_image, (350, 250)) #scaling the left img
        
        home_image = pygame.image.load("right1.png")
        home_image = pygame.transform.scale(home_image, (360, 240)) #scaling the right img  
        
        PLAY_BUTTON_COLOR = DARK_GREEN
        font_color= WHITE
        PLAY_BUTTON_HOVER_COLOR = (21, 110, 21)  
        play_button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 130, 50)
        
        play_button_color = PLAY_BUTTON_COLOR
        if play_button_rect.collidepoint(pygame.mouse.get_pos()):
            play_button_color = PLAY_BUTTON_HOVER_COLOR
            font_color= BLACK
           
          
        pygame.draw.rect(screen, play_button_color, play_button_rect)
        play_text = font.render("PLAY", True, font_color)
        text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, text_rect)
     
        left_image_rect = left_image.get_rect(left=150, centery=play_button_rect.centery+170) #left image
        screen.blit(left_image, left_image_rect)
        
        image_rect = home_image.get_rect(right=width - 50, centery=play_button_rect.centery+160) # right img
        screen.blit(home_image, image_rect)
        
    
        TUTORIAL_BUTTON_COLOR = CARROT
        font_color1= WHITE
        TUTORIAL_BUTTON_HOVER_COLOR = (185, 40, 28) 
        tutorial_button_rect = pygame.Rect(width // 2 - 50, height // 2 + 50, 130, 50)
        tutorial_button_color = TUTORIAL_BUTTON_COLOR
        if tutorial_button_rect.collidepoint(pygame.mouse.get_pos()):
            tutorial_button_color = TUTORIAL_BUTTON_HOVER_COLOR
            font_color1=BLACK
        pygame.draw.rect(screen, tutorial_button_color, tutorial_button_rect)
        tutorial_text = font.render("TUTORIAL", True, font_color1)
        text_rect = tutorial_text.get_rect(center= tutorial_button_rect.center)
        screen.blit(tutorial_text, text_rect)

        back_button_rect1 = pygame.Rect(100, 600, 100, 50)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    homepage = False 
                elif tutorial_button_rect.collidepoint(event.pos):
                    tutorial_window_open = True 
                elif back_button_rect1.collidepoint(event.pos):
                    tutorial_window_open = False
                    homepage = True

        if tutorial_window_open:
                show_tutorial_window(screen) 
       

    else:
        
        draw_vertical_gradient2(screen, COLORS)

        bob_x = pivot_x + arm_length * math.sin(angle)
        bob_y = pivot_y + arm_length * math.cos(angle)
        pygame.draw.line(screen, BLACK, (pivot_x, pivot_y), (int(bob_x), int(bob_y)), 2)
        pygame.draw.circle(screen, BOB_COLOR, (int(bob_x), int(bob_y)), int(mass_radius))

        pygame.draw.rect(screen, SLIDER, length_slider)
        pygame.draw.rect(screen, SLIDER, mass_slider)
        pygame.draw.rect(screen, SLIDER, gravity_slider)
        pygame.draw.rect(screen, SLIDER, angle_slider)
        pygame.draw.circle(screen, B, (length_knob_x, length_slider.y + slider_height // 2), 10)
        pygame.draw.circle(screen, B, (mass_knob_x, mass_slider.y + slider_height // 2), 10)
        pygame.draw.circle(screen, B, (gravity_knob_x, gravity_slider.y + slider_height // 2), 10)
        pygame.draw.circle(screen, B, (angle_knob_x, angle_slider.y + slider_height // 2), 10)

        length_text = font.render("Length: " + str(round(arm_length, 2)) + " m", True, BLACK)
        mass_text = font.render("Mass: " + str(round(mass_radius, 4)) + " kg", True, BLACK)
        gravity_text = font.render("Gravity: {:.2f} m/s^2".format(gravity), True, BLACK)
        angle_text = font.render("Initial Angle: {:.2f} rad".format(angle), True, BLACK)
        
       
        screen.blit(length_text, (length_slider.x , length_slider.y - 30))
        screen.blit(mass_text, (mass_slider.x, mass_slider.y - 30))
        screen.blit(gravity_text, (gravity_slider.x, gravity_slider.y - 30))
        screen.blit(angle_text, (angle_slider.x, angle_slider.y - 30))

        info_button_rect = pygame.Rect(width - 50, 10, 40, 40)
        pygame.draw.circle(screen, SLIDER, (width - 30, 30), 20)
        info_button_text = font.render("i", True, BLACK)
        text_rect = info_button_text.get_rect(center=info_button_rect.center)
        screen.blit(info_button_text, text_rect)

        button_x, button_y = 50, 500
        button_width, button_height = 100, 50
        button_color = DARK_GREEN if running_simulation else (255, 0, 0)
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_text = "Stop" if running_simulation else "Start"
        button_surface = font.render(button_text, True, WHITE)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        text_rect = button_surface.get_rect(center=button_rect.center)
        screen.blit(button_surface, text_rect)

        reset_button_x, reset_button_y = 200, 500
        reset_button_width, reset_button_height = 100, 50
        pygame.draw.rect(screen, (0, 0, 255), (reset_button_x, reset_button_y, reset_button_width, reset_button_height))
        reset_button_text = "Reset"
        reset_button_surface = font.render(reset_button_text, True, WHITE)
        reset_button_rect = pygame.Rect(reset_button_x, reset_button_y, reset_button_width, reset_button_height)
        text_rect_reset = reset_button_surface.get_rect(center=reset_button_rect.center)
        screen.blit(reset_button_surface, text_rect_reset)
        
        #back button for home
        back_button_rect = pygame.Rect(50, 15, 100, 40)  
        back_button_text = font.render("Back", True, BLACK)
        text_rect = back_button_text.get_rect(center= back_button_rect.center)
        button_color = BACK_BUTTON 
 
        pygame.draw.rect(screen, button_color, back_button_rect)
        screen.blit(back_button_text, text_rect)

        credits_rect = pygame.Rect(1080, 600, 270, 70)  
        
        credits_gradient_colors = [
                 (189, 242, 241), 
                (176, 249, 169) 
        ]
        
        draw_linear_gradient_rect(screen, credits_rect, credits_gradient_colors)

       

        contributor_text = ["Credits:", "Content Creation: Nirupjit Kaur", "Project Mentor: Dr. Neerja Garg"]
        render_text_list(screen, credits_font, contributor_text, (1080, 600), BLACK, font_size=credits_font_size)
        

        if running_simulation:
            if arm_length != 0:
                angular_acceleration = -gravity / arm_length * math.sin(angle)
                angular_velocity += angular_acceleration
                angle += angular_velocity

            height_from_lowest_point = arm_length * (1 - math.cos(angle))
            potential_energy = mass_radius * gravity * height_from_lowest_point
            velocity = arm_length * angular_velocity
            kinetic_energy = 0.5 * mass_radius * velocity ** 2

            pe_history.append(potential_energy)
            ke_history.append(kinetic_energy)

            if len(pe_history) > history_length:
                pe_history.pop(0)
                ke_history.pop(0)

            plt.figure(figsize=(6, 2.5),facecolor='#B1F2FF')
            time = np.arange(len(pe_history))
            plt.plot(time, pe_history, color='green', label='Potential Energy')
            plt.plot(time, ke_history, color='blue', label='Kinetic Energy')
            plt.xlabel('Time (s)')
            plt.ylabel('Energy (Joules)')
            plt.title('Energy vs. Time (in secs)')
            plt.legend()
            plt.grid(True)
            plt.gca().spines['top'].set_linewidth(2)
            plt.gca().spines['left'].set_linewidth(2)
            plt.gca().spines['right'].set_linewidth(2)

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            energy_graph = pygame.image.load(buf)
          
            screen.blit(energy_graph, (450, 400))

            plt.close()

            if gravity != 0:
                time_period = 2 * math.pi * math.sqrt(arm_length / gravity)
            else:
                time_period = float('inf')

            time_period_text = font.render("Time Period: {:.2f} s".format(time_period), True, BLACK)
            max_speed_text = font.render("Max Speed: {:.2f} m/s".format(max_speed), True, BLACK)
            angle_text = font.render("Angle: {:.2f} rad".format(angle), True, BLACK)

                
            metrics_offset_x= 80
            metrics_offset_y=80
            
            
            rect_width = max(max(time_period_text.get_width(), max_speed_text.get_width(), angle_text.get_width()) + 20, 180)
            rect_height = 140
            rect_x = width - rect_width - 90
            rect_y = 120
            
           
            gradient_colors_rect = [
                  (189, 242, 241),
                (176, 249, 169)   
            ]
            
            draw_linear_gradient_rect(screen, (rect_x, rect_y, rect_width, rect_height), gradient_colors_rect)
            
            screen.blit(time_period_text, (width - time_period_text.get_width() - 20- metrics_offset_x, 50 + metrics_offset_y))
            screen.blit(max_speed_text, (width - max_speed_text.get_width() - 20 - metrics_offset_x, 100 + metrics_offset_y))
            screen.blit(angle_text, (width - angle_text.get_width() - 20- metrics_offset_x, 150 + metrics_offset_y))

            rect_width = max(max(time_period_text.get_width(), max_speed_text.get_width(), angle_text.get_width()) + 20, 180)
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if length_slider.collidepoint(event.pos) or \
                        math.hypot(event.pos[0] - length_knob_x, event.pos[1] - (length_slider.y + slider_height // 2)) <= 10:
                    dragging_length = True
                if mass_slider.collidepoint(event.pos) or \
                        math.hypot(event.pos[0] - mass_knob_x, event.pos[1] - (mass_slider.y + slider_height // 2)) <= 10:
                    dragging_mass = True
                if gravity_slider.collidepoint(event.pos) or \
                        math.hypot(event.pos[0] - gravity_knob_x, event.pos[1] - (gravity_slider.y + slider_height // 2)) <= 10:
                    dragging_gravity = True
                if angle_slider.collidepoint(event.pos) or \
                        math.hypot(event.pos[0] - angle_knob_x, event.pos[1] - (angle_slider.y + slider_height // 2)) <= 10:
                    dragging_angle = True
                if info_button_rect.collidepoint(event.pos):
                    info_window_open = not info_window_open
                if button_rect.collidepoint(event.pos):
                    running_simulation = not running_simulation
                if reset_button_rect.collidepoint(event.pos):
                    arm_length = 150
                    mass_radius = 5
                    gravity = 9.8
                    angle = math.pi / 4
                    angular_velocity = 0
                    pe_history = []
                    ke_history = []
                    max_speed = calculate_max_speed()
                    length_knob_x = initial_length_knob_x
                    mass_knob_x = initial_mass_knob_x
                    gravity_knob_x = initial_gravity_knob_x
                    angle_knob_x = initial_angle_knob_x
                if button1_rect.collidepoint(event.pos):
                    current_page = PAGE_OBJECTIVE
                elif button2_rect.collidepoint(event.pos):
                    current_page = PAGE_SCIENCE
                elif button3_rect.collidepoint(event.pos):
                    current_page = PAGE_DESCRIPTION

                if back_button_rect.collidepoint(event.pos):
                    homepage = True
               
            if event.type == pygame.MOUSEBUTTONUP:
                    dragging_length = False
                    dragging_mass = False
                    dragging_gravity = False
                    dragging_angle = False
            if event.type == pygame.MOUSEMOTION:
                if dragging_length:
                    length_knob_x = max(length_slider.x, min(event.pos[0], length_slider.x + slider_width))
                    arm_length = length_knob_x - length_slider.x
                    max_speed = calculate_max_speed()
                if dragging_mass:
                    mass_knob_x = max(mass_slider.x, min(event.pos[0], mass_slider.x + slider_width))
                    mass_radius = mass_knob_x - mass_slider.x
                if dragging_gravity:
                    gravity_knob_x = max(gravity_slider.x, min(event.pos[0], gravity_slider.x + slider_width))
                    gravity = (gravity_knob_x - gravity_slider.x) / 10
                    max_speed = calculate_max_speed()
                if dragging_angle:
                    angle_knob_x = max(angle_slider.x, min(event.pos[0], angle_slider.x + slider_width))
                    angle = (angle_knob_x - angle_slider.x) / slider_width * 2 * math.pi

        if info_window_open:
            
            pygame.draw.rect(screen, WHITE, info_window_rect)
            screen_width, screen_height = 950, 650
            gradient_rect = pygame.Rect(400, 20, screen_width, screen_height)
    
            draw_gradient_background(screen, gradient_rect, LIGHT_BLUE_START, WHITE)
                

            menu_heading_font = pygame.font.Font('arial.ttf', 30)  
            menu_heading_text = menu_heading_font.render("About the Simulation", True, BLACK)
            menu_heading_pos = (info_window_rect.x + info_window_rect.width // 2 - menu_heading_text.get_width() // 2 - 10,  info_window_rect.y + 10 )
            screen.blit(menu_heading_text, menu_heading_pos)
            
            button_text_spacing = -150
            button1_text_pos = (button1_rect.x + button1_rect.width // 2 - button1_text.get_width() // 2, button1_rect.y + button1_rect.height // 2 - button1_text.get_height() // 2)
            button2_text_pos = (button2_rect.x + button2_rect.width // 2 - button2_text.get_width() // 2, button2_rect.y + button2_rect.height // 2 - button2_text.get_height() // 2)
            button3_text_pos = (button3_rect.x + button3_rect.width // 2 - button3_text.get_width() // 2, button3_rect.y + button3_rect.height // 2 - button3_text.get_height() // 2)

            if current_page == PAGE_OBJECTIVE:
                objective_text_pos = (info_window_rect.x+ 80 , button1_rect.centery - font.get_height() // 2 + 60)
                render_text_list_info(screen, font, ["Objective:","",
                                                "The objective of this simulation is to provide an interactive ", 
                                                "platform for understanding the dynamics of a pendulum. Real-time ",
                                                "energy graphs illustrate the interplay between potential and kinetic",
                                                "energy, enhancing comprehension of energy conversion processes",
                                                "and oscillatory motion."], objective_text_pos, BLACK )
                image = pygame.image.load("11.png")  
                image = pygame.transform.scale(image, (250, 230))  
                image_pos = (info_window_rect.x + info_window_rect.width // 2 - image.get_width() // 2, objective_text_pos[1] + 200)
                screen.blit(image, image_pos)

                 
            elif current_page == PAGE_SCIENCE:
                science_text_pos = (info_window_rect.x + 80, button1_rect.centery - font.get_height() // 2 +60)
                render_text_list_info(screen, font, ["Science:", "",
                                                "The simulation employs equations derived from classical mechanics.", 
                                                "The time period of the pendulum is given by:",
                                                "T=2π(√(L/g))","where:",
                                                "T= Time period of the pendulum",
                                                "L= length of the pendulum string",
                                                "g= acceleration due to gravity", "",
                                                "The maximum speed of the pendulum is given by:",
                                                "Vmax= √2gL(1-cos(\u03B8))","where:",
                                                "Vmax= Max. speed of the pendulum",
                                                "g= acceleration due to gravity",
                                                "L= length of the pendulum string",
                                                "\u03B8 = maximum angular displacement of the pendulum from the vertical position.",
                                                     "",
                                               "The angular acceleration of the pendulum is given by:",
                                               "Angular accl= (-g/L)*\u03B8",
                                               "where:", 
                                                "g= acceleration due to gravity", "L= length of the pendulum string",
                                                "\u03B8= angular displacement of the pendulum bob from the vertical"
                                               ], science_text_pos, BLACK)
            elif current_page == PAGE_DESCRIPTION:
                description_text_pos = (info_window_rect.x + 80, button1_rect.centery - font.get_height() // 2 + 60)
                render_text_list_info(screen, font, ["Description:", "",
                                                "The simulation presents a virtual pendulum with adjustable parameters",
                                                "through an intuitive interface. Users can modify parameters such as",
                                                "length, mass, gravity, and initial angle using sliders. Real-time",
                                                "visualization of the pendulum's motion, along with energy graphs ",
                                                "depicting potential and kinetic energy, offers a comprehensive ",
                                                "understanding of its dynamics. Controls enable starting, stopping",
                                                "and resetting the simulation, providing an engaging and interactive", 
                                                "learning experience suitable for educational purposes and exploratory", 
                                                "studies in mechanics."], description_text_pos, BLACK)
                image = pygame.image.load("desc-transformed.png")  
                image = pygame.transform.scale(image, (320, 280))  
                image_pos = (info_window_rect.x + info_window_rect.width // 2 - image.get_width() // 2, objective_text_pos[1] + 250)
                screen.blit(image, image_pos)


            
            pygame.draw.rect(screen, GREY, button1_rect)
            pygame.draw.rect(screen, GREY, button2_rect)
            pygame.draw.rect(screen, GREY, button3_rect)

            screen.blit(button1_text, button1_text_pos)
            screen.blit(button2_text, button2_text_pos)
            screen.blit(button3_text, button3_text_pos)
                                          
    pygame.display.flip()
    clock.tick(60)

pygame.quit()