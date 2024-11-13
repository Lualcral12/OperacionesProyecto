from PIL import Image, ImageTk

def Interpolacion(puntos, x):
    resultado = 0.0
    n = len(puntos)
    for i in range(n):
        termino = puntos[i]
        for j in range(n):
            if j != i:
                termino *= (x - j) / (i - j)
        resultado += termino
    return resultado


def Recorrido(imagen, x, y):
    Xbase = int(x)
    Ybase = int(y)
    dx = x - Xbase
    dy = y - Ybase

    PixelesVecinos = [[[0, 0, 0] for _ in range(3)] for _ in range(3)]
    for j in range(-1, 2):
        for i in range(-1, 2):
            pixel_x = min(max(Xbase + i, 0), imagen.width - 1)
            pixel_y = min(max(Ybase + j, 0), imagen.height - 1)
            PixelesVecinos[j + 1][i + 1] = imagen.getpixel((pixel_x, pixel_y))
    
    PixelInterpolado = [0, 0, 0]
    for c in range(3): 
        ResultadoFilas = [Interpolacion([PixelesVecinos[i][k][c] for k in range(3)], dx) for i in range(3)]
        PixelInterpolado[c] = Interpolacion(ResultadoFilas, dy)
    return tuple([int(max(0, min(255, valor))) for valor in PixelInterpolado])

def AumentarResolucion(Ruta):
    ImagenOriginal = Image.open(Ruta)
    AnchoOriginal, AltoOriginal = ImagenOriginal.size
    AnchoNuevo = AnchoOriginal * 2
    AltoNuevo = AltoOriginal * 2
    ImagenInterpolada = Image.new('RGB', (AnchoNuevo, AltoNuevo))
    
    for y in range(AltoNuevo):
        for x in range(AnchoNuevo):
            Xorigen = x / 2.0
            Yorigen = y / 2.0
            ColorInterpolado = Recorrido(ImagenOriginal, Xorigen, Yorigen)
            ImagenInterpolada.putpixel((x, y), ColorInterpolado)
        print(f"% {((y*100)/AltoNuevo)}")
    return ImagenInterpolada


def CargarImagen(ruta_imagen, EtiquetaIma):
    imagen = Image.open(ruta_imagen)
    imagen.thumbnail((600, 600))  
    imagen_tk = ImageTk.PhotoImage(imagen)
    EtiquetaIma.config(image=imagen_tk)
    EtiquetaIma.image = imagen_tk 



