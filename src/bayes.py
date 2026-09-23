"""Valor preditivo e volume de alertas falsos do sensor."""
from gerador_pomar import parametros_sensor

def calcular(matricula):
    p = parametros_sensor(matricula)
    prevalencia = p["prevalencia"]
    sensibilidade = p["sensibilidade"]
    falso_positivo = p["taxa_falso_positivo"]
    def vpp(s):
        return (s * prevalencia) / (s * prevalencia + falso_positivo * (1 - prevalencia))
    falsos = p["talhoes_por_semana"] * (1 - prevalencia) * falso_positivo
    return {**p, "vpp": vpp(sensibilidade), "falsos_em_100_alertas": 100 * (1 - vpp(sensibilidade)),
            "falsos_por_semana": falsos, "horas_perdidas": falsos * 12 / 60,
            "vpp_999": vpp(.999),
            "vpp_dois_positivos_independentes": (prevalencia * sensibilidade**2) /
                (prevalencia * sensibilidade**2 + (1 - prevalencia) * falso_positivo**2)}
