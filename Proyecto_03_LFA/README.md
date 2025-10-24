# Proyecto 03 - Validación con Regex

## 📚 Descripción del Proyecto
Este software educativo ha sido desarrollado como parte del curso **Lenguajes Formales y Autómatas** de la carrera de **Ingeniería en Informática y Sistemas**.  
Su objetivo principal es proporcionar una herramienta práctica que permita a los estudiantes comprender y aplicar los conceptos de **expresiones regulares (Regex)**, relacionando los fundamentos teóricos de gramáticas y autómatas con su implementación en un entorno interactivo.

## 🧠 Funcionalidades Principales
- Ingreso de una expresión regular para validarla sintácticamente.
- Ingreso de un texto de varias líneas para aplicar la expresión regular.
- Validación de errores de sintaxis en la expresión regular.
- Resaltado visual de las coincidencias encontradas en el texto.
- Listado separado de todas las coincidencias detectadas.

## ⚖️ Reglas de Validación Implementadas
- Paréntesis y corchetes correctamente balanceados.
- Uso permitido de símbolos básicos: letras (a–z, A–Z), dígitos (0–9) y caracteres especiales.
- Operadores soportados: `.`, `*`, `+`, `?`, `|`, `()`, `[]`, `\d`, `\w`, `\s`.
- Escapes válidos reconocidos: `\d`, `\w`, `\s`, `\b`, `\B`, `\t`, `\n`, `\r`, `\f`, `\v`, `\\`, entre otros.
- No se permiten cuantificadores consecutivos inválidos (`**`, `++`, `??`).

## 📁 Estructura del Proyecto
Proyecto_03_Validacion_Regex/

├── main.html # Interfaz gráfica

├── main.js # Lógica de validación y procesamiento

├── main.css # Estilos visuales

└── README.md # Documentación del proyecto

## ⚙️ Tecnologías Utilizadas
- **Lenguaje:** JavaScript
- **Estructura y estilos:** HTML5 + CSS3
- **Control de versiones:** Git & GitHub

## 🛠️ Cómo usar el programa
1. Clonar o descargar el proyecto.
2. Abrir el archivo **main.html** en un navegador web.
3. Escribir una expresión regular en el campo de entrada.
4. Escribir un texto de prueba en el área de texto.
5. Presionar el botón **“Validar”** para procesar la entrada.
6. Visualizar las coincidencias resaltadas en el texto y listadas debajo.
7. Si la expresión es inválida, corregirla según el mensaje de error mostrado.

## 🧑‍🤝‍🧑 Equipo de Desarrollo
- Granados de León, Luis Oswaldo – 1506124
- Ramirez Alvarez, Javier Estuardo – 1647124
- Santay Matías, Mily Angélica Virginia – 1507624
