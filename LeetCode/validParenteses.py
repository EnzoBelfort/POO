class Solution:
    def isValid(self, s: str) -> bool:
        pilha = []
        
        dic_chaves = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        
        for char in s:
            if char not in dic_chaves:
                pilha.append(char)
            else:
                if not pilha or pilha[-1] != dic_chaves[char]:
                    return False
                pilha.pop()
        
        return len(pilha) == 0