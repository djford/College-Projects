"""
 This program takes several different object classes and adds them together
 to create the game of pong. The user clicks on the screen to move the paddle
 object in order to prevent the ball object from reaching the right side of
 the window. The more the ball hits the paddle the faster the ball will go.
 
 
 (@author Daniel Ford 2012)
 
"""
from time import sleep
from random import randrange, random
from graphics import *
from Ball import Ball
from Paddle import Paddle

class Pong:

        def __init__(self, win):
                
                
                self.ball = Ball(win)
                
                
                
                self.paddle = Paddle(win)
               
                
                
                self.text = Text(Point(250, 40),"0" )
                self.text.draw(win)

                self.text2 = Text (Point(150,10),"Click the screen to move the paddle.")
                self.text2.draw(win)

                self.text3 = Text (Point(100, 40),"1" )
                self.text3.draw(win)

                self.text4 = Text (Point(210, 40),"Score: ")
                self.text4.draw(win)

                self.text5 = Text (Point(60, 40),"Level: ")
                self.text5.draw(win)


        def checkContact(self):
                # lower end of the paddle
                lower = self.paddle.pad.getP1().getY()
                # upper end of the paddle
                upper = self.paddle.pad.getP2().getY()
                # edge of the ball
                ballEdge = self.ball.getCenter().getY()
                # side edge of the ball hits the paddle
                if self.ball.getCenter().getX()+self.ball.getRadius()>self.paddle.getFront():
                        # upper edge of the ball does not pass the ends of the paddle
                        if  upper <= ballEdge <= lower:
                                self.ball.reverseX()
                        return True
                else:
                        return False


        def gameOver(self):
                # ball does not hit the front of the paddle
                if self.ball.getCenter().getX()>self.paddle.getFront():
                        return True
                else:
                        return False
                


        def play(self, win):
                # sets number of hits
                count = 0
                level = 1
                # runs until the game is not over
                while self.gameOver() == False:
                        pt = win.checkMouse()
                        if pt!=None:
                                self.paddle.paddleMove(pt)
                        self.ball.move(win)
                        if self.checkContact() == True:
                                # adds number of hits
                                count += 1
                                # changes the score
                                self.text.setText(count)
                                # when the ball hits the paddle 5 times
                                if (count % 5 == 0):
                                        # increases the level
                                        level += 1
                                        # changes the level
                                        self.text3.setText(level)
                                        # makes the ball go faster
                                        self.ball.goFaster()
                        sleep(0.05)
                # closes the window once the game is over
                win.close()
                print ("Game Over")
                print (count)
                
                

                        


def main():
        w = 300
        h = 300
        pWin = GraphWin("Pong", w, h )

        po = Pong(pWin)
        po.play(pWin)

if __name__ == '__main__':
        main()
                        
        
