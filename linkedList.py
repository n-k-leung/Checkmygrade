# Node class to be a part of Linked List
import sys
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create a class called LinkedList 
class LinkedList:
    def __init__(self):
        self.head = None
        #no tail so need to traverse

    # Add a node at the begining
    def add_first(self, data):
        """ Add First Node"""
        new_node = Node(data)
        if self.head is None: 
            self.head = new_node
            return
        else:
            new_node.next=self.head
            self.head=new_node
 

    ### Insert at the end
    def add_last(self, data):
        """ Add node at last position"""
        new_node = Node(data)
        if self.head is None:
            self.head=new_node
            return
            # if no allocated then return
        # will lose head so need copy; traversing copy not head
        current_node = self.head
        while current_node.next:
            current_node=current_node.next
        current_node.next=new_node



    def add_at_index(self, data,newdata):
        """Add node at a specifiec newdata"""
        if newdata == 0:
            self.add_first(data)
            return
        if newdata < 0:
            raise IndexError("Index cannot be negative")
            return
        else:
            current_node = self.head
            count = 0
            new_node = Node(data)
            if current_node is None:
                print("Index out of bounds")
                return
            # traverse linked list to get the index where to input a value
            while current_node is not None and count < newdata - 1:
                current_node = current_node.next
                count += 1
            
            new_node.next = current_node.next
            current_node.next = new_node
        


    def print_linked_list(self):
        """ print the  linked list"""
        if self.head is None:
            print("linked list is empty")
            return
        current_node = self.head
        #traverse list and pring
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next



    def check_head(self):
        # conditional statement
        return True if self.head is not None else False
    
    def linked_size(self):
        """ Get the size of linked list"""
        current_node = self.head
        sizeb=0
        i=0
        while current_node is not None:
            i=i+1
            sizeb= sizeb + sys.getsizeof(current_node.data)
            current_node=current_node.next
        return i,sizeb

    def delete_node(self, data):
        """ delete the linked linked list node"""
        current = self.head
        prev = None

        while current:
            if current.data == data:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next
        print("No data found")
            

    def delete_first_node(self):
        """ delete the linked linked list first node"""
        if not self.check_head():
            return None
        self.head = self.head.next
      
    def delete_last_node(self):
        """ delete the linked linked list last node"""
        if not self.check_head():
            return None
        current_node =self.head
        while current_node.next.next and current_node.next:
            current_node=current_node.next
            # one node before last
        current_node.next = None

    def delete_at_index(self,data):
        """ delete the linked linked list node"""
        if data < 0:
            return
        
        if data == 0:
            if self.head is not None:
                self.head = self.head.next
            return
        
        current_node = self.head
        prev = None
        count = 0

        while current_node is not None and count < data:
            prev = current_node
            current_node = current_node.next
            count += 1

        if current_node is None:
            return
        
        prev.next = current_node.next
        pass
    
    def reverse(self):
        """ This function reverse the list"""
        current_node = self.head
        prev = None

        # traverse all nodes of linked list
        while current_node is not None:
            nextNode = current_node.next
            current_node.next = prev
            prev = current_node
            current_node = nextNode

        self.head = prev

        return prev


def linkedList():
    ll=LinkedList()
    ll.add_first(4)
    ll.add_first(5)
    ll.add_first(7)
    ll.add_first(8)
    ll.add_first(9)
    ll.add_last(20)
    print("\nLinked List 1st time")
    ll.print_linked_list()

    #add functions
    try:
        ll.add_at_index(3,2) 
    except IndexError as e:
        print(f"Error: {e}")
    
    print("Linked List after adding 3 to index 2 of linked list")
    ll.print_linked_list()
    ll.add_first(2)
    print("Linked List after adding 2 to top of linked list")
    ll.print_linked_list()
    ll.add_last(21)
    print("Linked List after adding 21 to end of linked list")
    ll.print_linked_list()

    #delete functions
    ll.delete_first_node()
    print("Linked list after deleting first node:")
    ll.print_linked_list()
    ll.delete_last_node()
    print("Linked list after deleting last node:")
    ll.print_linked_list()
    ll.delete_at_index(1)
    print("Linked list after deleting index 1:")
    ll.print_linked_list()
    ll.delete_node(3)
    print("Linked list after deleting node 3:")
    ll.print_linked_list()

    #size function
    length, byte_size = ll.linked_size()
    print(f"Length of linked list: {length}")
    print(f"Byte size: {byte_size}")

    #reverse function
    ll.reverse()
    print("Linked list reversed:")
    ll.print_linked_list()

if __name__ == "__main__":
    linkedList()

# output:
# Linked List 1st time
# 9
# 8
# 7
# 5
# 4
# 20
# Linked List after adding 3 to index 2 of linked list
# 9
# 8
# 3
# 7
# 5
# 4
# 20
# Linked List after adding 2 to top of linked list
# 2
# 9
# 8
# 3
# 7
# 5
# 4
# 20
# Linked List after adding 21 to end of linked list
# 2
# 9
# 8
# 3
# 7
# 5
# 4
# 20
# 21
# Linked list after deleting first node:
# 9
# 8
# 3
# 7
# 5
# 4
# 20
# 21
# Linked list after deleting last node:
# 9
# 8
# 3
# 7
# 5
# 4
# 20
# Linked list after deleting index 1:
# 9
# 3
# 7
# 5
# 4
# 20
# Linked list after deleting node 3:
# 9
# 7
# 5
# 4
# 20
# Length of linked list: 5
# Byte size: 140
# Linked list reversed:
# 20
# 4
# 5
# 7
# 9