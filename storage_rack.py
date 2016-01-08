import Part
from FreeCAD import Base
import numpy as np


class Storage_Rack():
	"""\n This class shall be used .... \n"""

	def __init__(self, rack_width, rack_height, rack_depth, wood_thickness, num_shelves):
		self.width     = rack_width
		self.height    = rack_height
		self.depth	   = rack_depth 
		self.thickness = wood_thickness
		self.shelves   = num_shelves

		self.create_rack()

	def create_rack(self):
		self.parts = {}
		self.parts['bottom shelf'] = self.create_board(self.width, self.depth, self.thickness)
		self.parts['top shelf'] = self.parts['bottom shelf'].mirror(Base.Vector(0,0,self.height/2), Base.Vector(0,0,1))

		self.parts['left side'] = self.create_board(self.height, self.depth, self.thickness)
		self.parts['left side'].rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),270)
		self.parts['left side'].rotate(Base.Vector(0,self.depth/2,0), Base.Vector(0,0,1),180)

		self.parts['right side'] = self.parts['left side'].mirror(Base.Vector(self.width/2, 0,0), Base.Vector(1,0,0))
		
		self.make_shelves()
		
	def make_shelves(self):
		
		if self.shelves >= 1:
			for i in range(1,self.shelves+1):
				shelf_name = 'shelf '+str(i)
				dowel_name = 'dowel '+str(i)
				move_z = i*self.height/(self.shelves+1)
				self.parts[shelf_name] = Part.makeBox(self.width-2*self.thickness, self.depth, self.thickness)
				self.parts[shelf_name].Placement.Base = Base.Vector(self.thickness, 0, move_z-self.thickness/2)

				# create dowels (4 pieces)

				dowel_length = 20
				dowel_radius = 4
				drill_length = dowel_length + 4

				dowel = Part.makeCylinder(dowel_radius,dowel_length,Base.Vector(0,0,0),Base.Vector(1,0,0), 360)
				dowel = dowel.makeChamfer(1,[dowel.Edge1,dowel.Edge3])
				dowel.Placement.Base = Base.Vector(self.thickness-dowel_length/2, 50, move_z)
				dowel2 = dowel.mirror(Base.Vector(0,self.depth/2,0), Base.Vector(0,1,0))
				dowel = dowel.fuse(dowel2)
				dowel2 = dowel.mirror(Base.Vector(self.width/2,0,0), Base.Vector(1,0,0))
				dowel = dowel.fuse(dowel2)
				self.parts[dowel_name] = dowel 

				# drill for the dowels
				drill = Part.makeCylinder(dowel_radius,drill_length,Base.Vector(0,0,0),Base.Vector(1,0,0), 360)
				drill.Placement.Base = Base.Vector(self.thickness-drill_length/2, 50, move_z)
				drill2 = drill.mirror(Base.Vector(0,self.depth/2,0), Base.Vector(0,1,0))
				drill = drill.fuse(drill2)
				drill2 = drill.mirror(Base.Vector(self.width/2,0,0), Base.Vector(1,0,0))
				drill = drill.fuse(drill2)

				self.parts['left side'] = self.parts['left side'].cut(drill)
				self.parts['right side'] = self.parts['right side'].cut(drill)
				self.parts[shelf_name] = self.parts[shelf_name].cut(drill)


	def create_board(self, board_width, board_depth, board_thickness):
		board = Part.makeBox(board_width, board_depth, board_thickness)

		V1 = Base.Vector(0,0,0)
		V2 = Base.Vector(0,0,board_thickness)
		V3 = Base.Vector(board_thickness,0,board_thickness)
		miter_left = Part.makePolygon([ V1,V2,V3,V1])
		miter_left = Part.Face(miter_left)
		miter_left = miter_left.extrude(Base.Vector(0,board_depth,0))

		miter_right = miter_left.mirror(Base.Vector(board_width/2,0,0), Base.Vector(1,0,0))

		miter = miter_left.fuse(miter_right)

		return board.cut(miter)
		
	def move_board(self, move_x, move_y, move_z):
		for key in self.parts:
			original_pos = self.parts[key].Placement.Base
			self.parts[key].Placement.Base = Base.Vector(move_x, move_y, move_z) + original_pos

