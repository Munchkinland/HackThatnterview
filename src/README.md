# Hackea la Entrevista

![download(1)](https://github.com/user-attachments/assets/39123f83-bced-4c0d-a164-cbe29f87fb0e)

## Descripción

**Hackea la Entrevista** es un asistente inteligente diseñado para ayudar a los candidatos a prepararse para entrevistas de trabajo. Utiliza tecnologías avanzadas de procesamiento de lenguaje natural y reconocimiento de voz para proporcionar respuestas efectivas a preguntas de entrevistas, basándose en el currículum del usuario y la descripción del trabajo.

## Características

- **Procesamiento de Currículums**: Soporta múltiples formatos de archivo (txt, docx, pdf, ppt, pptx) para extraer información clave.
- **Reconocimiento de Voz**: Captura preguntas de entrevistas en tiempo real y las convierte a texto.
- **Generación de Respuestas**: Utiliza modelos de IA para generar respuestas personalizadas.
- **Traducción de Idiomas**: Traduce preguntas y respuestas a diferentes idiomas según sea necesario.
- **Interfaz de Usuario Intuitiva**: Fácil de usar, con opciones para cargar archivos y escuchar preguntas.

## Instalación

### 1. Clona este repositorio:

git clone https://github.com/tuusuario/hackea-la-entrevista.git

cd hackea-la-entrevista


### 2. Crea un entorno virtual e instala las dependencias:

bash
python -m venv venv

source venv/bin/activate  # En Windows usa venv\Scripts\activate

pip install -r requirements.txt


### 3. Configura las variables de entorno:

   - Crea un archivo `.env` en la raíz del proyecto y añade tu clave de API de OpenAI:
     ```

 OPENAI_API_KEY=tu_clave_api
 

   - **Obtener la clave de API de OpenAI**: Regístrate en [OpenAI](https://beta.openai.com/signup/) y genera una clave de API desde el panel de control.

### 4. Descarga y configura el modelo Vosk:
   - Descarga el modelo de Vosk desde [Vosk Models](https://alphacephei.com/vosk/models).
   - Descomprime el modelo descargado en la carpeta `models` dentro del directorio del proyecto.

### 5. Ejecuta la aplicación:

bash
python main.py


## Uso

1. Abre la aplicación y carga tu currículum y la descripción del trabajo.
2. Usa el micrófono para hacer preguntas de entrevista o escríbelas directamente.
3. Genera respuestas y, si es necesario, tradúcelas al idioma deseado.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`).
4. Sube tus cambios (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](./LICENSE).

## Contacto

Me puedes enviar un mensaje o pull request desde GITHUB

### Video Explicativo

https://www.linkedin.com/feed/update/urn:li:activity:7250946140756467712/

