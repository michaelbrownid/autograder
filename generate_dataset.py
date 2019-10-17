#     plt.figure(figsize=(20,10))
#     cols = 5
#   for i in range(cols):
#         plt.subplot(5/cols+1,cols,i+1)
#         plt.imshow(X[i])
#         plt.title('Digit: '+str(y[i]),fontsize=20)

from keras.datasets import mnist
(X_tr,y_tr),(X_ts,y_ts) = mnist.load_data()

def grab_indices(indices,n,index_list):
    indices = list(np.arange(len(X_ts)))
    sel = np.random.choice(indices,4,replace=False)
    for ind in sel:
        del indices[ind]
    index_list.append(sel)
    del sel
    return indices,index_list

def make_stuff():
    index_list=[]
    indices = list(np.arange(len(X_ts)))
    for i in range(int(len(X_ts)/4)):
        indices,index_list = grab_indices(indices,4,index_list)