import platform

'''
Rapporto tra la dimensione reale del foglio A4 in
centimetri e la dimensione della finestra che permette di 
disegnare i Tag
Usato per il posizionamento degli oggetti
Ha valore 21/424
'''
REAL_RATIO = 0.0495283

'''
Returns directory containing model's files,
directory is different for windows and linux
'''
def MODEL_DIR():
    if platform.system() == "Windows":
        return "models\\"
    else:
        return "models/"

'''
Returns directory containing rune tag's files,
directory is different for windows and linux
'''
def TAG_DIR():
    if platform.system() == "Windows":
        return "runeTags\\"
    else:
        return "runeTags/"
