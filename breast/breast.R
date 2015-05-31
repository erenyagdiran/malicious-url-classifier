dataset<- read.csv('breast/wdbc.data', head = FALSE)

index <- 1:nrow(dataset)
testindex <- sample(index, trunc(length(index)*30/100))
testset <- dataset[testindex,]
trainset <- dataset[-testindex,]

tuned <- tune.svm(V2~., data = trainset, gamma = 10^(-6:-1), cost = 10^(-1:1))

model  <- svm(V2~., data = trainset, kernel = "radial", gamma = 0.001, cost = 10)

prediction <- predict(model, testset[,-2])
tab <- table(pred = prediction, true = testset[,2])
tab

names(dataset)

plot(model,dataset,V3~V4)

dataset2 <- read.csv('test1.csv')
dataset2 <- dataset2[,c("Id","Malware","Url_length","Is_Sub_Domain","Who_is_score")]
summary(dataset2)
dataset = dataset2

index <- 1:nrow(dataset)
testindex <- sample(index, trunc(length(index)*30/100))
testset <- dataset[testindex,]
trainset <- dataset[-testindex,]

tuned <- tune.svm(Malware~., data = trainset, gamma = 10^(-6:-1), cost = 10^(-1:1))

model  <- svm(Malware~., data = trainset, kernel = "linear", gamma = 0.05, cost = 10) 

prediction <- predict(model, testset[,-2])
tab <- table(pred = prediction, true = testset[,2])
tab

names(dataset)

plot(model,dataset,Is_Sub_Domain~Who_is_score)

