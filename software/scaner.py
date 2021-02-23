import cv2
import numpy as np


def empty_callback(x):
    pass
           
color_RGB = {
    'red'    : (0,0,255),
    'orange' : (0,165,255),
    'blue'   : (255,0,0),
    'green'  : (0,255,0),
    'white'  : (255,255,255),
    'yellow' : (0,255,255)
}


square_pos = [
    [200, 150], [300, 150], [400, 150],
    [200, 250], [300, 250], [400, 250],
    [200, 350], [300, 350], [400, 350]
]

sticker_pos = [
    [20, 20], [54, 20], [88, 20],
    [20, 54], [54, 54], [88, 54],
    [20, 88], [54, 88], [88, 88]
]

scaned_pos = [
    [20, 130], [54, 130], [88, 130],
    [20, 164], [54, 164], [88, 164],
    [20, 198], [54, 198], [88, 198]   
]

colors_hsv = {
    'white':[[150,86,255],[62,0,40]],
    'yellow':[[72,255,255],[23,50,52]],
    'red':[[172,255,255],[11,154,0]],
    'orange':[[172,168,255],[18,62,198]],
    'green':[[98,255,255],[63,150,0]],
    'blue':[[118,255,255],[89,178,51]]
}

color = ['white','yellow','red','orange','green','blue']

# funkcja wyświetlająca kwadraty definiujące obszary skanowania
def draw_squares(frame):
    for i,(x,y) in enumerate(square_pos):
        cv2.rectangle(frame, (x,y), (x+30, y+30), (255, 255, 255), 2)

# funkcja wyświetlająca aktualnie odczytywane kolory
def draw_stickers(frame, state):
    for i,(x,y) in enumerate(sticker_pos):
        cv2.rectangle(frame, (x,y), (x+32,y+32), color_RGB[state[i]], -1)

# funkcja wyświetlająca zeskanowane kolory
def draw_scaned(frame, state):
    for i,(x,y) in enumerate(scaned_pos):
        cv2.rectangle(frame, (x,y), (x+32,y+32), color_RGB[state[i]], -1)

# funkcja sprawdzająca kolor na podstawie wartości HSV
def color_detect(h,s,v,colors):
    for col in colors:
        if col == 'red' or col == 'orange':
                if (h <= colors[col][1][0] or h >= colors[col][0][0]) and s in range(colors[col][1][1],colors[col][0][1]+1) and v in range(colors[col][1][2],colors[col][0][2]+1):
                    return col            
        elif h in range(colors[col][1][0],colors[col][0][0]+1) and s in range(colors[col][1][1],colors[col][0][1]+1) and v in range(colors[col][1][2],colors[col][0][2]+1):
            return col

    return "white"

# funkcja zamieniająca nazwy kolorów na ich symbole
def convert(sides):

    for col in sides:
        for i in range(9):
            if sides[col][i] == 'white':
                sides[col][i] = 'U'
            elif sides[col][i] == 'yellow':
                sides[col][i] = 'D'
            elif sides[col][i] == 'red':
                sides[col][i] = 'R'
            elif sides[col][i] == 'orange':
                sides[col][i] = 'L'
            elif sides[col][i] == 'green':
                sides[col][i] = 'F'
            elif sides[col][i] == 'blue':
                sides[col][i] = 'B'

    return sides
            
# funkcja odpowiedzailna za skanowanie kostki
def scan():
    cam_port = 1
    cam = cv2.VideoCapture(cam_port)    # inicjacja odczytywania obrazu z kamery

    sides = {}

    state   = [ 'white','white','white',
            'white','white','white',
            'white','white','white']

    scaned_state   = [ 'white','white','white',
            'white','white','white',
            'white','white','white']

    cv2.namedWindow('scan', 0)          # utworzenie okna skanowania
    cv2.resizeWindow('scan', 700, 800)

    # utworzenie suwaków 
    cv2.createTrackbar('H lower','scan',colors_hsv["white"][1][0],179, empty_callback)
    cv2.createTrackbar('S lower', 'scan',colors_hsv["white"][1][1],255, empty_callback)
    cv2.createTrackbar('V lower', 'scan',colors_hsv["white"][1][2],255, empty_callback)

    cv2.createTrackbar('H upper','scan',colors_hsv["white"][0][0],179, empty_callback)
    cv2.createTrackbar('S upper', 'scan',colors_hsv["white"][0][1],255, empty_callback)
    cv2.createTrackbar('V upper', 'scan',colors_hsv["white"][0][2],255, empty_callback)

    while len(sides) < 6:

        _, frame = cam.read()                               # odczytanie obrazu z kamer    
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # zamiana kolorów na barwy w modelu HSV
        key = cv2.waitKey(10)                               

        hsv = []

        draw_squares(frame)
        draw_scaned(frame, scaned_state)
        
        # odczytanie średnich wartości HSV ze skanowanych pól
        for i in range(9):
            sum_h = [0,0,0]
            x = [0,0,0]
            avg = [0,0,0]
            for j in range(20):
                for k in range(20):
                    x = hsv_frame[square_pos[i][1]+5+j][square_pos[i][0]+5+k]
                    sum_h[0] = sum_h[0] + x[0]
                    sum_h[1] = sum_h[1] + x[1]
                    sum_h[2] = sum_h[2] + x[2]

            avg[0] = round(sum_h[0]/400)
            avg[1] = round(sum_h[1]/400)
            avg[2] = round(sum_h[2]/400)
            hsv.append(avg)

        # odczytanie kolorów ze skanowanych pól
        for i,(x,y) in enumerate(sticker_pos):
            color_name = color_detect(hsv[i][0], hsv[i][1], hsv[i][2], colors_hsv)
            state[i] = color_name
    
        draw_stickers(frame, state)

        # zapisanie aktualnych kolorów przyciskiem 'spacja'
        if key == 32:
            scaned_state = list(state)
            face = state[4]
            sides[face] = list(state)

        text = 'Scaned sides {}/6'.format(len(sides))
        cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        
        cv2.imshow("scan", frame) # wyświetlenie obrazu z kamery

        # przerwanie kalibracji przyciskiem 'backspace'
        if key == 27:
            break

        # kalibracja wartości granicznych HSV poszczególnych kolorów 
        # uruchamiana przyciskiem 'enter'
        if key == 13:
            i = 0

            while i < 6:
                _, frame = cam.read()                               # odczytanie obrazu z kamer 
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # zamiana kolorów na barwy w modelu HSV
                key = cv2.waitKey(10) & 0xff

                # odczytanie wartości granicznych HSV z suwaków
                h_lower = cv2.getTrackbarPos('H lower', 'scan')
                h_upper = cv2.getTrackbarPos('H upper', 'scan')
                s_lower = cv2.getTrackbarPos('S lower', 'scan')
                s_upper = cv2.getTrackbarPos('S upper', 'scan')
                v_lower = cv2.getTrackbarPos('V lower', 'scan')
                v_upper = cv2.getTrackbarPos('V upper', 'scan')

                # utworzenie maski dla kolorów czerwonego i pomarańczowego
                if color[i] == 'red' or color[i] == 'orange':
                    lower = np.array([0, s_lower, v_lower])
                    upper = np.array([h_lower, s_upper, v_upper])
                    mask1 = cv2.inRange(hsv_frame, lower, upper)
                    lower = np.array([s_upper, s_lower, v_lower])
                    upper = np.array([179, s_upper, v_upper])
                    mask2 = cv2.inRange(hsv_frame, lower, upper)
                    mask = cv2.bitwise_or(mask1, mask2)
                    con = cv2.bitwise_and(frame,frame, mask = mask)
                    lower = np.array([h_lower, s_lower, v_lower])
                    upper = np.array([h_upper, s_upper, v_upper])

                # utworzenie maski dla pozostałych kolorów
                else:
                    lower = np.array([h_lower, s_lower, v_lower])
                    upper = np.array([h_upper, s_upper, v_upper])

                    mask = cv2.inRange(hsv_frame, lower, upper)
                    con = cv2.bitwise_and(frame,frame, mask = mask)

                # przejście do kalibracji następnego koloru po wciśnięciu spacji
                if key == 32:
                    colors_hsv[color[i]] = [upper, lower]
                    i+= 1

                    if(i < 6):
                        cv2.setTrackbarPos('H upper','scan',colors_hsv[color[i]][0][0])
                        cv2.setTrackbarPos('S upper','scan',colors_hsv[color[i]][0][1])
                        cv2.setTrackbarPos('V upper','scan',colors_hsv[color[i]][0][2])
                        cv2.setTrackbarPos('H lower','scan',colors_hsv[color[i]][1][0])
                        cv2.setTrackbarPos('S lower','scan',colors_hsv[color[i]][1][1])
                        cv2.setTrackbarPos('V lower','scan',colors_hsv[color[i]][1][2])

                if(i < 6):
                    cv2.putText(con, color[i], (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

                cv2.imshow("scan", con) # wyświetlenie obrazu z kamery wraz z maską

                # przerwanie kalibracji przyciskiem 'backspace'
                if key == 27:
                    break

    cam.release()
    cv2.destroyAllWindows()
    sides = convert(sides)
    return sides

#scan() #linia służaca do testowania programu