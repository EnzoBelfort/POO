class Solution:
  def mergeTwoLists(self, lista1: Optional[ListNode], lista2: Optional[ListNode]) -> Optional[ListNode]:
    head = ListNode(0)                   # cabeça da lista nova 
    atual = head                         # ponteiro para a lista nova

    while lista1 and lista2:
      if lista1.val <= lista2.val:
        atual.next = lista1
        lista1 = lista1.next
      else:
        atual.next = lista2
        lista2 = lista2.next
      atual = atual.next
    
    if lista1:
      atual.next = lista1
    else:
      atual.next = lista2

    return head.next  