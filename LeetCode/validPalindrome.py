class Solution:
    def isPalindrome(self, s: str) -> bool:
        inicio = 0
        fim = len(s) - 1
        
        while inicio < fim:
            while inicio < fim and not s[inicio].isalnum():               # se o caractere não for alfanumérico
                inicio += 1
            
            while inicio < fim and not s[fim].isalnum():
                fim -= 1
            
            if s[inicio].lower() != s[fim].lower():
                return False
            
            inicio += 1
            fim -= 1
        
        return True