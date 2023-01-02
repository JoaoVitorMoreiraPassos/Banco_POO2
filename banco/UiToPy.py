import os

def convert():
    arqs = os.listdir('./ui')
    arqs = [arq for arq in arqs if arq.endswith('.ui')]
    for i in arqs:
        os.system('pyuic5 ./ui/%s -o ./screens/%s.py' % (i, i[2:-3]))
        print(f"arquivo {i[2:-3]}.py convertido com sucesso!")
    
