#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Main module
"""
from lxml import etree
import svgwrite
import math

class MODE:
   POLYLINE=0
   LINE=1

def readpathfile(fn):
   energies = []
   tree = etree.parse(fn)
   for e in tree.xpath("/energies/energy/val"):
      print(e.text)
      energies.append(float(e.text))
   return energies

def generate_path(energies, mode=MODE.LINE):
   dx=10
   prev_x=0
   prev_y=float('nan')
   dwg = svgwrite.Drawing('path.svg', size=('297mm', '210mm'), profile='tiny')
   lines = []
   polyline = dwg.polyline(points=[], stroke='green', fill='none', stroke_width=0.1)
   for e in energies:
      if not(math.isnan(prev_y)):
         new_x=prev_x+dx
         new_y=-e
         print(prev_x, prev_y, new_x, new_y)
#         dwg.add(dwg.line((prev_x, prev_y), (new_x, new_y), stroke=svgwrite.rgb(5, 50, 16, '%')))
         lines.append(dwg.line((prev_x, prev_y), (new_x, new_y), stroke=svgwrite.rgb(5, 50, 16, '%'), stroke_linecap='round'))
         polyline.points.append((prev_x, prev_y))
         polyline.points.append((new_x, new_y))
         prev_x=new_x
         prev_y=new_y
      new_x=prev_x+dx
      new_y=-e
      prev_y=new_y
#      dwg.add(dwg.line((prev_x, prev_y), (new_x, new_y), stroke=svgwrite.rgb(10, 10, 16, '%')))
      lines.append(dwg.line((prev_x, prev_y), (new_x, new_y), stroke=svgwrite.rgb(10, 10, 16, '%'), stroke_linecap='round'))
      polyline.points.append((prev_x, prev_y))
      polyline.points.append((new_x, new_y))
      prev_x=new_x
   if (mode==MODE.LINE):
      for l in lines:
         dwg.add(l)
   elif (mode==MODE.POLYLINE):
      dwg.add(polyline)
   dwg.save()
   
def main():
   """
   Main routine
   """
   energies = readpathfile("path.xml")
   generate_path(energies)

if __name__ == '__main__':
    main()
