import os
import sqlite3
import cv2

def retrieve_frames_from_database():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Recuperar todos os quadros da tabela 'frames'
    c.execute("SELECT frame FROM frames")
    resultados = c.fetchall()
    for resultado in resultados:
        frame_data = resultado[0]

        # Criar um arquivo de imagem temporário
        temp_image_file = 'temp_frame.jpg'
        with open(temp_image_file, 'wb') as image_file:
            image_file.write(frame_data)

        # Ler a imagem usando o OpenCV
        frame = cv2.imread(temp_image_file)

        # Exibir ou processar o quadro conforme necessário
        cv2.imshow('Quadro', frame)
        cv2.waitKey(0)

        # Remover o arquivo de imagem temporário
        os.remove(temp_image_file)

    # Fechar a conexão com o banco de dados
    conn.close()

# Chamar a função para recuperar e exibir todos os quadros do banco de dados
retrieve_frames_from_database()
