x <- c(73,74,86,74,80,78,86,82,87,80)
y <- c(57,59,63,59,60,59,61,59,64,59)
u <- c(61,70,79,65,55,85,57,83,70,75)
v <- c(48,48,52,48,42,58,48,52,52,52)

#xy <- cor(scale(x),scale(y))
#xu <- cor(scale(x),scale(u))
#xv <- cor(scale(x),scale(v))
#yu <- cor(scale(y),scale(u))
#yv <- cor(scale(y),scale(v))
#uv <- cor(scale(u),scale(v))

#print(cor(scale(x),scale(u)))
#print(cor(scale(u),scale(x)))

#xy <- cor(x,y)
#xu <- cor(x,u)
#xv <- cor(x,v)
#yu <- cor(y,u)
#yv <- cor(y,v)
#uv <- cor(u,v)

#r11 <- rbind(c(1,xy),c(xy,1))
#r12 <- rbind(c(xu,xv),c(yu,yv))
#r21 <- rbind(c(xu,yu),c(xv,yv))
#r22 <- rbind(c(1,uv),c(uv,1))

#a <- solve(r11)%*%r12%*%solve(r22)%*%r21
#z <- eigen(a)
#print(z$values)

u1 <- matrix(c(scale(x),scale(y)),,2)
#u1 <- matrix(c(x,y),,2)
print(u1)
u2 <- matrix(c(scale(u),scale(v)),,2)
#u2 <- matrix(c(u,v),,2)
print(u2)
a<-var(u1,u2)%*%t(var(u1,u2))
print(a)
z <- eigen(a)
print(z$values)
print(z$vectors)

#print(cancor(u1,u2))
