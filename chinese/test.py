from svmutil import *

y, x = svm_read_problem('question_chinese')
m = svm_train(y[:], x[:], '-c 512.0 -g 0.0078125')
p_label, p_acc, p_val = svm_predict(y[:], x[:], m)


# Other utility functions
svm_save_model('question_chinese.model', m)
m = svm_load_model('question_chinese.model')
p_label, p_acc, p_val = svm_predict(y[:], x[:], m)
#print p_label,p_acc,p_val
