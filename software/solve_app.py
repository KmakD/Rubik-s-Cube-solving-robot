import tkinter as tk
from tkinter import messagebox
import cube
import kociemba
import serial
import scaner
import time

ser = serial.Serial('COM3', baudrate = 9600, timeout = 1)   # inicjacja komunikacji z mikrokontrolerem poprzez port USB

HEIGHT = 700
WIDTH = 800
FRAMES = 120

white = "#ffffff"
yellow = "#ffff00"
red = "#ff0000" 
orange = "#ffa31a"
green = "#33cc33"
blue = "#0099ff"
grey = "#cccccc"

col = white
solution_msg = ""

# funkcja umożliwiająca wybór koloru w celu konfiguracji siatki
def select(colour):
    sel.configure(bg = colour)
    global col
    col = colour
    return col

# funkcja umożliwiająca ręczną klaibrację siatki i 
# zapisująca zmieniony stan kostki w podprogramie 'cube'
def sett(index):
    global col
    
    cubie[index].configure(bg = col, activebackground = col)

    if col == white:
        state = "U"
    elif col == yellow:
        state = "D"
    elif col == red:
        state = "R"
    elif col == orange:
        state = "L"
    elif col == green:
        state = "F"
    else:
        state = "B"

    if index < 9:
        d = 0
        if index < 3 + d:
            cube.up[0][index-d] = state
        elif index < 6 + d:
            cube.up[1][index-3-d] = state
        elif index < 9 + d:
            cube.up[2][index-6-d] = state

    elif index < 18:
        d = 9
        if index < 3 + d:
            cube.left[0][index-d] = state
        elif index < 6 + d:
            cube.left[1][index-3-d] = state
        elif index < 9 + d:
            cube.left[2][index-6-d] = state

    elif index < 27:
        d = 18
        if index < 3 + d:
            cube.front[0][index-d] = state
        elif index < 6 + d:
            cube.front[1][index-3-d] = state
        elif index < 9 + d:
            cube.front[2][index-6-d] = state

    elif index < 36:
        d = 27
        if index < 3 + d:
            cube.right[0][index-d] = state
        elif index < 6 + d:
            cube.right[1][index-3-d] = state
        elif index < 9 + d:
            cube.right[2][index-6-d] = state

    elif index < 45:
        d = 36
        if index < 3 + d:
            cube.back[0][index-d] = state
        elif index < 6 + d:
            cube.back[1][index-3-d] = state
        elif index < 9 + d:
            cube.back[2][index-6-d] = state

    else:
        d = 45
        if index < 3 + d:
            cube.down[0][index-d] = state
        elif index < 6 + d:
            cube.down[1][index-3-d] = state
        elif index < 9 + d:
            cube.down[2][index-6-d] = state

# funkcja odpowiedzialna za znalezienie rozwiązania i przesłanie go do mikrokontrolera
def solve():
    global solution_msg
    cube_stt = ''

    # zamiana stanu kostki z podprogramu 'cube' na ciąg znaków
    for i in range(3):
        for j in range(3):   
            cube_stt += cube.up[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.right[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.front[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.down[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.left[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.back[i][j]

    ser.timeout = 0.001
    start_time = time.perf_counter()

    try:
        solution_msg = kociemba.solve(cube_stt) # wyznaczenie rozwiązania 
        ser.write(solution_msg.encode())        # przesłanie rozwiązania do mikrokontrolera
    except ValueError:
        print("Invalid grid")
        popup = tk.messagebox.showerror(title = "Error", message = "Invalid grid") #okno informujące w przypadku blędnej siatki
    
    solution.configure(text = solution_msg)
    
    print("Solution: " + solution_msg)   

    
    while ser.readline().decode() != "stop":
        pass

    end_time = time.perf_counter() - start_time
    tim.configure(text = "Time: {:.3f}".format(end_time))

    ser.timeout = 1


# funkcja umożliwiające przesłanie ruchów z pola 'entry' do mikrokontrolera
def scramble():
    global solution_msg

    solution_msg = scramble.get()

    ser.write(solution_msg.encode())        #przesłanie wpisanego ciągu znaków do mikrokontrolera
    print("Scramble: " + solution_msg)

# funkcja umożliwiająca skanowanie kostki
def scan():

    sides = {}
    sides = scaner.scan()   #wywołanie funkcji skanującej podprogramu 'scaner'

    # zapisanie odczytanego stanu kostki w podprogramie 'cube'
    for i in range(3):
        for j in range(3):
            cube.up[i][j] = sides['white'][j+i*3]
            cube.right[i][j] = sides['red'][j+i*3]
            cube.front[i][j] = sides['green'][j+i*3]
            cube.down[i][j] = sides['yellow'][j+i*3]
            cube.left[i][j] = sides['orange'][j+i*3]
            cube.back[i][j] = sides['blue'][j+i*3]

    # zmiana siatki zgodnie z odczytanym stanem kostki 
    k = 0
    for col in sides:

        color = white

        if col == 'white':
            k = 0
        elif col == 'orange':
            k = 1
        elif col == 'green':
            k = 2
        elif col == 'red':
            k = 3
        elif col == 'blue':
            k = 4
        else:
            k = 5

        for i in range(9):
            if sides[col][i] == 'U':
                color = white        
            elif sides[col][i] == 'R':
                color = red
            elif sides[col][i] == 'F':
                color = green        
            elif sides[col][i] == 'D':
                color = yellow
            elif sides[col][i] == 'L':
                color = orange        
            else:
                color = blue

            cubie[i + k*9].configure(bg = color, activebackground = color)

    reverse() # wywołanie funkcji wyznaczającej algorytm mieszający

# funkcja wyznaczająca algorytm mieszający poprzez odwrócenie algorytmu układającego
def reverse():

    cube_stt = ''
    sol = ''
    scr = ''

    # zamiana stanu kostki z podprogramu 'cube' na ciąg znaków
    for i in range(3):
        for j in range(3):   
            cube_stt += cube.up[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.right[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.front[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.down[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.left[i][j]

    for i in range(3):
        for j in range(3):   
            cube_stt += cube.back[i][j]
        
    try:
        sol = kociemba.solve(cube_stt) #wyznaczenie rozwiązania kostki 
    except ValueError:
        print("Invalid grid")
        popup = tk.messagebox.showerror(title = "Error", message = "Invalid grid")
    
    # odwrócenie znalezionego rozwiązania
    for i in range(1,len(sol) + 1):
        if sol[len(sol)-i] == 'R' or sol[len(sol)-i] == 'L' or sol[len(sol)-i] == 'U' or sol[len(sol)-i] == 'D' or sol[len(sol)-i] == 'F' or sol[len(sol)-i] == 'B':
            if i != 1:
                if sol[len(sol)-i + 1] == '\'':
                    scr += sol[len(sol)-i] + ' '
                elif sol[len(sol)-i + 1] == '2':
                    scr += sol[len(sol)-i] + '2 '
                else:
                    scr += sol[len(sol)-i] + '\' '
            elif sol[len(sol)-i] == 'R' or sol[len(sol)-i] == 'L' or sol[len(sol)-i] == 'U' or sol[len(sol)-i] == 'D' or sol[len(sol)-i] == 'F' or sol[len(sol)-i] == 'B':
                scr += sol[len(sol)-i] + '\' '
                

    scramble.delete(0, tk.END)
    scramble.insert(0,scr)

root = tk.Tk()  # utworzenie okna aplikacji

# utworzenie oraz umieszczenie ram w oknie aplikacji
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)    
canvas.pack()

panel = tk.Frame(root, bg = "grey", width = FRAMES, height = 3*FRAMES)
panel.place(x = 100 + 4*FRAMES, y = 50)

color_select = tk.Frame(panel, bg = "grey")
color_select.place(relx = 0.05, rely = 0.38, relwidth = 0.9, relheight = 0.6)

cube_grid = tk.Frame(root, bg ="grey", width = 4*FRAMES, height = 3*FRAMES)
cube_grid.place(x = 50, y = 50)

solution_frame = tk.Frame(root, bg = "grey", width = 4*FRAMES, height = 1.5*FRAMES)
solution_frame.place(x = 50, y = 100 + 3*FRAMES)

# ramy siatki
white_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
white_frame.grid(row = 0, column = 1)
orange_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
orange_frame.grid(row = 1, column = 0)
green_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
green_frame.grid(row = 1, column = 1)
red_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
red_frame.grid(row = 1, column = 2)
blue_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
blue_frame.grid(row = 1, column = 3)
yellow_frame = tk.Frame(cube_grid, bg = "grey", width = FRAMES, height = FRAMES)
yellow_frame.grid(row = 2, column = 1)

# utworzenie elementów siatki kostki
cubie = [
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(0)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(1)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(2)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(3)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(5)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(6)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(7)),
    tk.Button(white_frame, bg = white, bd = 0, activebackground = white, command = lambda:sett(8)),

    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(9)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(10)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(11)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(12)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(14)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(15)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(16)),
    tk.Button(orange_frame, bg = orange, bd = 0, activebackground = orange, command = lambda:sett(17)),

    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(18)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(19)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(20)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(21)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(23)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(24)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(25)),
    tk.Button(green_frame, bg = green, bd = 0, activebackground = green, command = lambda:sett(26)),

    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(27)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(28)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(29)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(30)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(32)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(33)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(34)),
    tk.Button(red_frame, bg = red, bd = 0, activebackground = red, command = lambda:sett(35)),

    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(36)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(37)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(38)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(39)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(41)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(42)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(43)),
    tk.Button(blue_frame, bg = blue, bd = 0, activebackground = blue, command = lambda:sett(44)),

    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(45)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(46)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(47)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(48)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(50)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(51)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(52)),
    tk.Button(yellow_frame, bg = yellow, bd = 0, activebackground = yellow, command = lambda:sett(53)),    
]

# zdefiniowanie i umieszczenie przycisków pozwalających na wybór koloru konfiguracji siatki
button0 = tk.Button(color_select, bg = white, bd = 0, command = lambda:select(white))
button1 = tk.Button(color_select, bg = yellow, bd = 0, command = lambda:select(yellow))
button2 = tk.Button(color_select, bg = red, bd = 0, command = lambda:select(red))
button3 = tk.Button(color_select, bg = orange, bd = 0, command = lambda:select(orange))
button4 = tk.Button(color_select, bg = blue, bd = 0, command = lambda:select(blue))
button5 = tk.Button(color_select, bg = green, bd = 0, command = lambda:select(green))
sel = tk.Frame(color_select, bg = white)


button0.place(relx = 0.05, rely = 0.025, relwidth = 0.42, relheight = 0.21)
button1.place(relx = 0.52, rely = 0.025, relwidth = 0.42, relheight = 0.21)
button2.place(relx = 0.05, rely = 0.26, relwidth = 0.42, relheight = 0.21)
button3.place(relx = 0.52, rely = 0.26, relwidth = 0.42, relheight = 0.21)
button4.place(relx = 0.05, rely = 0.495, relwidth = 0.42, relheight = 0.21)
button5.place(relx = 0.52, rely = 0.495, relwidth = 0.42, relheight = 0.21)
sel.place(relx = 0.25, rely = 0.73, relwidth = 0.5, relheight = 0.25)

# umieszczenie siatki w oknie aplikacji
for i in range(3):
    for j in range(3):
        cubie[j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)
        cubie[9 + j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)
        cubie[18 + j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)
        cubie[27 + j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)
        cubie[36 + j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)
        cubie[45 + j+3*i].place(relx = 0.04 + j*0.32, rely = 0.04 + i*0.32, relheight = 0.28, relwidth = 0.28)      #add 0.28+0.04 = 0,32

# zdefiniowanie i umieszczenie przycisków
solve_button = tk.Button(panel, command = solve, text = "Solve", font = "times 14")
solve_button.place(relx = 0.05, rely = 0.02, relwidth = 0.9, height = 30)
scramble_button = tk.Button(panel, command = scramble, text = "Scramble", font = "times 14")
scramble_button.place(relx = 0.05, rely = 0.14, relwidth = 0.9, height = 30)
scan_button = tk.Button(panel, command = scan, text = "Scan", font = "times 14")
scan_button.place(relx = 0.05, rely = 0.26, relwidth = 0.9, height = 30)

# zdefiniowanie i umieszczenie pola 'entry' oraz etykiet
scramble = tk.Entry(solution_frame, font = "times 12")
scramble_txt = tk.Label(solution_frame, text = "Enter moves", bg = "grey", font = "times 16")
solution = tk.Label(solution_frame, text = "Solution", font = "times 12")
solution_txt = tk.Label(solution_frame, bg = "grey", text = "Solution", font = "times 16")
tim = tk.Label(solution_frame, bg = "grey", text = "Time: 0:000", font = "times 20")

scramble.place(relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.15)
scramble_txt.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.15)
solution.place(relx = 0.05, rely = 0.55, relwidth = 0.9, relheight = 0.15)
solution_txt.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.15)
tim.place(relx = 0.05, rely = 0.8, relwidth = 0.9, relheight = 0.2)

root.mainloop()