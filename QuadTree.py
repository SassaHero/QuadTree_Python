#!/usr/bin/env python
# -*- coding: utf-8 -*-
class QTNode:
    def __init__(self, point, label):
        self.label = label
        self.x = point[0]
        self.y = point[1]
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.Parent = None
            
class QuadTree:
    """
    Simple point quad tree implementaion.
    This quad tree supports insert, and searchNode operations.
    """
    def __init__(self):
        self.root = None
        self.nodeNum = 0
            
    def insertNode(self, newPoint):
        """Insert point into this quad tree."""
        new_node = QTNode(newPoint, self.nodeNum)
        if self.root is None :
            self.root = new_node
        else :
            node = self.root
            while True :
                if newPoint[0] >= node.x and newPoint[1] >= node.y :  # NE region
                    if node.NE is None :
                        node.NE = new_node
                        new_node.Parent = node
                        break
                    node = node.NE
                elif newPoint[0] >= node.x and newPoint[1] < node.y : # SE region
                    if node.SE is None :
                        node.SE = new_node
                        new_node.Parent = node
                        break
                    node = node.SE
                elif newPoint[0] < node.x and newPoint[1] >= node.y : # NW region
                    if node.NW is None :
                        node.NW = new_node
                        new_node.Parent = node
                        break
                    node = node.NW
                else :                                                # SW region
                    if node.SW is None :
                        node.SW = new_node
                        new_node.Parent = node
                        break
                    node = node.SW
        self.nodeNum += 1
        return new_node
                    
    
    def searchNode(self, point):
        """
        Return the node for coordinates if the node is in the quad tree,
        or None otherwise.
        """
        node = self.root
        while node is not None :
            if point[0] == node.x and point[1] == node.y :   # Find!!
                return node
            elif point[0] >= node.x and point[1] >= node.y : # Go to NE region
                node = node.NE
            elif point[0] >= node.x and point[1] < node.y :  # Go to SE region
                node = node.SE
            elif point[0] < node.x and point[1] >= node.y :  # Go to NW region
                node = node.NW                                    
            else :                                           # Go to SW region
                node = node.SW
        return None


    def makeOptQT(self, lst):
        """Generate a balanced quad tree from the point list."""
        
        def median(x):
            if x % 2 == 0 : # x is even
                return (x/2 + x/2 + 1)/2
            else :          # x is odd 
                return (x + 1)/2

        points = lst[:]     # copy the list of points 
        if len(points) == 0 : return
        points.sort()
        point = points[median(len(points))-1]  # Extract median point 
        self.insertNode(point)
        points.remove(points[median(len(points))-1])

        # Make sub region's point list
        NE_points = [x for x in points if x[0] >= point[0] and x[1] >= point[1]] 
        SE_points = [x for x in points if x[0] >= point[0] and x[1] < point[1]]  
        NW_points = [x for x in points if x[0] < point[0] and x[1] >= point[1]]  
        SW_points = [x for x in points if x[0] < point[0] and x[1] < point[1]]  
        self.makeOptQT(NE_points)
        self.makeOptQT(SE_points)      
        self.makeOptQT(NW_points)
        self.makeOptQT(SW_points)
    

if __name__ == '__main__':
    
    qtree = QuadTree()
    lst = [(0,0), (-1,-2), (-3,4), (2,-5), (1,4), (-4,-6), (3,5), (2,2), (-4,1), (1, -10)]
    qtree.insertNode((-1, 6))
    qtree.insertNode((1, 2))
