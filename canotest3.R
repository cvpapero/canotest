x1 <- c(220,230,240,240,250,260,260,260,270,280)
x2 <- c(110,150,150,250,200,150,250,290,250,290)
x3 <- c(0,1,2,1,3,3,2,1,4,4)

#x12 <- cor(scale(x1),scale(x2))
#x13 <- cor(scale(x1),scale(x3))
#x23 <- cor(scale(x2),scale(x3))


u1 <- matrix(c(x1,x2),,2)
u2 <- matrix(c(x3),,1)

print(cancor(u1,u2))