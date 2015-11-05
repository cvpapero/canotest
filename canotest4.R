x <- c(73,74,86,74,80,78,86,82,87,80)
y <- c(57,59,63,59,60,59,61,59,64,59)
u <- c(61,70,79,65,55,85,57,83,70,75)
v <- c(48,48,52,48,42,58,48,52,52,52)

#cat("ave")
#print(sum(x)/10)
#cat("var")
#print(var(x))

#rxy <- cor(scale(x),scale(y))
#rxu <- cor(scale(x),scale(u))
#rxv <- cor(scale(x),scale(v))
#ryu <- cor(scale(y),scale(u))
#ryv <- cor(scale(y),scale(v))
#ruv <- cor(scale(u),scale(v))

#r11 <- matrix(c(1,rxy,rxy,1),2,2)
#r12 <- matrix(c(rxu,ryu,rxv,ryv),2,2)
#r21 <- matrix(c(rxu,rxv,ryu,ryv),2,2)
#r22 <- matrix(c(1,ruv,ruv,1),2,2)

#a <- solve(r11)%*%r12%*%solve(r22)%*%r21
#cat("a")
#print(a)
#z <- eigen(a)
#cat("eigen")
#print(z) 

f <- matrix(c(x,y),,2)
g <- matrix(c(u,v),,2)

#f <- data.frame(x,y)
#g <- data.frame(u,v)

#print(f)
#print(g)
#vm <- var(f,g)
#print(vm) 

#b <- vm%*%t(vm)

#print(b)
#print(eigen(b))

cca<-cancor(f,g)
print(cca)
#of <- fm%*%cca$xcoef
#og <- gm%*%cca$ycoef
#print(of)
#print(og)
