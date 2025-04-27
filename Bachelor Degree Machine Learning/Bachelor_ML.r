####STEP 0: preprocessing e divisione dataset####
options(scipen = 999, digits = 3)
setwd("/Users/federicoclerici/Documents/Unimib/Terzo anno/Data mining e machine learning/progetto ML")
b <- read.csv("in-vehicle-coupon-recommendation.csv", sep=",", dec = ".", stringsAsFactors=TRUE, na.strings=c("NA","NaN", "", "Unknown ", "Unknown"))
b[,-4]<-lapply(b[,-4],as.factor)
library(car)
b$Y<-recode(b$Y, recodes="1='c0'; else='c1'") #ricodifica target

#nzv
library(caret)
a<-nzv(b)
colnames(b[a])
b<-b[-a] #abbiamo rimosso la variabile "toCoupon_GEQ5min" in quanto ha zero variance

#collinearità
library(dplyr)
library(plyr)
b_fac <- b[,20:24]%>% dplyr::select_if(is.factor)
options(max.print=2500)
combos <- combn(ncol(b_fac),2)
adply(combos, 2, function(x) {
  test <- chisq.test(b_fac[, x[1]], b_fac[, x[2]])
  tab  <- table(b_fac[, x[1]], b_fac[, x[2]])
  out <- data.frame("Row" = colnames(b_fac)[x[1]]
                    , "Column" = colnames(b_fac[x[2]])
                    , "Chi.Square" = round(test$statistic,3)
                    , "df"= test$parameter
                    , "p.value" = round(test$p.value, 3)
                    , "n" = sum(table(b_fac[,x[1]], b_fac[,x[2]]))
                    , "u1" =length(unique(b_fac[,x[1]]))-1
                    , "u2" =length(unique(b_fac[,x[2]]))-1
                    , "nMinu1u2" =sum(table(b_fac[,x[1]], b_fac[,x[2]]))* min(length(unique(b_fac[,x[1]]))-1 , length(unique(b_fac[,x[2]]))-1) 
                    , "Chi.Square norm"  =test$statistic/(sum(table(b_fac[,x[1]], b_fac[,x[2]]))* min(length(unique(b_fac[,x[1]]))-1 , length(unique(b_fac[,x[2]]))-1)) 
  )
  
  
  return(out)
  
})
b <- subset(b, select = -c(direction_opp)) #rimozione variabile collineare "direction_opp"

#missing values
library(VIM)
library(mice)
missingness<- aggr(b[,-23], col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, labels=names(b[,-25]), cex.axis=.7,gap=3)
#rimozione variabile "car" con troppi missing
b <- subset(b, select = -c(car))
covdata=b[,c("Bar", "CoffeeHouse", "CarryAway", "RestaurantLessThan20","Restaurant20To50")]
#imputazione dati mancanti
tempData <- mice(covdata, m=1, maxit=20, meth='pmm', seed=500)
df_imputed <- complete(tempData,1)
b[,c("Bar","CoffeeHouse","CarryAway", "RestaurantLessThan20","Restaurant20To50")]<-df_imputed
sapply(b, function(x)(sum(is.na(x))))

#model selection con Boruta
library(Boruta)
set.seed(1234)
boruta.train <- Boruta(Y~., data = b, doTrace = 1)

plot(boruta.train, xlab = "features", xaxt = "n", ylab="MDI") #teniamo tutte le covariate

#divisione dataset
library(caret)
set.seed(1234)
Trainindex <- createDataPartition(y = b$Y, p = .90, list = FALSE)
a <- b[ Trainindex,]
score  <- b[-Trainindex,]
set.seed(1234)
Trainindex <- createDataPartition(y = a$Y, p = .66, list = FALSE)
train <- a[ Trainindex,]
test  <- a[-Trainindex,]

library(caret)
rm(a)
rm(covdata)
rm(df_imputed)
rm(missingness)
rm(Trainindex)
rm(tempData)
rm(combos)
rm(b_fac)

###fine preprocess
####STEP 1: tuning modelli####
library(pROC)
library(caret)
metric<-"Sens"

#LOGISTICO
set.seed(1234)

fit <- glm(Y~. , data=train, family="binomial")
summary(fit)

#facciamo model selection con stepAIC
library(MASS)
step <- stepAIC(fit, direction="both")

control <- trainControl(method= "cv",number=10, summaryFunction = twoClassSummary, classProbs = TRUE ,savePrediction = TRUE)
glm=train(Y ~ destination + passanger + weather + time + coupon + expiration + 
            gender + age + maritalStatus + education + occupation + income + 
            Bar + CoffeeHouse + RestaurantLessThan20 + Restaurant20To50 + 
            toCoupon_GEQ25min + direction_same,data=train, method = "glm", preProcess=c("corr", "nzv"),metric=metric,
           trControl = control, tuneLength=5, trace=FALSE)
getTrainPerf(glm)
pred_probrO=predict(glm,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#RIDGE (performa meglio di Lasso)
set.seed(1234)
control <- trainControl(method="cv", number = 10, classProbs = T,savePrediction = TRUE, summaryFunction=twoClassSummary)
tunegrid <- expand.grid(.alpha=0,.lambda=seq(0, 1, by = 0.001))
ridge<-train(Y ~ .,data=train, method = "glmnet",trControl = control, tuneLength=10, metric=metric,tuneGrid=tunegrid)
getTrainPerf(ridge)
pred_probrO=predict(ridge,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#NAIVE BAYES
set.seed(1234)
ctrl =trainControl(method="cv", number = 10, classProbs = T,   summaryFunction=twoClassSummary,savePrediction = TRUE)
naivebayes =train(Y~., data=train,method = "naive_bayes",metric=metric,
                  trControl = ctrl, tuneLength=5)
getTrainPerf(naivebayes)
pred_probrO=predict(naivebayes,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#PLS
set.seed(1234)
control=trainControl(method= "cv",number=10, classProbs=TRUE, summaryFunction=twoClassSummary, savePrediction = TRUE)
pls2=train(Y~. , data=train , method = "pls", metric = metric, preProcess = c("scale", "BoxCox"),
           trControl = control, tuneLength=5)
getTrainPerf(pls2)
pred_probrO=predict(pls2,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#Rpart
set.seed(1234)
ctrl <- trainControl(method = "cv" , number=10, summaryFunction = twoClassSummary , classProbs = TRUE,savePrediction = TRUE)
rpartTune<- train(Y ~ ., data = train, method = "rpart", tuneLength = 20,trControl=ctrl, metric = metric)
getTrainPerf(rpartTune)
pred_probrO=predict(rpartTune,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

plot(varImp(rpartTune))

#costruiamo albero da plottare con cp suggerito da Caret
library(rpart)
library(rpart.plot)
cv.caret <- rpart(Y ~ ., data = train, method = "class", 
                  cp = 0.00108, xval = 5)

rpart.plot(cv.caret, type = 4, extra = 1)

#C5.0
set.seed(1234)
control <- trainControl(method="cv", number=10, summaryFunction = twoClassSummary, classProbs = TRUE,savePrediction = TRUE)
c5 <- train(Y ~ ., data = train, method = "C5.0Tree", trControl = control, metric = metric, verbose=FALSE)
getTrainPerf(c5)
pred_probrO=predict(c5,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#BAGGED TREE
set.seed(1234)
control <- trainControl(method="cv", number=10, summaryFunction = twoClassSummary, classProbs = TRUE,savePrediction = TRUE)
tree_cart <- train(Y ~ ., data = train, B=500, method = "treebag", trControl = control, metric = metric, verbose=FALSE) 
getTrainPerf(tree_cart)
pred_probrO=predict(tree_cart,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#RANDOM FOREST
set.seed(1234)
control <- trainControl(method="cv", number=10, search="grid", summaryFunction = twoClassSummary, classProbs = TRUE ,savePrediction = TRUE)
tunegrid <- expand.grid(.mtry=c(1:5))
ranfor <- train(Y~., data=train, method="rf", tuneGrid=tunegrid, metric=metric, trControl=control, ntree=300)
getTrainPerf(ranfor)
pred_probrO=predict(ranfor,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#GRADIENT BOOSTING
set.seed(24) #seed con performance migliori
control <- trainControl(method="cv", number=10, summaryFunction = twoClassSummary, classProbs = TRUE,savePrediction = TRUE)
gradient_boost <- train(Y ~ ., data = train, method = "gbm", trControl = control, metric = metric, verbose=FALSE) 
getTrainPerf(gradient_boost)
pred_probrO=predict(gradient_boost,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)

#NEURAL NETWORK (model selection con Rpart: teniamo 10 var. con varImp>20)
set.seed(1234)
control <- trainControl(method="cv", number=10,  classProbs = TRUE, summaryFunction = twoClassSummary, search = "grid")
tunegrid <- expand.grid(size=c(1:5), decay=c(0.05, 0.1, 0.3, 0.5, 0.75))
nnetFit_CV <- train(train[,c("coupon","expiration","CoffeeHouse","toCoupon_GEQ25min","destination","temperature","time","Bar","weather","direction_same")], train$Y,
                    method = "nnet",
                    metric = metric,
                    tuneLength = 10,
                    preProcess = c("scale"),
                    trControl=control,
                    trace = T,
                    maxit = 500)
getTrainPerf(nnetFit_CV)
pred_probrO=predict(nnetFit_CV,newdata=test,type=c("prob"))[,1]
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)


####STEP 2: assessment modelli####

#costruzione box-plot ROC, Sens e Spec
results <- resamples(list(glm=glm, pls=pls2, ridge=ridge, C5.0=c5, gradient_boost=gradient_boost, naive_bayes=naivebayes,decisionTree=rpartTune,treebag=tree_cart, nnet=nnetFit_CV, randomF=ranfor))
par(mfrow=c(1,3))
bwplot(results)
par(mfrow=c(1,1))

#costruzione curva ROC
library(ROCR)
models=list("glm"=glm, "pls"=pls2, "ridge"=ridge, "C5.0"=c5, "gradient_boost"=gradient_boost, "naive_bayes"=naivebayes,"decisionTree"=rpartTune,"treebag"=tree_cart, "nnet"=nnetFit_CV, "randomF"=ranfor)
class(models) <- "caretList"
mylist<-list()
cnt<-0
for(i in 1:length(models)){
  probs <- predict(models[[i]], newdata=test, type='prob')
  probs<-data.frame(cbind(probs,winner = test$Y))
  probs$winner_num<-ifelse(probs$winner=='c0',1,0)
  pred<-ROCR::prediction(probs$c0,probs$winner_num)
  perf<-ROCR::performance(pred,"tpr", "fpr")
  mylist[[i]] <- data.frame(fpr=unlist(perf@x.values),tpr=unlist(perf@y.values),model=models[[i]]$method) 
}
allROCS <-data.frame(do.call("rbind",mylist))


#stampiamo le curve ROC
library(ggplot2)
library(ggthemes)
ggplot(allROCS, aes(x=fpr, ymin=0, ymax=tpr)) + 
  geom_line(aes(y=tpr,color=model),linewidth=1.5) +
  labs(title = "ROC curves on test set",
       x = "False Positive rate",
       y = "True Positive Rate")+
  theme_fivethirtyeight() + scale_color_brewer(palette='Paired') + 
  geom_segment(aes(x=0, y=0, xend=1, yend=1), colour = 'black',lty=2)

#valuto AUC per best model (Treebag)
posterior = predict(tree_cart, newdata = test, type="prob")
posterior=data.frame(posterior)
pred_prob1=posterior[,1]
pred_probrO=predict(tree_cart,newdata=test,type=c("prob"))[,1]
library(pROC)
roc(Y ~ pred_probrO, levels=c("c1", "c0"), data = test)


####STEP 3: scelta soglia####
predVal <- predict(tree_cart, test,type = "prob")
df=data.frame(cbind(test$Y , predVal))
colnames(df)=c("Y","Probc0","Probc1")
df=df[,1:2]

library(dplyr)
thresholds <- seq(from = 0, to = 1, by = 0.01)
prop_table <- data.frame(threshold = thresholds, Sens = NA,  Spec = NA, true_c0 = NA,  true_c1 = NA ,fn_c0=NA)

for (threshold in thresholds) {
  pred <- ifelse(df$Probc0 > threshold, "c0", "c1")
  pred_t <- ifelse(pred == df$Y, TRUE, FALSE)
  group <- data.frame(df, "pred" = pred_t) %>%
    group_by(Y, pred) %>%
    dplyr::summarise(n = n())
  group_c0 <- filter(group, Y == "c0")
  true_c0=sum(filter(group_c0, pred == TRUE)$n)
  prop_c0 <- sum(filter(group_c0, pred == TRUE)$n) / sum(group_c0$n)
  prop_table[prop_table$threshold == threshold, "Sens"] <- prop_c0
  prop_table[prop_table$threshold == threshold, "true_c0"] <- true_c0
  fn_c0=sum(filter(group_c0, pred == FALSE)$n)
  
  prop_table[prop_table$threshold == threshold, "fn_c0"] <- fn_c0
  group_c1 <- filter(group, Y == "c1")
  true_c1=sum(filter(group_c1, pred == TRUE)$n)
  prop_c1 <- sum(filter(group_c1, pred == TRUE)$n) / sum(group_c1$n)
  prop_table[prop_table$threshold == threshold, "Spec"] <- prop_c1
  prop_table[prop_table$threshold == threshold, "true_c1"] <- true_c1
}

# false positive
prop_table$fp_c0=nrow(test)-prop_table$true_c1-prop_table$true_c0-prop_table$fn_c0
# find accuracy
prop_table$acc=(prop_table$true_c1+prop_table$true_c0)/nrow(test)
# find precision
prop_table$Prec=prop_table$true_c0/(prop_table$true_c0+prop_table$fp_c0)
# find F1 =2*(prec*sens)/(prec+sens)
# prop_true_c0 = sensitivity
prop_table$F1=2*(prop_table$Sens*prop_table$Prec)/(prop_table$Sens+prop_table$Prec)

#nel caso ci siano valori mancanti li sostituiamo con degli 0
library(Hmisc)
prop_table$Prec=impute(prop_table$Prec, 1)
prop_table$F1=impute(prop_table$F1, 0)

#teniamo solo le colonne con le metriche
colnames(prop_table)
prop_table2 = prop_table[,-c(4:7)] #eliminiamo quindi le colonne dei TP TN FP FN

#costruiamo il plot con le thresholds
library(dplyr)
library(tidyr)
gathered=prop_table2 %>%
  gather(x, y, Sens:F1)
# plot measures 
library(ggplot2)
gathered %>%
  ggplot(aes(x = threshold, y = y, color = x)) +
  geom_point() +
  geom_line() +
  scale_color_brewer(palette = "Set1") +
  labs(y = "measures",
       color = "c0: event\nc1: non event")
# possiamo fare uno zoom sulla parte centrale del grafico
gathered %>%
  ggplot(aes(x = threshold, y = y, color = x)) +
  geom_point() +
  geom_line() +
  scale_color_brewer(palette = "Set1") +
  labs(y = "measures",
       color = "c0: event\n c1: nonevent") +
  coord_cartesian(xlim = c(0.01, 0.5))

#costruiamo la matrice di confusione con la soglia scelta
df$decision=ifelse(df$Probc0>0.23,"c0","c1")
table(df$Y,df$decision)
confusionMatrix(as.factor(df$decision),df$Y, positive = "c0") #abbiamo una sens=96.1%

####STEP 4: scoring####
pred_score = predict(tree_cart, score, type="prob")
df = data.frame(cbind(score$Y,pred_score))
colnames(df) = c("Y","Probc0","Probc1")
df = df[,1:2]
df$decision_score=ifelse(df$Probc0>0.23,"c0","c1")
confusionMatrix(as.factor(df$decision_score),df$Y, positive = "c0") #sens=95.4%
