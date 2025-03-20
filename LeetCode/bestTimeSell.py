class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        def findMaxProfit(left: int, right: int) -> int:
            if left == right:  # Caso base
                return 0

            mid = (left + right) // 2

            # Calcula os lucros para as duas metades
            left_max = findMaxProfit(left, mid)
            right_max = findMaxProfit(mid + 1, right)

            # Calcula o lucro máximo cruzando o meio
            cross_max = findMaxCrossing(prices, left, mid, right)

            # Retorna o lucro máximo entre as três partes
            return max(left_max, right_max, cross_max)

        def findMaxCrossing(prices: List[int], left: int, mid: int, right: int) -> int:
            min_left = float("inf")
            for i in range(left, mid + 1):
                min_left = min(min_left, prices[i])

            max_right = float("-inf")
            for j in range(mid + 1, right + 1):
                max_right = max(max_right, prices[j])

            return max_right - min_left

        # Inicializar os cálculos
        left = 0
        right = len(prices) - 1
        max_profit = findMaxProfit(left, right)

        return max(0, max_profit)
