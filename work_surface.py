import Part
from FreeCAD import Base
import numpy as np

class Work_Surface():
	"""  \n"""
	
	def __init__(self, wood_thickness, blinds_depth, blinds_height, surface_underside):
		""" """
		self.left_width 	  = 1020
		self.oven_width		  = 515
		self.total_width	  = 2770
		self.right_width	  = self.total_width - self.left_width - self.oven_width
		self.depth 			  = 605		# depth of the work surface
		self.thickness		  = wood_thickness
		self.blind_depth 	  = blinds_depth	# for blinds below work surface
		self.underside_height = surface_underside
		
		self.parts_left = {}
		self.parts_left['top'] = self.create_top_left()
		
		self.parts_right = {}
		self.parts_right['top'] = Part.makeBox(self.right_width, self.depth, self.thickness)
		
		self.make_blinds()
		
		self.parts_left['top'].Placement.Base = Base.Vector(0,0,self.thickness)
		self.move_parts(self.parts_left,0,0,self.underside_height)
		
		self.parts_right['top'].Placement.Base = Base.Vector(0,0,self.thickness)
		self.move_parts(self.parts_right,self.left_width + self.oven_width,0,self.underside_height)
		
		
		self.make_blinds_top(blinds_height)
		
		self.make_supports()
		
		self.parts_right['shelf'] = self.create_shelf()
		
		
		
		
	def create_top_left(self):
		plain_board = Part.makeBox(self.left_width, self.depth, self.thickness)
		
		# corner cut
		
		V1 = plain_board.Vertex2.Point
		V2 = plain_board.Vertex4.Point
		V3 = V2 + Base.Vector(560,0,0)
		cut_edge = Part.makePolygon([ V1,V2,V3,V1])		
		cut_edge = Part.Face(cut_edge)
		cut_edge = cut_edge.extrude(Base.Vector(0,0,self.thickness))
		
		
		# gas pipe cut
		
		V4 = V2 + Base.Vector(0,-250,0)
		V5 = V4 + Base.Vector(437.5,0,0)
		V6 = V5 + Base.Vector(0,-35,0)
		V7 = V4 + Base.Vector(0,-35,0)
		
		VC1 = V5 + Base.Vector(17.5,-17.5,0)
		
		L1 = Part.Line(V4,V5)
		C1 = Part.Arc(V5,VC1,V6)
		L2 = Part.Line(V6,V7)
		L3 = Part.Line(V7,V4)
		
		S1 = Part.Shape([C1,L1,L2,L3])

		opening = Part.Wire(S1.Edges)
		opening = Part.Face(opening)
		opening = opening.extrude(Base.Vector(0,0,self.thickness))
		
		top_left = plain_board.cut(cut_edge)
		top_left = top_left.cut(opening)
		
		return top_left
		
	def make_blinds(self):
		""" Make underside blinds for work surface left and right """
		
		def create_miter(Vertex1, Vertex2, Vertex3):
			miter = Part.makePolygon([ Vertex1,Vertex2,Vertex3,Vertex1])		
			miter = Part.Face(miter)
			miter = miter.extrude(Base.Vector(0,0,self.thickness))
			
			return miter
			
		
		# left side
		blind_front = Part.makeBox(self.left_width, self.blind_depth, self.thickness)
		blind_front = blind_front.common(self.parts_left['top'])
		
		V1 = blind_front.Vertex2.Point
		V2 = blind_front.Vertex6.Point
		V3 = V2 + Base.Vector(-self.blind_depth,0,0)
		
		
		blind_front = blind_front.cut(create_miter(V1,V2,V3))
		
		self.parts_left['blind front'] = blind_front
		
		blind_side = Part.makeBox(self.blind_depth, self.depth, self.thickness)
		blind_side.Placement.Base = Base.Vector(self.left_width-self.blind_depth, 0,0)
		blind_side = blind_side.cut(blind_front)
		
		self.parts_left['blind side'] = blind_side
		
		# right side
		blind_front = Part.makeBox(self.right_width, self.blind_depth, self.thickness)
		self.parts_right['blind front'] = blind_front
		
		V1 = blind_front.Vertex2.Point
		V2 = blind_front.Vertex4.Point
		V3 = V2 + Base.Vector(self.blind_depth,0,0)
		
		blind_front = blind_front.cut(create_miter(V1,V2,V3))
		self.parts_right['blind front'] = blind_front
		
		blind_side = Part.makeBox(self.blind_depth, self.depth, self.thickness)
		blind_side = blind_side.cut(blind_front)
		
		self.parts_right['blind side'] = blind_side
		
		
	def make_blinds_top(self, blinds_height):
		
		# Top 1
		V1 = self.parts_left['top'].Vertex3.Point
		V2 = self.parts_left['top'].Vertex11.Point
		alpha = np.arctan(560/605)
		move_x = self.thickness/np.cos(alpha)
		V3 = V2 + Base.Vector(move_x,0,0)
		V4 = V1 + Base.Vector(move_x,0,0)
		
		blind_top1 = Part.makePolygon([V1,V2,V3,V4,V1])
		blind_top1 = Part.Face(blind_top1)
		self.parts_left['blind_top1'] = blind_top1.extrude(Base.Vector(0,0,blinds_height))
		
		
		# Top 2
		V1 = self.parts_left['top'].Vertex16.Point
		V2 = self.parts_left['top'].Vertex13.Point
		V4 = V4 = V1 + Base.Vector(move_x,0,0)
		
		gamma = (np.pi-alpha)/2
		move_x = self.thickness/np.tan(gamma)
		V3 = V2 + Base.Vector(move_x, -self.thickness, 0)
		
		blind_top2 = Part.makePolygon([V1,V2,V3,V4,V1])
		blind_top2 = Part.Face(blind_top2)
		self.parts_left['blind_top2'] = blind_top2.extrude(Base.Vector(0,0,blinds_height))
		
		# Top 3
		V1 = V2
		V4 = V3
		V2 = self.parts_left['top'].Vertex12.Point
		V3 = V2 + Base.Vector(0,-self.thickness,0)
		
		blind_top3 = Part.makePolygon([V1,V2,V3,V4,V1])
		blind_top3 = Part.Face(blind_top3)
		self.parts_left['blind_top3'] = blind_top3.extrude(Base.Vector(0,0,blinds_height))
		
		# Top 4 (right work surface)
		V1 = self.parts_right['top'].Vertex3.Point
		V2 = self.parts_right['top'].Vertex7.Point
		V3 = V2 + Base.Vector(-self.thickness, -self.thickness, 0)
		V4 = V1 + Base.Vector(0,-self.thickness,0)
		
		blind_top4 = Part.makePolygon([V1,V2,V3,V4,V1])
		blind_top4 = Part.Face(blind_top4)
		self.parts_right['blind_top4'] = blind_top4.extrude(Base.Vector(0,0,blinds_height))
		
		
		# Top 5 (right works surface)
		V1 = V2
		V2 = self.parts_right['top'].Vertex5.Point
		V4 = V3
		V3 = V2 + Base.Vector(-self.thickness, 0, 0)
		
		blind_top5 = Part.makePolygon([V1,V2,V3,V4,V1])
		blind_top5 = Part.Face(blind_top5)
		self.parts_right['blind_top5'] = blind_top5.extrude(Base.Vector(0,0,blinds_height))
		
	def make_supports(self):
		self.pos_support1 = self.parts_left['top'].Vertex2.Point + Base.Vector(-(self.blind_depth + 30), (self.blind_depth + 30),0)
		
		self.pos_support2 = self.parts_right['top'].Vertex2.Point + Base.Vector((self.blind_depth + 30), (self.blind_depth + 30),0)
		
		self.pos_support3 = self.parts_right['top'].Vertex6.Point + Base.Vector(-(self.blind_depth + 30), (self.blind_depth + 30),0)
		
		self.parts_left['support1'] = Part.makeBox(self.thickness, self.thickness, self.underside_height, self.pos_support1, Base.Vector(0,0,-1))
		self.parts_right['support2'] = Part.makeBox(self.thickness, self.thickness, self.underside_height, self.pos_support2 + Base.Vector(self.thickness, 0,0), Base.Vector(0,0,-1))
		self.parts_right['support3'] = Part.makeBox(self.thickness, self.thickness, self.underside_height, self.pos_support3, Base.Vector(0,0,-1))
				
		
	def create_shelf(self):
		shelf_width = self.pos_support3[0]-self.pos_support2[0]
		shelf_depth = self.depth - self.pos_support2[1]
		shelf_height = self.underside_height / 2
		
		shelf = Part.makeBox(shelf_width, shelf_depth, self.thickness, Base.Vector(self.pos_support2[0], self.pos_support2[1], shelf_height)) 
		shelf = shelf.cut(self.parts_right['support2'])
		shelf = shelf.cut(self.parts_right['support3'])
		
		return shelf
		
		
	def move_parts(self, parts, move_x, move_y, move_z):
		for key in parts:
			original_pos = parts[key].Placement.Base
			print(original_pos)
			parts[key].Placement.Base = Base.Vector(move_x, move_y, move_z) + original_pos
			print(parts[key].Placement.Base)
			
