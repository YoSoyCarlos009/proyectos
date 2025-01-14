import speech_recognition as sr
import keyboard  # Para detectar las teclas presionadas
import pyttsx3  # Para convertir texto a voz

# Diccionario de palabras personalizado
custom_dictionary = {
    "py": "Python",
    "usb": "USB",
    "ide": "entorno de desarrollo integrado",
    # Agrega más palabras y sus equivalentes según tu necesidad
}

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    waiting_for_space = True  # Bandera para controlar si se muestra el mensaje de espera

    with sr.Microphone() as source:
        print("Esperando que el micrófono esté activo...")
        recognizer.adjust_for_ambient_noise(source)
        print("Micrófono activo. Mantén presionada la tecla 'espacio' para dictar, presiona '0' para finalizar.")

        while True:
            if keyboard.is_pressed('0'):
                print("Programa finalizado.")
                break

            if keyboard.is_pressed('space'):
                if waiting_for_space:
                    print("Escuchando...")
                    waiting_for_space = False  # Cambiar la bandera para evitar repetir el mensaje

                audio = recognizer.listen(source)

                try:
                    # Reconocimiento de voz usando Google Speech Recognition
                    text = recognizer.recognize_google(audio, language="es-ES")  # Cambia el idioma según lo que necesites
                    print(f"Texto reconocido: {text}")

                    # Revisar si hay palabras del diccionario personalizado y reemplazarlas
                    words = text.split()
                    corrected_text = ' '.join([custom_dictionary.get(word.lower(), word) for word in words])

                    print(f"Texto final después de ajustar: {corrected_text}")

                    # Convertir texto final a voz
                    text_to_speech(corrected_text)

                except sr.UnknownValueError:
                    print("No pude entender el audio")
                except sr.RequestError as e:
                    print(f"No se pudo conectar al servicio de reconocimiento de voz; {e}")
            else:
                if not waiting_for_space:
                    print("Esperando dictado... Mantén presionada la tecla 'espacio'.")
                    waiting_for_space = True  # Cambiar la bandera para mostrar el mensaje una vez

def text_to_speech(text):
    """Convierte el texto a voz."""
    engine.say(text)
    engine.runAndWait()

def text_input_mode():
    """Permite al usuario escribir texto y lo convierte a voz."""
    while True:
        text = input("Escribe el texto que quieres convertir a voz (o presiona '0' para finalizar): ")
        if text == '0':
            print("Programa finalizado.")
            break

        # Revisar si hay palabras del diccionario personalizado y reemplazarlas
        words = text.split()
        corrected_text = ' '.join([custom_dictionary.get(word.lower(), word) for word in words])

        print(f"Texto final después de ajustar: {corrected_text}")
        
        # Convertir el texto corregido a voz
        text_to_speech(corrected_text)

if __name__ == "__main__":
    # Preguntar al usuario si quiere dictar o escribir
    print("¿Quieres dictar o escribir? (Escribe 'dictar' o 'escribir')")
    mode = input().strip().lower()

    if mode == "dictar":
        recognize_speech_from_mic()
    elif mode == "escribir":
        text_input_mode()
    else:
        print("Opción no válida. Por favor, selecciona 'dictar' o 'escribir'.")
