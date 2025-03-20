# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        
        if root is None:            # caso base
            return None
        
        # pós ordem
        filho_esq = self.invertTree(root.left)
        filho_dir = self.invertTree(root.right)
        
        root.left = filho_dir
        root.right = filho_esq
        
        return root