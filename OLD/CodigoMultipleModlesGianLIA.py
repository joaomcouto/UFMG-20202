from threading import Thread
from queue import Queue
import sys
import os
import pandas as pd
import numpy as np
from multiprocessing import Pool
import pickle
from sklearn.metrics import f1_score

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import random
import time

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve, roc_auc_score, auc, confusion_matrix, accuracy_score

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn import tree

HOME_PATH = '/homeLocal/gzuin/'
MODELS_PATH = HOME_PATH + 'RootCauses-Behaviour/Models/'
TABLES_PATH = HOME_PATH
GRAPHS_PATH = HOME_PATH + 'RootCauses-Behaviour/Graphs/'
IMAGES_PATH = HOME_PATH + 'RootCauses-Behaviour/Clusters/'

N_FOLDS = 5
RANDOM_STATE = 1


def random_combinations(iterable, r, x, seed=10):
    pool = tuple(iterable)
    n = len(pool)
    a = []
    random.seed(seed)
    for i in range(x):
        indices = sorted(random.sample(range(n), r))
        a.insert(len(a), tuple(pool[i] for i in indices))
    return list(set(a))


def gridSearch(df, comb, c):
    bestParams = {'random_state': 20200225, 'criterion': 'gini', 'max_depth': None,
                  'min_samples_split': 71, 'min_samples_leaf': 29, 'min_impurity_decrease': 0.0}
    bestAUC = -1

    mdrange = [None, 3, 5, 10]
    criterions = ['gini', 'entropy']
    mssrange = list(range(5, 101, 5))
    mslrange = list(range(5, 51, 5))
    midrange = [0.0, 0.01, 0.1]

    combinations = len(mdrange)*len(mssrange)*len(mslrange)*len(midrange)

    if os.path.isfile(MODELS_PATH + 'MultipleModels_DecisionTrees/' + 'suicidio-size%d-gridsearch.pkl' % c):
        with open(MODELS_PATH + 'MultipleModels_DecisionTrees/' + 'suicidio-size%d-gridsearch.pkl' % c, 'rb') as pkldic:
            bestParams = pickle.load(pkldic)
            griddone[c] = combinations
        return bestParams

    tdone = 0.0
    begin = time.time()
    z = 0
    for crit in criterions:
        for md in mdrange:
            for mss in mssrange:
                for msl in mslrange:
                    for mid in midrange:
                        tdone += 1
                        aucs = []
                        # ff eh um modelo, comb eh uma lista de tuplas onde cada tupla é um modelo(conjunto de features) de mesmo tamanho
                        for ff in comb:
                            f = []
                            for x in ff:  # transforma a tupla com o modelo em uma lista
                                f.insert(len(f), x)
                            auc, accmedia, preds, probs,f1,_ = select_features_platelabel(df, f,{'random_state': 1, 'max_depth': md, 'min_samples_split': mss, 'min_samples_leaf': msl, 'min_impurity_decrease': mid, 'criterion': crit}, nfolds=4,f1i=True)
                            aucs.extend(auc)
                            z += 1
                            # print(z,len(comb))

                        if np.mean(f1) > bestAUC:
                            bestParams['max_depth'] = md
                            bestParams['min_samples_split'] = mss
                            bestParams['min_samples_leaf'] = msl
                            bestParams['min_impurity_decrease'] = mid
                            bestParams['criterion'] = crit
                            bestAUC = np.mean(f1)

                        if c != 0:
                            now = time.time()
                            elapsed = now-begin
                            perinstance = float(elapsed)/float(tdone)
                            predicted = perinstance * combinations
                            griddone[c] += 1
                            sys.stdout.write('GridSearch (size %02d) Progress: %.3f%% (%d/%d) [Elapsed: %ds | Predicted %ds | Avg: %ds]\r' % (
                                c, 100.0*tdone/combinations, tdone, combinations, elapsed, predicted, perinstance))
                            sys.stdout.flush()

    with open(MODELS_PATH + 'MultipleModels_DecisionTrees/' + 'suicidio-size%d-gridsearch.pkl' % c, 'wb') as pkldic:
        pickle.dump(bestParams, pkldic)
    return(bestParams)


# Recebe varios modelos DE MESMO TAMANHO, cada uma é uma tupla em comb
def eval_panel_platelabel(df, comb, c, exit_stat, exit_outp):

    fpath = MODELS_PATH + 'MultipleModels_DecisionTrees/' + \
        'suicidio-size%d-preds.csv' % c

    performed = []
    if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
        performed = list(pd.read_csv(
            fpath, delimiter=';', header=0)['features'])
        done[c] += len(performed)
        global predone
        predone += len(performed)

        exit_outp.write('\n')
        exit_stat.write('\n')
    else:
        exit_outp.write('features')
        for i in range(len(df)):
            exit_outp.write(';pred%d' % (i+1))
        for i in range(len(df)):
            exit_outp.write(';prob%d' % (i+1))
        exit_outp.write('\n')

    params = gridSearch(df, comb[:max(50, int(0.001*float(len(comb))))], c)

    ncomb = []
    begin = time.time()
    tdone = 0.0

    for ff in comb:
        f = []
        for x in ff:  # transforma a tupla com o modelo em uma lista
            f.insert(len(f), x)

        if str(f) not in performed:
            ncomb.append(ff)
    comb = ncomb
    res = []
    # ff eh um modelo, comb eh uma lista de tuplas onde cada tupla é um modelo(conjunto de features) de mesmo tamanho
    for ff in comb:
        tdone += 1
        now = time.time()
        elapsed = now-begin
        perinstance = float(elapsed)/float(tdone)
        predicted = perinstance * len(comb)
        sys.stdout.write('MM (size %02d) Progress: %.3f%% (%d/%d) [Elapsed: %ds | Predicted %ds | Avg: %ds]\r' % (
            c, 100.0*tdone/len(comb), tdone, len(comb), elapsed, predicted, perinstance))
        sys.stdout.flush()

        global s
        if done[c] > s:
            break

        f = []
        for x in ff:  # transforma a tupla com o modelo em uma lista
            f.insert(len(f), x)
        auc, accmedia, preds, probs, f1, f1w = select_features_platelabel(
            df, f, params, nfolds=N_FOLDS, f1i=True)  # Chama a funcao central com apenas um modelo f
        done[c] += 1
        res.append(np.mean(auc))
        exit_stat.write("%s;%f;%f;%f;%s;%s;%s;%s\n" %
                        (str(f), np.mean(auc),np.mean(f1),np.mean(f1w),auc,f1,f1w,accmedia))

        exit_outp.write("%s" % str(f))
        for p in preds:
            exit_outp.write(';%d' % p)
        for p in probs:
            exit_outp.write(';%f' % p)
        exit_outp.write('\n')
    return(res)


def delete_last_lines(ifile):
    with open(ifile, "r+", encoding="utf-8") as file:

        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()


def select_features_platelabel(df, features, params, nfolds, f1i=False):  # Recebe UM modelo

    X = df[features].values
    y = df[label_column_name].values
    predList = np.zeros(len(df))
    probList = np.zeros(len(df))

    cv = StratifiedKFold(n_splits=nfolds, shuffle=True, random_state=1)
    foldNum = 0
    a = []
    b = []
    c = []
    d = []
    for (train, val) in cv.split(X, y):
        #print(np.sum(y[train]),np.sum(y[val],len(y))
        foldNum = foldNum + 1

        # Modelo arvore
        classifier = DecisionTreeClassifier(class_weight='balanced', max_depth=params['max_depth'], min_samples_leaf=params['min_samples_leaf'],min_samples_split=params['min_samples_split'], min_impurity_decrease=params['min_impurity_decrease'], criterion=params['criterion'])
        classifier = classifier.fit(X[train], y[train])
        probas_ = classifier.predict_proba(X[val])
        probas = [probas_[x][0] for x in range(len(probas_))]

        pred = classifier.predict(X[val])
        area1 = roc_auc_score(y[val], probas_[:, 1])
        area2 = accuracy_score(y[val], pred)  # guarda acuracia

        #print('b',np.sum(y[val]),np.sum(pred),len(y[val]))
        f1 = f1_score(y[val],pred, average='binary')
        #print('w',np.sum(y[val]),np.sum(pred),len(y[val]))
        f1w = f1_score(y[val],pred, average='weighted')

        a.insert(len(a), area1)
        b.insert(len(b), area2)
        c.insert(len(c),f1)
        d.insert(len(d),f1w)

        for j in range(len(val)):
            predList[val[j]] = pred[j]
            probList[val[j]] = probas[j]

    if f1i:
        return a, np.mean(b), predList, probList,c,d
    return a, np.mean(b), predList, probList


df = pd.read_csv(TABLES_PATH + 'totalcx7.csv')
df = df.dropna(axis=0)
columns = list(df.columns)

label_column_name = 'suicidio'
unwanted_columns = [] + [label_column_name]
features_columns = [
    item for item in columns if item not in unwanted_columns]
print(len(df), np.sum(df[label_column_name]))
print(len(features_columns))


print(np.sum(df['suicidio']),len(df))

global done
global griddone
global predone
global queue_finished
queue_finished = 0
predone = 0
global s
s = 10000
totalmodels = 0
combs = []
done = []
griddone = []

print('Creating Feature Combinations')
for c in range(0, 21):
    # print('\t Size:%d'%c)
    if c == 0:
        combs.append([])
    else:
        combs.append(list(set(random_combinations(features_columns, c, s))))
    done.append(0)
    griddone.append(0)
    totalmodels += len(combs[-1])


def run_mmpool(c):
    sys.stdout.write("Starting MM size %d\n" % c)
    sys.stdout.flush()

    comb = combs[c]
    exit1 = open(MODELS_PATH + 'MultipleModels_DecisionTrees/' +
                 'suicidio-size%d-result.csv' % c, 'a+')
    exit2 = open(MODELS_PATH + 'MultipleModels_DecisionTrees/' +
                 'suicidio-size%d-preds.csv' % c, 'a+')

    a = eval_panel_platelabel(df, comb, c, exit1, exit2)
    global queue_finished
    queue_finished += 1
    exit1.close()
    exit2.close()
    return(a)


if 1==1:
    print('Creating Directories')
    if (not os.path.isdir(MODELS_PATH + 'MultipleModels_DecisionTrees')):
        os.mkdir(MODELS_PATH + 'MultipleModels_DecisionTrees')

    for c in range(1, 21):
        if os.path.isfile('MultipleModels_DecisionTrees/' + 'suicidio-size%d-result.csv' % c):
            delete_last_lines('MultipleModels_DecisionTrees/' +
                              'suicidio-size%d-result.csv' % c)
            delete_last_lines('MultipleModels_DecisionTrees/' +
                              'suicidio-size%d-preds.csv' % c)

    pool = Pool(processes=10)
    results = pool.map(run_mmpool, list(range(1, 21)))
    pool.join()

    for i in range(0, len(results)):
        print(np.max(results[i]))