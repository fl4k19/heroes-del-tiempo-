import random
import time
import os

# =========================
# Definición de clases
# =========================

class Personaje:
    def __init__(self, nombre, raza, vida, ataque, defensa, arma, habilidades):
        self.nombre = nombre
        self.raza = raza
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defensa = defensa
        self.arma = arma
        self.habilidades = habilidades

    def esta_vivo(self):
        return self.vida > 0

    def atacar(self, enemigo):
        dano = max(0, self.ataque - enemigo.defensa)
        enemigo.vida -= dano
        print(f"{self.nombre} ataca a {enemigo.nombre} con {self.arma} ⚔️ y causa {dano} de daño.")

    def usar_habilidad(self, enemigo):
        print("\nElige una habilidad:")
        for idx, hab in enumerate(self.habilidades):
            print(f"{idx + 1}) {hab['nombre']}: {hab['descripcion']}")
        eleccion = input("Número de habilidad: ").strip()
        if eleccion.isdigit():
            idx = int(eleccion) - 1
            if 0 <= idx < len(self.habilidades):
                habilidad = self.habilidades[idx]
                habilidad['funcion'](self, enemigo)
                return
        print("❌ ¡Opción inválida! Se pierde el turno.")

class Enemigo:
    def __init__(self, nivel):
        self.nombre = f"Enemigo Nivel {nivel}"
        self.vida = 50 + nivel * 10
        self.vida_max = self.vida
        self.ataque = 10 + nivel * 2
        self.defensa = 5 + nivel
        self.arma = "Garras"

    def esta_vivo(self):
        return self.vida > 0

    def atacar(self, jugador):
        dano = max(0, self.ataque - jugador.defensa)
        jugador.vida -= dano
        print(f"{self.nombre} ataca a {jugador.nombre} y causa {dano} de daño.")

# =========================
# Habilidades de personajes
# =========================

def habilidad_corte_rapido(jugador, enemigo):
    print(f"⚡ {jugador.nombre} usa Corte Rápido ⚔️.")
    dano = jugador.ataque + 5 - enemigo.defensa
    dano_real = max(0, dano)
    enemigo.vida -= dano_real
    print(f"💥 Causa {dano_real} de daño.")

def habilidad_guardia(jugador, enemigo):
    print(f"🛡️ {jugador.nombre} usa Guardia. ¡Aumenta su defensa!")
    jugador.defensa += 5
    print(f"{jugador.nombre} ahora tiene {jugador.defensa} de defensa.")

def habilidad_lanza_sagrada(jugador, enemigo):
    print(f"🔱 {jugador.nombre} lanza su Lanza Sagrada.")
    dano = jugador.ataque + 8 - enemigo.defensa
    dano_real = max(0, dano)
    enemigo.vida -= dano_real
    print(f"💥 Causa {dano_real} de daño.")

def habilidad_curacion(jugador, enemigo):
    print(f"✨ {jugador.nombre} usa Curación.")
    curacion = 15
    jugador.vida = min(jugador.vida + curacion, jugador.vida_max)
    print(f"❤️ Recupera {curacion} de vida. Ahora tiene {jugador.vida} de vida.")

habilidades_tomoe = [
    {"nombre": "Corte Rápido", "descripcion": "Ataque veloz que inflige daño extra.", "funcion": habilidad_corte_rapido},
    {"nombre": "Guardia", "descripcion": "Aumenta temporalmente la defensa.", "funcion": habilidad_guardia}
]

habilidades_juana = [
    {"nombre": "Lanza Sagrada", "descripcion": "Ataque poderoso con la lanza.", "funcion": habilidad_lanza_sagrada},
    {"nombre": "Curación", "descripcion": "Recupera vida.", "funcion": habilidad_curacion}
]

# =========================
# Utilidades visuales
# =========================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_vida_corazones(vida_actual, vida_max):
    corazones_totales = 10
    corazones_llenos = int((vida_actual / vida_max) * corazones_totales)
    corazones_vacios = corazones_totales - corazones_llenos
    return "❤️" * corazones_llenos + "♡" * corazones_vacios

def mostrar_estado_general(jugador, companero, enemigo):
    print("="*40)
    print(f"🧙‍♂️ {jugador.nombre}  | Vida: {mostrar_vida_corazones(jugador.vida, jugador.vida_max)} ({jugador.vida}/{jugador.vida_max}) | Defensa: {jugador.defensa} | Arma: {jugador.arma} ⚔️")
    print(f"🤝 {companero.nombre} | Vida: {mostrar_vida_corazones(companero.vida, companero.vida_max)} ({companero.vida}/{companero.vida_max}) | Defensa: {companero.defensa} | Arma: {companero.arma} ⚔️")
    print(f"👹 {enemigo.nombre} | Vida: {mostrar_vida_corazones(enemigo.vida, enemigo.vida_max)} ({enemigo.vida}/{enemigo.vida_max}) | Defensa: {enemigo.defensa} | Arma: {enemigo.arma} 🐾")
    print("="*40)

# =========================
# Menú de selección
# =========================

def menu_seleccion_personaje():
    personajes = [
        Personaje("Tomoe", "Humano", 100, 20, 10, "Katana", habilidades_tomoe),
        Personaje("Juana de Arco", "Humano", 80, 15, 12, "Lanza", habilidades_juana)
    ]
    print("=== MENÚ DE SELECCIÓN DE PERSONAJE ===")
    while True:
        for idx, personaje in enumerate(personajes):
            print(f"{idx + 1}) {personaje.nombre} ({personaje.raza}, {personaje.arma})")
        eleccion = input("Elige el número de tu personaje: ").strip()
        if eleccion.isdigit():
            idx = int(eleccion) - 1
            if 0 <= idx < len(personajes):
                jugador = personajes.pop(idx)
                companero = personajes[0]
                print(f"\nHas elegido: {jugador.nombre}")
                print(f"Tu compañero será: {companero.nombre}")
                time.sleep(2)
                return jugador, companero
        print("❌ ¡Opción inválida! Intenta de nuevo.")

# =========================
# Turnos de juego
# =========================

def turno_jugador(jugador, enemigo):
    if not jugador.esta_vivo():
        return
    print(f"\n➡️ Turno de {jugador.nombre}:")
    print("1) Atacar ⚔️")
    print("2) Usar habilidad ✨")
    opcion = input("Elige una opción: ").strip()
    if opcion == "1":
        jugador.atacar(enemigo)
    elif opcion == "2":
        jugador.usar_habilidad(enemigo)
    else:
        print("❌ ¡Opción inválida! Se pierde el turno.")

def turno_companero(companero, enemigo):
    if not companero.esta_vivo():
        return
    accion = random.choice(["atacar", "habilidad"])
    print(f"\n➡️ Turno de {companero.nombre}:")
    if accion == "atacar":
        print(f"{companero.nombre} decide atacar ⚔️")
        companero.atacar(enemigo)
    else:
        habilidad = random.choice(companero.habilidades)
        print(f"{companero.nombre} usa {habilidad['nombre']} ✨: {habilidad['descripcion']}")
        habilidad['funcion'](companero, enemigo)
    time.sleep(1)

def turno_enemigo(enemigo, jugador, companero):
    if not enemigo.esta_vivo():
        return
    objetivo = jugador if jugador.esta_vivo() else companero
    print(f"\n➡️ Turno de {enemigo.nombre}:")
    enemigo.atacar(objetivo)
    time.sleep(1)

# =========================
# Juego principal
# =========================

def juego():
    limpiar_pantalla()
    print("⚔️ HEROES DEL TIEMPO ⚔️")
    nivel = 1

    jugador, companero = menu_seleccion_personaje()

    while jugador.esta_vivo() and companero.esta_vivo():
        enemigo = Enemigo(nivel)
        while jugador.esta_vivo() and companero.esta_vivo() and enemigo.esta_vivo():
            limpiar_pantalla()
            mostrar_estado_general(jugador, companero, enemigo)
            turno_jugador(jugador, enemigo)
            if enemigo.esta_vivo():
                turno_companero(companero, enemigo)
            if enemigo.esta_vivo():
                turno_enemigo(enemigo, jugador, companero)
            time.sleep(1.5)

        if jugador.esta_vivo() and companero.esta_vivo():
            print(f"\n🎉 ¡VICTORIA! Nivel {nivel} completado 🎉")
            nivel += 1
            time.sleep(2)
        else:
            print("\n☠️ HAS SIDO DERROTADO ☠️")
            break

if __name__ == "__main__":
    juego()
