import sys
import time
from mcpi.minecraft import Minecraft

mc = Minecraft.create()

def fill(blk=0,act=0,a=5,b=5,c=3):
	x, y, z = mc.player.getPos()
	for i in range(a):
		for j in range(b):
			for k in range(c):
				mc.setBlock(x+i, y+k, z+j, blk, act)
