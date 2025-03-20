class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):                       # se as strings não têm o mesmo tamanho    
            return False
        
        s_ordenado = sorted(s)                      
        t_ordenado = sorted(t)
        
        return s_ordenado == t_ordenado