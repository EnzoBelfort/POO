class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        cor_original = image[sr][sc]
        
        # Se a cor original já é a mesma que a cor desejada, não há nada a fazer, portanto retorna a imagem inalterada.
        if cor_original == color:
            return image
        
        # Inicia o processo de flood fill a partir do pixel (sr, sc).
        self._dfs(image, sr, sc, cor_original, color)
        return image

    def _dfs(self, image: List[List[int]], r: int, c: int, cor_original: int, nova_cor: int) -> None:
        # Verifica se o pixel está fora dos limites da imagem.
        if r < 0 or r >= len(image) or c < 0 or c >= len(image[0]):
            return
        
        # Se o pixel atual não tem a cor original, não deve ser alterado.
        if image[r][c] != cor_original:
            return
        
        image[r][c] = nova_cor
        
        self._dfs(image, r - 1, c, cor_original, nova_cor)  # Acima
        self._dfs(image, r + 1, c, cor_original, nova_cor)  # Abaixo
        self._dfs(image, r, c - 1, cor_original, nova_cor)  # Esquerda
        self._dfs(image, r, c + 1, cor_original, nova_cor)  # Direita  