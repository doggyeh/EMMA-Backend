from svmutil import *

y, x = svm_read_problem('heart_scale')
m = svm_train(y[:200], x[:200], '-c 4')
p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)


# Other utility functions
svm_save_model('heart_scale.model', m)
m = svm_load_model('heart_scale.model')
p_label, p_acc, p_val = svm_predict(y[:200], x[:200], m)
#print p_label,p_acc,p_val
