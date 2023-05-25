import os
import cv2
import face_recognition
from datetime import datetime
import sqlite3

def connect_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c

def create_table():
    conn, c = connect_database()
    c.execute('''CREATE TABLE IF NOT EXISTS frames
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 frame BLOB,
                 timestamp TEXT)''')

def reconhecimento_facial():
    # Diretório contendo as imagens de treinamento
    diretorio_treinamento = "img"

    # Carregar as imagens de treinamento
    imagens_treinamento = []
    nomes_treinamento = []
    for nome_arquivo in os.listdir(diretorio_treinamento):
        caminho_imagem = os.path.join(diretorio_treinamento, nome_arquivo)
        imagem = face_recognition.load_image_file(caminho_imagem)
        encoding = face_recognition.face_encodings(imagem)
        if len(encoding) > 0:
            imagens_treinamento.append(encoding[0])
            nomes_treinamento.append(os.path.splitext(nome_arquivo)[0])
        else:
            print(f"Não foi possível detectar rosto na imagem {nome_arquivo}")

    # Inicializar a webcam
    video_capture = cv2.VideoCapture(0)

    # Connect to the SQLite database
    conn, c = connect_database()

    # Create table if it doesn't exist
    create_table()

    while True:
        # Capturar um frame da webcam
        ret, frame = video_capture.read()

        # Converter o frame para RGB (a biblioteca face_recognition usa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encontrar os rostos no frame capturado
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Iterar sobre os rostos encontrados
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Comparar o rosto com as imagens de treinamento
            matches = face_recognition.compare_faces(imagens_treinamento, face_encoding)

            # Verificar se há uma correspondência
            nome = "Desconhecido"
            if True in matches:
                index = matches.index(True)
                nome = nomes_treinamento[index]

            # Desenhar um retângulo e exibir o nome do rosto reconhecido
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, nome, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Obter a data e hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Adicionar a data e hora na imagem
        cv2.putText(frame, data_hora, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Salvar a imagem quando a tecla para fechar a câmera for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            nome_imagem = f'{nome}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.jpg'
            cv2.imwrite(nome_imagem, frame)
            print(f"Imagem salva como {nome_imagem}")

            # Save the frame to the SQLite database
            with open(nome_imagem, 'rb') as image_file:
                img_data = image_file.read()
                c.execute("INSERT INTO frames (frame, timestamp) VALUES (?, ?)", (sqlite3.Binary(img_data), data_hora))
                conn.commit()

            # Remove the image file
            os.remove(nome_imagem)
            break

        # Exibir o frame resultante
        cv2.imshow('Video', frame)

        # Parar o loop se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar os recursos
    video_capture.release()
    cv2.destroyAllWindows()
    conn.close()

# Chamada da função para executar o reconhecimento facial
reconhecimento_facial()
