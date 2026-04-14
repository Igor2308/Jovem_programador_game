def limitar_na_tela(rect, largura_tela, altura_tela):
    margem = 15

    if rect.left < margem:
        rect.left = margem
    if rect.right > largura_tela - margem:
        rect.right = largura_tela - margem
    if rect.top < margem:
        rect.top = margem
    if rect.bottom > altura_tela - margem:
        rect.bottom = altura_tela - margem