data = read.csv('malware.csv', header=FALSE);
names(data)
names(data) <- c("Time","Url","Ip","Hostname","Malware","DomainOwner","As","H","Country")
data[1:4,]
summary(data)

data = data[,c(1,2,3,5,9)]
dim(data)

summary(data)

data2 = data[data[,2] != '-',]
summary(data2)
dim(data2)

#set malware true
data2[,4] = 'Yes'
data2[,4]

summary(data2)
write.csv(data2, file = "malware_clean.csv")


alexa = read.csv('alexa1m.csv',header=FALSE)

names(alexa)

names(alexa) <- c("Id","Domain Name")

##get 1000 thousand random domain from the data

mysample <- alexa[sample(1:nrow(alexa), 1000,replace=FALSE),]

mysample 

write.csv(mysample, file='alexa_1000_sampled.csv')


###After pre-liminary preprocessing

##Load the parsed malicious urls


mal = read.csv('malware_clean.csv', fileEncoding="latin1");
keeps <- c("Time","Url","Ip","Malware","Country");
mal = mal[keeps]

trust = read.csv('alexa_1000_ip_fixed.csv', fileEncoding="latin1");
names(trust) <- c("Time","Url","Ip","Malware","Country");

allDataset = rbind(mal,trust);
summary(allDataset);

write.csv(allDataset, file = "allDataSet.csv")

dataset = read.csv('test1.csv', fileEncoding="latin1");

summary(dataset)

names(dataset)

dataset1 = dataset[,c("Id","Malware","Url_length","Is_Sub_Domain","Who_is_score")]

summary(dataset1)

library(e1071)
dataset = dataset1;
index <- 1:nrow(dataset);
testindex <- sample(index, trunc(length(index)*30/100));
testset <- dataset[testindex,];
trainset <- dataset[-testindex,];


tuned <- tune.svm(Malware~., data = trainset, gamma = 10^(-6:-1), cost = 10^(-1:1))

dataset = dataset1
index <- 1:nrow(dataset)
testindex <- sample(index, trunc(length(index)/3))
testset <- dataset[testindex,]
trainset <- dataset[-testindex,]

model <- svm(Malware~., data = trainset)
prediction <- predict(model, testset)
tab <- table(pred = prediction, true = testset[,1])
ta




