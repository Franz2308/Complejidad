# mi_app/algoritmo.py
from math import radians, cos, sin, sqrt, atan2
from mi_app.graph_utils import minutos_entre_distritos
from mi_app.utils import distritos

def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def compatibilidad(estudiante1, estudiante2, speed_kmh=25):
    score = 0
    
    # Edad
    edad_diff = abs(estudiante1.age - estudiante2.age)
    score += max(0, 1 - (edad_diff / 10))
    
    # Presupuesto
    budget_diff = abs(estudiante1.expected_rent - estudiante2.expected_rent)
    score += max(0, 1 - (budget_diff / 1000))
    
    # Distancia geográfica
    dist = distancia_km(estudiante1.latitude, estudiante1.longitude,
                        estudiante2.latitude, estudiante2.longitude)
    score += max(0, 1 - (dist / 20))
    
    # Mascotas y fumador
    if estudiante1.has_pets == estudiante2.has_pets:
        score += 1
    if estudiante1.smoker == estudiante2.smoker:
        score += 1

    # --- NUEVO: tiempo al campus ---
    tiempo1 = minutos_entre_distritos(distritos, estudiante1.district, estudiante1.university, speed_kmh)
    tiempo2 = minutos_entre_distritos(distritos, estudiante2.district, estudiante2.university, speed_kmh)
    tiempo_diff = abs(tiempo1 - tiempo2)
    
    if tiempo_diff <= 10:       # diferencia menor a 10 min → suma 1
        score += 1
    elif tiempo_diff <= 20:     # diferencia entre 10 y 20 min → suma 0.5
        score += 0.5
    # >20 min → no suma

    max_score = 6  # antes era 5, ahora sumamos máximo 1 por tiempo
    return round(score / max_score, 2)
