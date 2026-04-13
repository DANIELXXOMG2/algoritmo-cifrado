# Algoritmo de Cifrado

**Sistema de cifrado AES-GCM con verificación de integridad SHA-256**

🔗 **Repositorio**: [https://github.com/DANIELXXOMG2/algoritmo-cifrado](https://github.com/DANIELXXOMG2/algoritmo-cifrado)

Sistema académico que implementa cifrado simétrico AES-256-GCM con generación de huellas digitales SHA-256 y control de integridad.

## Características

- **Cifrado AES-256-GCM**: Cifrado simétrico autenticado de 256 bits
- **Derivación de claves PBKDF2-SHA256**: 480,000 iteraciones (recomendación OWASP 2023)
- **Verificación de integridad SHA-256**: Huella digital criptográfica
- **Interfaz CLI**: Comandos para cifrar, descifrar, calcular hash y verificar
- **Soporte Unicode**: Manejo completo de texto en múltiples idiomas
- **Gestión de archivos**: Operaciones seguras de lectura/escritura

## Requisitos

- Python 3.10+
- `cryptography>=43.0.0`

## Instalación

```bash
# Clonar el repositorio
cd "Algoritmo de Cifrado"

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar el paquete en modo desarrollo
pip install -e .
```

## Uso

### Cifrar texto

```bash
algoritmo-cifrado encrypt --input "Hola Mundo" --password "mipassword" --output mensaje.enc
```

### Descifrar archivo

```bash
algoritmo-cifrado decrypt --input mensaje.enc --password "mipassword" --output descifrado.txt
```

### Calcular huella SHA-256

```bash
# De texto
algoritmo-cifrado hash --input "Hello World"

# De archivo
algoritmo-cifrado hash --input documento.txt
```

### Verificar integridad

```bash
algoritmo-cifrado verify --input archivo.txt --fingerprint "abc123..."
```

## Arquitectura

```
algoritmo_cifrado/
├── cipher/           # Cifrado AES-GCM
│   ├── aes_gcm.py    # Funciones de cifrado/descifrado
│   └── exceptions.py # Jerarquía de excepciones
├── hash_utils/       # Utilidades de hash
│   └── sha256.py     # Fingerprinting SHA-256
├── key_utils/        # Gestión de claves
│   ├── pbkdf2.py     # Derivación PBKDF2
│   └── salt.py       # Generación de sales
├── validators/       # Validación de entradas
│   ├── input.py      # Validación de texto/password
│   └── file_handler.py # Operaciones de archivos
└── cli/              # Interfaz de línea de comandos
    ├── commands.py   # Lógica de comandos
    └── main.py       # Punto de entrada
```

## Formato de archivo cifrado

```
[salt: 16 bytes][iv: 12 bytes][meta_len: 4 bytes][metadata JSON][ciphertext+tag]
```

- **salt**: 16 bytes aleatorios para derivación de clave
- **iv**: 12 bytes para modo GCM
- **meta_len**: Longitud del metadata en bytes (big-endian)
- **metadata**: JSON con nombre original, tamaño, parámetros
- **ciphertext+tag**: Datos cifrados + tag de autenticación (16 bytes)

## Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=term-missing

# Ejecutar prueba específica
pytest tests/test_cipher.py -v
```

## Medidas de seguridad

| Concern | Mitigación |
|---------|------------|
| Reutilización de IV | IV único de 12 bytes por operación |
| Fuerza bruta de contraseña | PBKDF2 con 480,000 iteraciones |
| Reutilización de salt | Salt aleatorio de 16 bytes por clave |
| Modificación de ciphertext | Tag GCM de 128 bits verificado |
| Errores con información | Mensajes genéricos para distintos errores |

## Autor

Proyecto Académico

## Licencia

MIT License
