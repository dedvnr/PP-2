import pygame
import datetime
import tools 

UI_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_BG = (220, 220, 220)
UI_TEXT_COL = (40, 40, 40)
ACTIVE_ICON_HIGHLIGHT = (0, 0, 255)

S_SIZE, M_SIZE, L_SIZE = 2, 5, 10

def create_pixel_icon(name, color):
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    surf.fill((255, 255, 255, 0))

    if name == 'pencil':
        pygame.draw.rect(surf, (139, 69, 19), (5, 5, 20, 10)) 
        pygame.draw.line(surf, color, (0, 25), (30, 25), 2) 
    elif name == 'eraser':
        pygame.draw.rect(surf, (255, 182, 193), (5, 5, 20, 20), border_radius=3)
        pygame.draw.rect(surf, WHITE, (10, 10, 10, 10))
    elif name == 'fill':
        pygame.draw.rect(surf, (105, 105, 105), (5, 5, 20, 20))
        pygame.draw.circle(surf, color, (15, 10), 8) 
    elif name == 'text':
        font_A = pygame.font.SysFont("arial", 28, bold=True)
        A_txt = font_A.render("A", True, BLACK)
        surf.blit(A_txt, (3, 0))
        pygame.draw.line(surf, BLACK, (22, 2), (22, 28), 2) 
    elif name == 'rect': pygame.draw.rect(surf, color, (3, 3, 24, 24), 3)
    elif name == 'circle': pygame.draw.circle(surf, color, (15, 15), 12, 3)
    elif name == 'line': pygame.draw.line(surf, color, (3, 3), (27, 27), 3)
    elif name == 'rhombus': 
        points = [(15, 3), (27, 15), (15, 27), (3, 15)]
        pygame.draw.polygon(surf, color, points, 3)
    elif name == 'equi_tri': 
        points = [(15, 3), (27, 24), (3, 24)]
        pygame.draw.polygon(surf, color, points, 3)
    elif name == 'right_tri':
        points = [(3, 3), (3, 27), (27, 27)]
        pygame.draw.polygon(surf, color, points, 3)
    
    return surf

def draw_ui_panel(screen, font, current_color, active_mode, current_thickness, icons):
    pygame.draw.rect(screen, GRAY_BG, (0, 0, 800, UI_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, UI_HEIGHT-1), (800, UI_HEIGHT-1), 1)

    colors = {
        "black": BLACK, "red": (255, 0, 0), "green": (0, 255, 0),
        "blue": (0, 0, 255), "yellow": (255, 255, 0), "purple": (128, 0, 128)
    }
    y_col = 15
    x_col_start = 20
    for name, col in colors.items():
        box_rect = pygame.Rect(x_col_start, y_col, 30, 30)
        pygame.draw.rect(screen, col, box_rect)
        if col == current_color: 
            pygame.draw.rect(screen, BLACK, box_rect, 3)
        x_col_start += 40

    size_btn_width = 70
    x_size_start = 20
    sizes = [(S_SIZE, "Small"), (M_SIZE, "Medium"), (L_SIZE, "Large")]
    
    lbl_s = font.render(f"SIZES:", True, UI_TEXT_COL)
    screen.blit(lbl_s, (x_size_start, 60))
    x_size_start += 60

    for idx, (sz, lbl) in enumerate(sizes):
        s_rect = pygame.Rect(x_size_start, 55, size_btn_width, 30)
        btn_col = (180, 180, 180) if sz != current_thickness else (140, 140, 200)
        pygame.draw.rect(screen, btn_col, s_rect, border_radius=4)
        
        s_txt = font.render(f"{lbl}", True, UI_TEXT_COL)
        tx = s_rect.x + (size_btn_width - s_txt.get_width()) // 2
        screen.blit(s_txt, (tx, 60))
        x_size_start += size_btn_width + 10

    tool_buttons_render_data = [
        (330, 15, 'pencil', 'P'), (365, 15, 'eraser', 'E'), (400, 15, 'fill', 'F'), (435, 15, 'text', 'T'),
        (480, 15, 'line', 'L'),   (515, 15, 'rect', 'R'),   (550, 15, 'circle', 'C'), (585, 15, 'square', 'S'),
        (620, 15, 'rhombus', 'H'), (655, 15, 'equi_tri', 'Q'), (690, 15, 'right_tri', 'W')
    ]
    
    font_hotkey = pygame.font.SysFont("arial", 12, bold=True)
    
    for bx, by, bmode, hkey in tool_buttons_render_data:
        icon_surf = icons[bmode]
        screen.blit(icon_surf, (bx, by))
        
        if bmode == active_mode:
            pygame.draw.rect(screen, ACTIVE_ICON_HIGHLIGHT, (bx-2, by-2, 34, 34), 2)

        h_txt = font_hotkey.render(f"{hkey}", True, ACTIVE_ICON_HIGHLIGHT if bmode == active_mode else (80, 80, 80))
        tx = bx + (icon_surf.get_width() - h_txt.get_width()) // 2
        screen.blit(h_txt, (tx, by + 34))

    info_txt_1 = font.render(f"ACTIVE: {active_mode.upper()} ({current_thickness}px)", True, UI_TEXT_COL)
    info_txt_2 = font.render("Use 1, 2, 3 to change Size | Ctrl+S to Save", True, (60, 60, 60))
    screen.blit(info_txt_1, (630, 75))
    screen.blit(info_txt_2, (330, 75))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Пэйнт")
    
    font_main = pygame.font.SysFont("arial", 16)
    
    canvas = pygame.Surface((800, 600)).convert_alpha()
    canvas.fill(WHITE)
    
    mode = 'pencil' 
    current_color = BLACK
    thickness = M_SIZE 
    start_pos = None
    last_pos = None
    
    text_input, text_pos, is_typing = "", None, False

    icons = {}
    icon_list = ['pencil', 'eraser', 'fill', 'text', 'line',
                 'rect', 'circle', 'square', 'rhombus', 'equi_tri', 'right_tri']
    
    try:
        for name in icon_list:
            img = pygame.image.load(f'assets/{name}.png').convert_alpha()
            icons[name] = pygame.transform.scale(img, (30, 30))
    except FileNotFoundError:
        print(f"Error: Missing one or more icons in 'assets/'. Creating fallbacks.")
        icons = {}
        icon_list_programmatic = ['pencil', 'eraser', 'fill', 'text', 'rect', 'circle', 'line', 'rhombus', 'equi_tri', 'right_tri']
        for name in icon_list_programmatic:
            icons[name] = create_pixel_icon(name, BLACK) 

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if is_typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        canvas.blit(font_main.render(text_input, True, current_color), text_pos)
                        is_typing = False
                    elif event.key == pygame.K_ESCAPE: is_typing = False
                    elif event.key == pygame.K_BACKSPACE: text_input = text_input[:-1]
                    else: text_input += event.unicode
                continue 

            if event.type == pygame.KEYDOWN:
                modes = {pygame.K_p: 'pencil', pygame.K_l: 'line', pygame.K_r: 'rect', 
                         pygame.K_c: 'circle', pygame.K_s: 'square', pygame.K_h: 'rhombus', 
                         pygame.K_q: 'equi_tri', pygame.K_w: 'right_tri', 
                         pygame.K_f: 'fill', pygame.K_t: 'text', pygame.K_e: 'eraser'}
                if event.key in modes: mode = modes[event.key]

                if event.key == pygame.K_1: thickness = S_SIZE
                if event.key == pygame.K_2: thickness = M_SIZE
                if event.key == pygame.K_3: thickness = L_SIZE
                
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"assets/painting_{now}.png"
                    try:
                        pygame.image.save(canvas, filename)
                        print(f"Canvas saved inside assets/ as painting_{now}.png")
                    except:
                        pygame.image.save(canvas, f"painting_{now}.png")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[1] > UI_HEIGHT: 
                    if mode == 'fill': 
                        tools.flood_fill(canvas, mouse_pos[0], mouse_pos[1], current_color)
                    elif mode == 'text': 
                        text_pos, is_typing, text_input = mouse_pos, True, ""
                    else: start_pos = last_pos = mouse_pos
                        
                else: 
                    if 15 <= mouse_pos[1] <= 45:
                        for i in range(6): 
                            if pygame.Rect(20 + i * 40, 15, 30, 30).collidepoint(mouse_pos):
                                current_color = list(color_definitions.values())[i]
                    
                    if 55 <= mouse_pos[1] <= 85:
                        szs = [S_SIZE, M_SIZE, L_SIZE]
                        btn_width = 70
                        for idx in range(3):
                            s_rect = pygame.Rect(80 + idx * (btn_width + 10), 55, btn_width, 30)
                            if s_rect.collidepoint(mouse_pos):
                                thickness = szs[idx]

                    for bx, by, bmode, hkey in tool_buttons_full_data:
                        if pygame.Rect(bx, by, 30, 30).collidepoint(mouse_pos):
                            mode = bmode
                            start_pos = None

            if event.type == pygame.MOUSEBUTTONUP:
                if start_pos:
                    args = (canvas, current_color, start_pos, mouse_pos, thickness)
                    if mode == 'line': pygame.draw.line(*args) 
                    elif mode == 'rect': tools.draw_rect(*args)
                    elif mode == 'circle': tools.draw_circle(*args)
                    elif mode == 'square': tools.draw_square(*args)
                    elif mode == 'equi_tri': tools.draw_equi_tri(*args)
                    elif mode == 'right_tri': tools.draw_right_tri(*args)
                    elif mode == 'rhombus': tools.draw_rhombus(*args)
                    
                    start_pos = None 

        if pygame.mouse.get_pressed()[0] and mouse_pos[1] > UI_HEIGHT:
            if mode == 'pencil':
                pygame.draw.line(canvas, current_color, last_pos, mouse_pos, thickness)
                last_pos = mouse_pos 
            elif mode == 'eraser':
                pygame.draw.circle(canvas, WHITE, mouse_pos, thickness * 5)

        screen.blit(canvas, (0, 0))
        
        if start_pos and mouse_pos[1] > UI_HEIGHT:
            args = (screen, current_color, start_pos, mouse_pos, thickness)
            if mode == 'line': pygame.draw.line(*args) 
            elif mode == 'rect': tools.draw_rect(*args)
            elif mode == 'circle': tools.draw_circle(*args)
            elif mode == 'square': tools.draw_square(*args)
            elif mode == 'equi_tri': tools.draw_equi_tri(*args)
            elif mode == 'right_tri': tools.draw_right_tri(*args)
            elif mode == 'rhombus': tools.draw_rhombus(*args)

        if is_typing:
            cursor_blink = "|" if pygame.time.get_ticks() % 1000 < 500 else " "
            txt_preview = font_main.render(text_input + cursor_blink, True, current_color)
            screen.blit(txt_preview, text_pos)
        
        draw_ui_panel(screen, font_main, current_color, mode, thickness, icons)
        
        pygame.display.flip()
        clock.tick(120)

tool_buttons_full_data = [
    (330, 15, 'pencil', 'P'), (365, 15, 'eraser', 'E'), (400, 15, 'fill', 'F'), (435, 15, 'text', 'T'),
    (480, 15, 'line', 'L'),   (515, 15, 'rect', 'R'),   (550, 15, 'circle', 'C'), (585, 15, 'square', 'S'),
    (620, 15, 'rhombus', 'H'), (655, 15, 'equi_tri', 'Q'), (690, 15, 'right_tri', 'W')
]
color_definitions = {
    "black": BLACK, "red": (255, 0, 0), "green": (0, 255, 0),
    "blue": (0, 0, 255), "yellow": (255, 255, 0), "purple": (128, 0, 128)
}

if __name__ == "__main__":
    main()