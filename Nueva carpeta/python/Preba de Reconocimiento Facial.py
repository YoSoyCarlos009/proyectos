import face_recognition
import cv2
import os
import pickle

# Archivo para guardar los datos de rostros
DATA_FILE = "face_data.pkl"

def load_face_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            return pickle.load(file)
    return {}

def save_face_data(data):
    with open(DATA_FILE, "wb") as file:
        pickle.dump(data, file)

def register_face(face_data):
    video_capture = cv2.VideoCapture(0)
    
    print("Presiona 'q' para salir del programa.")
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error al capturar video.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = input("Ingrese su nombre: ")
                face_data[name] = face_encoding
                save_face_data(face_data)
                print(f"Rostro de {name} guardado.")
                video_capture.release()
                return
        else:
            cv2.putText(frame, "No se detecto ningun rostro", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Registro de Rostro', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def recognize_face(face_data):
    video_capture = cv2.VideoCapture(0)
    
    print("Presiona 'q' para salir del programa.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error al capturar video.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Desconocido"
                matches = face_recognition.compare_faces(list(face_data.values()), face_encoding)

                if True in matches:
                    first_match_index = matches.index(True)
                    name = list(face_data.keys())[first_match_index]
                else:
                    name = "Usuario no reconocido"

                # Dibujar el rectángulo y el nombre
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.75, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "No se detecto ningun rostro", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Reconocimiento de Rostro', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def main():
    face_data = load_face_data()

    while True:
        choice = input("¿Quieres agregar un rostro nuevo o detectar un rostro existente? (agregar/detectar/salir): ").strip().lower()
        if choice == 'agregar':
            register_face(face_data)
        elif choice == 'detectar':
            recognize_face(face_data)
        elif choice == 'salir':
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if _name_ == "_main_":
    main()
