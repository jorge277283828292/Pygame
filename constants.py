# SIZES
# Tamaños
WIDTH, HEIGHT = 1280, 720  # Screen dimensions / Dimensiones de la pantalla
PLAYER = 100  # Player character size / Tamaño del personaje del jugador
GRASS = 64  # Size of a single grass tile / Tamaño de un tile de pasto individual
GRASSES = 40  # Number or density of grass objects / Número o densidad de objetos de pasto
TREE = 120  # Tree object size / Tamaño del objeto árbol
SMALL_STONE = 60  # Small stone object size / Tamaño del objeto piedra pequeña
FLOWER = 60  # Flower object size / Tamaño del objeto flor
HOUSE = 150  # House object size / Tamaño del objeto casa
GRASS_OBJ = 15  # Size of decorative grass objects / Tamaño de los objetos de pasto decorativos
DECORATIVE_FLOWER = 20  # Size of decorative flower objects / Tamaño de los objetos de flores decorativas

# ANIMATIONS
# Animaciones
BASIC_FRAMES = 6  # Number of basic animation frames / Número de frames de animación básicos
IDLE_DOWN = 0  # Animation index for idle facing down / Índice de animación para inactivo mirando hacia abajo
IDLE_RIGHT = 1  # Animation index for idle facing right / Índice de animación para inactivo mirando hacia la derecha
IDLE_UP = 2  # Animation index for idle facing up / Índice de animación para inactivo mirando hacia arriba
WALK_DOWN = 3  # Animation index for walking down / Índice de animación para caminar hacia abajo
WALK_RIGHT = 4  # Animation index for walking right / Índice de animación para caminar hacia la derecha
WALK_UP = 5  # Animation index for walking up / Índice de animación para caminar hacia arriba
FRAME_SIZE = 32  # Size of an individual animation frame / Tamaño de un frame de animación individual
ANIMATION_DELAY = 100  # Delay between animation frames (milliseconds) / Retraso entre frames de animación (milisegundos)
RUNNING = 50  # Speed factor or state for running / Factor de velocidad o estado para correr

# COLORS
# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# STATES
# Estados máximos
MAX_ENERGY = 100  # Maximum energy level / Nivel máximo de energía
MAX_FOOD = 100  # Maximum food level / Nivel máximo de comida
MAX_THIRST = 100  # Maximum thirst level / Nivel máximo de sed
MAX_STAMINA = 100  # Maximum stamina level / Nivel máximo de resistencia

# COLORS STATES
# Colores de las barras de estado
ENERGY_COLOR = (255, 255, 0)  # Yellow for energy bar / Amarillo para la barra de energía
FOOD_COLOR = (255, 165, 0)  # Orange for food bar / Naranja para la barra de comida
THIRST_COLOR = (0, 191, 255)  # Blue for thirst bar / Azul para la barra de sed
STAMINA_COLOR = (124, 252, 0)  # Green for stamina bar / Verde para la barra de resistencia
BAR_BACKGROUND_COLOR = (100, 100, 100)  # Dark gray for bar background / Gris oscuro para el fondo de la barra

# INTERVAL OF TIME
# Intervalo de actualización de estado
STATUS_UPDATE_INTERVAL = 1000  # How often status bars update (milliseconds) / Cada cuánto se actualizan las barras de estado (milisegundos)

# SYSTEM DAY/NIGHT
# Sistema de día/noche
DAY_LENGTH = 30 * 24000  # Total length of a day-night cycle (milliseconds) / Duración total de un ciclo día-noche (milisegundos)
DAWN_TIME = 12000  # Time point for dawn / Punto de tiempo para el amanecer
MORNING_TIME = 8000  # Time point for morning / Punto de tiempo para la mañana
DUSK_TIME = 24000  # Time point for dusk / Punto de tiempo para el anochecer
MIDNIGHT_TIME = 24000  # Time point for midnight (same as DUSK_TIME in this setup for transition) / Punto de tiempo para la medianoche (igual que DUSK_TIME en esta configuración para la transición)
MAX_DARKNESS = 180  # Maximum alpha value for darkness overlay / Valor alfa máximo para la superposición de oscuridad

# ILLUMINATION COLORS
# Colores de iluminación
NIGHT_COLOR = (20, 50, 50)  # Color tint for night / Tono de color para la noche
DAY_COLOR = (255, 255, 255)  # Color tint for day (full white) / Tono de color para el día (blanco completo)
DAWN_DUSK_COLOR = (255, 193, 137)  # Color tint for dawn/dusk / Tono de color para el amanecer/anochecer

NIGHT_START = 18  # Hour at which night starts (e.g., 6 PM) / Hora a la que comienza la noche (ej. 6 PM)
NIGHT_END = 20  # Hour at which night ends (e.g., 8 PM, used for fade out) / Hora a la que termina la noche (ej. 8 PM, usado para desvanecimiento)
MAX_NIGHT_ALPHA = 120  # Maximum transparency for the night overlay / Transparencia máxima para la superposición nocturna

# DECREASE AND INCREASE RATES
# Tasas de crecimiento y decrecimiento
FOOD_DECREASE_RATE = 0.01  # Rate at which food decreases / Tasa a la que disminuye la comida
THIRST_DECREASE_RATE = 0.02  # Rate at which thirst decreases / Tasa a la que disminuye la sed
ENERGY_DECREASE_RATE = 0.005  # Rate at which energy decreases / Tasa a la que disminuye la energía
ENERGY_INCREASE_RATE = 0.001  # Rate at which energy increases / Tasa a la que aumenta la energía
MOVEMENT_ENERGY_COST = 0.001  # Energy cost per unit of movement / Costo de energía por unidad de movimiento

# SPEED
# Velocidad
WALK_SPEED = 5  # Player walking speed / Velocidad de caminata del jugador
RUN_SPEED = 8  # Player running speed / Velocidad de carrera del jugador
STAMINA_DECREASE_RATE = 0.05  # Rate at which stamina decreases while running / Tasa a la que disminuye la resistencia al correr
STAMINA_INCREASE_RATE = 0.02  # Rate at which stamina increases when not running / Tasa a la que aumenta la resistencia al no correr
RUN_FOOD_DECREASE_MULTIPLER = 2.0  # Multiplier for food decrease when running / Multiplicador para la disminución de comida al correr
RUN_THIRST_DECREASE_MULTIPLER = 2.0  # Multiplier for thirst decrease when running / Multiplicador para la disminución de sed al correr

# INVENTORY CONSTANTS
# Constantes de Inventario
SLOT_SIZE = 64  # Size of each inventory slot / Tamaño de cada slot del inventario
HOTBAR_SLOTS = 8  # Number of slots in the hotbar / Número de slots en la hotbar
INVENTORY_ROWS = 4  # Number of rows in the main inventory / Número de filas en el inventario principal
INVENTORY_COLS = 5  # Number of columns in the main inventory / Número de columnas en el inventario principal
MARGIN = 10  # Margin around inventory elements / Margen alrededor de los elementos del inventario

# COLORS INVENTORY
# Colores Inventario
SLOT_COLOR = (139, 139, 139)  # Background color of inventory slots / Color de fondo de los slots del inventario
SLOT_BORDER = (100, 100, 100)  # Border color of inventory slots / Color del borde de los slots del inventario
SLOT_HOVER = (160, 160, 160)  # Color when a slot is hovered over / Color cuando se pasa el ratón por un slot

# HOTBAR POSITION (ALWAYS VISIBLE BELOW)
# Posición del hotbar (Siempre visible abajo)
HOTBAR_Y = HEIGHT - SLOT_SIZE - MARGIN  # Y-coordinate for the hotbar / Coordenada Y para la hotbar
HOTBAR_X = (WIDTH - (SLOT_SIZE * HOTBAR_SLOTS)) // 2  # X-coordinate for the hotbar (centered) / Coordenada X para la hotbar (centrada)

# MAIN INVENTORY POSITION
# Posición del inventario principal
INVENTORY_X = (WIDTH - (SLOT_SIZE * INVENTORY_COLS)) // 2  # X-coordinate for main inventory (centered) / Coordenada X para el inventario principal (centrada)
INVENTORY_Y = (HEIGHT - (SLOT_SIZE * INVENTORY_ROWS)) // 2  # Y-coordinate for main inventory (centered) / Coordenada Y para el inventario principal (centrada)

# CRAFTING CONSTANTS
# Constantes de Crafteo
CRAFTING_GRID_SIZE = 2  # Dimensions of the square crafting grid (e.g., 2x2) / Dimensiones de la cuadrícula de crafteo (ej. 2x2)
CRAFTING_GRID_Y = INVENTORY_Y + SLOT_SIZE  # Y-coordinate for the crafting grid / Coordenada Y para la cuadrícula de crafteo
CRAFTING_GRID_X = INVENTORY_X + (SLOT_SIZE * INVENTORY_COLS) + 50  # X-coordinate for the crafting grid / Coordenada X para la cuadrícula de crafteo
CRAFTING_RESULT_SLOT_X = CRAFTING_GRID_X + (SLOT_SIZE * CRAFTING_GRID_SIZE) + 20  # X-coordinate for the crafting result slot / Coordenada X para el slot de resultado de crafteo
CRAFTING_RESULT_SLOT_Y = CRAFTING_GRID_Y + (SLOT_SIZE // 2) - (SLOT_SIZE // 2)  # Y-coordinate for the crafting result slot (adjusted for centering) / Coordenada Y para el slot de resultado de crafteo (ajustada para centrado)
CRAFTING_GRID_ROWS = 2  # Number of rows in the crafting grid / Número de filas en la cuadrícula de crafteo
CRAFTING_GRID_COLS = 2  # Number of columns in the crafting grid / Número de columnas en la cuadrícula de crafteo

# HAND SLOTS CONSTANTS
# Constantes de los Slots de Mano
LEFT_HAND_SLOT_X = HOTBAR_X - SLOT_SIZE - MARGIN  # X-coordinate for the left hand slot / Coordenada X para el slot de la mano izquierda
LEFT_HAND_SLOT_Y = HOTBAR_Y  # Y-coordinate for the left hand slot / Coordenada Y para el slot de la mano izquierda
RIGHT_HAND_SLOT_X = HOTBAR_X + (SLOT_SIZE * HOTBAR_SLOTS) + MARGIN  # X-coordinate for the right hand slot / Coordenada X para el slot de la mano derecha
RIGHT_HAND_SLOT_Y = HOTBAR_Y  # Y-coordinate for the right hand slot / Coordenada Y para el slot de la mano derecha

# TOOLS ANIMATIONS
# Animaciones de Herramientas
AXE_COLS = 2  # Number of columns in the axe animation sprite sheet / Número de columnas en la hoja de sprites de la animación del hacha
AXE_FRAMES = 2  # Total frames for axe animation / Frames totales para la animación del hacha
AXE_ANIMATIONS_DELAY = 200  # Delay between axe animation frames / Retraso entre frames de animación del hacha
ACTION_FRAME_SIZE = 48  # Size of action animation frames (e.g., tool swings) / Tamaño de los frames de animación de acción (ej. golpes de herramienta)
HOE_COLS = 3  # Number of columns in the hoe animation sprite sheet / Número de columnas en la hoja de sprites de la animación de la azada
HOE_FRAMES = 3  # Total frames for hoe animation / Frames totales para la animación de la azada
HOE_ANIMATION_DELAY = 400  # Delay between hoe animation frames / Retraso entre frames de animación de la azada

# Water
# Agua
WATER_COLOR = (0, 191, 255)  # Color of water / Color del agua
WATER_MOVE_MULTIPLIER = 0.5  # Multiplier for water animation movement / Multiplicador para el movimiento de la animación del agua
WATER_GENERATION_PROBABILITY = 0.3  # Probability of water generation / Probabilidad de generación de agua
WATER_THIRST_RECOVERY = 20  # Amount of thirst recovered by drinking water / Cantidad de sed recuperada al beber agua
WATER_BUFFER_ZONE = 64  # Buffer zone around water for certain interactions / Zona de amortiguación alrededor del agua para ciertas interacciones

FARM_GROWTH_TIME = 10000  # Time in milliseconds for farm crops to grow one stage / Tiempo en milisegundos para que los cultivos de la granja crezcan una etapa