import cv2
import face_recognition
import numpy as np
import os
import pickle

# Cargar datos de rostros guardados
def load_face_data():
    if os.path.exists("face_data.pkl"):
        with open("face_data.pkl", "rb") as f:
            return pickle.load(f)
    return {}

# Guardar datos de rostros
def save_face_data(face_data):
    with open("face_data.pkl", "wb") as f:
        pickle.dump(face_data, f)

# Registrar un nuevo rostro
def register_face(face_data):
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error al abrir la cámara.")
        return

    print("Escaneando rostro... Presiona 'q' para salir del registro.")

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) > 0:
            for face_location in face_locations:
                top, right, bottom, left = face_location

                # Usa la imagen completa y la ubicación del rostro
                face_encodings = face_recognition.face_encodings(rgb_frame, [face_location])
                
                if len(face_encodings) > 0:
                    name = input("Ingrese su nombre para guardar el rostro: ")
                    face_data[name] = face_encodings[0]  # Guardar solo la primera codificación
                    save_face_data(face_data)
                    print(f"Rostro de {name} guardado.")
                    capture.release()
                    cv2.destroyAllWindows()
                    return

        cv2.putText(frame, "Escaneando rostro...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.imshow("Registro de Rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

# Detectar un rostro existente
def recognize_face(face_data):
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error al abrir la cámara.")
        return

    print("Detectando rostro... Presiona 'q' para salir.")

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Error al capturar la imagen.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(list(face_data.values()), face_encoding)
            name = "Desconocido"

            if True in matches:
                first_match_index = matches.index(True)
                name = list(face_data.keys())[first_match_index]
            else:
                # Mostrar "Desconocido" y permitir registrar en tiempo real
                cv2.putText(frame, "Desconocido", (face_location[3], face_location[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
                cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0, 0, 255), 2)

                # Preguntar si se desea registrar el rostro desconocido
                cv2.imshow("Detección de Rostro", frame)
                if cv2.waitKey(1000) & 0xFF == ord('a'):  # Presiona 'a' para agregar un rostro desconocido
                    name = input("Introduce el nombre de la persona: ")
                    face_data[name] = face_encoding
                    save_face_data(face_data)
                    print(f"Rostro de {name} guardado.")

            # Mostrar el nombre de la persona
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        cv2.imshow("Detección de Rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

# Función principal
def main():
    face_data = load_face_data()

    while True:
        choice = input("¿Quieres agregar un rostro nuevo o detectar un rostro existente? (agregar/detectar/salir): ").lower()

        if choice == "agregar":
            register_face(face_data)
        elif choice == "detectar":
            recognize_face(face_data)
        elif choice == "salir":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()

