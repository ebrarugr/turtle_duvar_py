"""Kaplumbağanın duvardan yansıyacağı yönü hesaplayan yardımcı işlevler."""

import math


def aciyi_normalize_et(aci):
    """Açıyı -pi ile pi arasına getirir."""
    return math.atan2(math.sin(aci), math.cos(aci))


def yeni_yon_hesapla(x, y, theta, alt_sinir, ust_sinir):
    """Dışarı yönelen kaplumbağa duvara geldiyse yeni hedef açıyı döndürür.

    Duvara çarpılmadıysa None döndürür. Yalnızca duvara doğru gidiliyorsa
    dönüş başlatılır; böylece dönüşten sonra aynı duvarda takılıp kalınmaz.
    """
    x_yonu = math.cos(theta)
    y_yonu = math.sin(theta)

    x_duvari = (
        (x <= alt_sinir and x_yonu < -0.0001)
        or (x >= ust_sinir and x_yonu > 0.0001)
    )
    y_duvari = (
        (y <= alt_sinir and y_yonu < -0.0001)
        or (y >= ust_sinir and y_yonu > 0.0001)
    )

    if not (x_duvari or y_duvari):
        return None

    yeni_aci = theta
    if x_duvari:
        yeni_aci = math.pi - yeni_aci
    if y_duvari:
        yeni_aci = -yeni_aci

    return aciyi_normalize_et(yeni_aci)
