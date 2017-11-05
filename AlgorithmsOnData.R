#install packages if they are not installed
if(!require("tree")) install.packages("tree")
if(!require("rpart")) install.packages("rpart")
if(!require("party")) install.packages("party")
if(!require("C50")) install.packages("C50")
if(!require("caret")) install.packages("caret")
if(!require("e1071")) install.packages("e1071")
if(!require("ROCR")) install.packages("ROCR")

#read dataset
setwd("C:/Users/alber/Desktop/Hackathon/TrainingData")

# function definitions to simplify ROC curve drawing and AUC calculation
plotROC <-function (pred_probs, ...)
{
  pred_obj<-prediction(pred_probs, cc_test$NewBusiness)
  perf<-performance(pred_obj, measure="tpr",x.measure="fpr")
  plot(perf, ...)
}

calculateAUC <-function (pred_probs)
{
  pred_obj<-prediction(pred_probs, cc_test$NewBusiness)
  auc_obj<-performance(pred_obj, "auc")
  auc_obj@y.values[[1]]
}

# Read the dataset and remove missing values
CC=read.csv("CC_Data.csv")
cc = na.omit(CC)

# Splitting Data.

set.seed(6201)
dtype<-sample(2,nrow(cc),replace=TRUE,prob=c(0.7,0.3))
#dtype=1 : training set dtype=2: test set
sum(dtype==1) # size of training set
sum(dtype==2) # size of test set

cc_train <- cc[dtype==1,]
cc_test <- cc[dtype==2,]

# We're going to first use the "tree" package.
attach(cc_train)
library(tree)
tree.fit<-tree(NewBusiness~Age+Credit_Debit+Bank+Money, data=cc_train)
summary(tree.fit)
print(tree.fit)
plot(tree.fit)
text(tree.fit,pretty=0)
library(caret)
confusionMatrix(table(predict(tree.fit,type="Bank",cc_train),cc_train$NewBusiness))
tree_pred<-predict(tree.fit, type="Bank",cc_test)
confusionMatrix(table(tree_pred,cc_test$NewBusiness))

library(ROCR)
tree_probs<-(predict(tree.fit, type="vector",cc_test))[,2]
plotROC(tree_probs, colorize=TRUE)
abline(a=0,b=1)
calculateAUC(tree_probs)

tree.fit2<-tree(NewBusiness~Age+Credit_Debit+Bank+Money, split="gini", data=cc_train)
summary(tree.fit2)
print(tree.fit2)
plot(tree.fit2)
text(tree.fit2,pretty=0)
confusionMatrix(table(predict(tree.fit2,type="Bank",cc_train),cc_train$NewBusiness))
tree_pred2<-predict(tree.fit2, type="Bank",cc_test)
confusionMatrix(table(tree_pred2,cc_test$NewBusiness))

tree_probs2<-(predict(tree.fit2, type="vector",cc_test))[,2]
plotROC(tree_probs2, colorize=TRUE)
abline(a=0,b=1)
calculateAUC(tree_probs2)

# Another package for decision tree Bankifiers
library(rpart)
rpart.fit<-rpart(NewBusiness~Age+Credit_Debit+Bank+Money, data=cc_train, parms=list(split="information"))
summary(rpart.fit)
print(rpart.fit)
plot(rpart.fit)
text(rpart.fit, use.n=T)
confusionMatrix(table(predict(rpart.fit,type="Bank",cc_train),cc_train$NewBusiness))
rpart_pred<-predict(rpart.fit,type="Bank",cc_test)
confusionMatrix(table(rpart_pred,cc_test$NewBusiness))
rpart_probs<-(predict(rpart.fit, type="prob",cc_test))[,2]
plotROC(rpart_probs, colorize=TRUE)
abline(a=0,b=1)
calculateAUC(rpart_probs)

# Yet another package for decision tree Bankifers
library(party)
ctree.fit<-ctree(NewBusiness~Age+Credit_Debit+Bank+Money, data=cc_train)
ctree.fit
summary(ctree.fit)
plot(ctree.fit)
confusionMatrix(table(predict(ctree.fit,type="response",cc_train),cc_train$NewBusiness))
ctree_pred<-predict(ctree.fit,type="response",cc_test)
confusionMatrix(table(ctree_pred,cc_test$NewBusiness))
ctree_probs<-unlist(lapply(predict(ctree.fit, type="prob", cc_test), `[[`,2))
plotROC(ctree_probs, colorize=TRUE)
abline(a=0,b=1)
calculateAUC(ctree_probs)

# This is an improved version of the popular ID3/C4.5 algorithms.
library(C50)
see5.fit<-C5.0(NewBusiness~Age+Credit_Debit+Bank+Money, data=cc_train)
summary(see5.fit)
plot(see5.fit)
confusionMatrix(table(predict(see5.fit,type="Bank",cc_train),cc_train$NewBusiness))
see5_pred<-predict(see5.fit,type="Bank",cc_test)
confusionMatrix(table(see5_pred,cc_test$NewBusiness))
see5_probs<-(predict(see5.fit, type="prob",cc_test))[,2]
plotROC(see5_probs, colorize=TRUE)
abline(a=0,b=1)
calculateAUC(see5_probs)


# Predictions using other Bankifers we've learned before.
glm.fit<-step(glm(NewBusiness~Age+Credit_Debit+Bank+Money,family=binomial, 
                  data=cc_train), direction="both")
library(MASS)
lda.fit<-lda(NewBusiness~Age+Credit_Debit+Bank, data=cc_train)
qda.fit<-qda(NewBusiness~Age+Credit_Debit+Bank, data=cc_train)

library(e1071)
bayes.fit<-naiveBayes(NewBusiness~Age+Credit_Debit+Bank,data=cc_train)


# for KNN
contrasts(Credit_Debit)
contrasts(Bank)
library(Bank)
attach(cc_train)
Credit_DebitMale<-ifelse(Credit_Debit=="Male", 1, 0)
Bank2nd<-ifelse(Bank=="2nd",1,0)
Bank3rd<-ifelse(Bank=="3rd",1,0)
Xvar_train<-cbind(Age, Credit_DebitMale, Bank2nd, Bank3rd)
attach(cc_test)
Credit_DebitMale<-ifelse(Credit_Debit=="Male", 1, 0)
Bank2nd<-ifelse(Bank=="2nd",1,0)
Bank3rd<-ifelse(Bank=="3rd",1,0)
Xvar_test<-cbind(Age, Credit_DebitMale, Bank2nd, Bank3rd)
set.seed(1)
knn.fit<-knn(Xvar_train,Xvar_test,cc_train$NewBusiness,k=3, prob = TRUE)

# probabilities and Bankification results for evaluation and ROC drawing
contrasts(NewBusiness)
glm_probs <- predict(glm.fit, cc_test,type="response")
glm_pred <- ifelse(glm_probs>0.5, "Survived", "Died")
plotROC(glm_probs, colorize=TRUE)
calculateAUC(glm_probs)

lda_pred <- predict(lda.fit, cc_test)
lda_probs <- lda_pred$posterior[,2]
qda_pred <- predict(qda.fit, cc_test)
qda_probs <- qda_pred$posterior[,2]
bayes_pred<-predict(bayes.fit,cc_test)
bayes_probs<-(predict(bayes.fit, type="raw", cc_test))[,2]
knn_probs<- ifelse(knn.fit=="Survived", attr(knn.fit,"prob"), 1-attr(knn.fit,"prob"))


#Evaluation metrics and ROC curves for all Bankifiers
library(caret)
confusionMatrix(table(glm_pred, cc_test$NewBusiness))
confusionMatrix(table(lda_pred$Bank, cc_test$NewBusiness))
confusionMatrix(table(qda_pred$Bank, cc_test$NewBusiness))
confusionMatrix(table(bayes_pred, cc_test$NewBusiness))
confusionMatrix(table(knn.fit, cc_test$NewBusiness))
confusionMatrix(table(tree_pred, cc_test$NewBusiness))
confusionMatrix(table(tree_pred2, cc_test$NewBusiness))
confusionMatrix(table(ctree_pred, cc_test$NewBusiness))
confusionMatrix(table(rpart_pred, cc_test$NewBusiness))
confusionMatrix(table(see5_pred, cc_test$NewBusiness))

plotROC(glm_probs)
abline(a=0,b=1)
calculateAUC(glm_probs)
plotROC(lda_probs, add=TRUE, col="red")
calculateAUC(lda_probs)
plotROC(qda_probs, add=TRUE, col="blue")
calculateAUC(qda_probs)
plotROC(bayes_probs, add=TRUE, col="cyan")
calculateAUC(bayes_probs)
plotROC(knn_probs, add=TRUE, col="green")
calculateAUC(knn_probs)
plotROC(tree_probs, add=TRUE, col="navy")
calculateAUC(tree_probs)
plotROC(tree_probs2, add=TRUE, col="azure")
calculateAUC(tree_probs2)
plotROC(ctree_probs, add=TRUE, col="purple")
calculateAUC(ctree_probs)
plotROC(rpart_probs, add=TRUE, col="orange")
calculateAUC(rpart_probs)
plotROC(see5_probs, add=TRUE, col="brown")
calculateAUC(see5_probs)

