import copy
def global_align(x, y, s_match, s_mismatch, s_gap):
    A = []
    for i in range(len(y) + 1):
        A.append([0] * (len(x) +1))
    for i in range(len(y)+1):
        A[i][0] = s_gap * i
    for i in range(len(x)+1):
        A[0][i] = s_gap * i
    for i in range(1, len(y) + 1):
        for j in range(1, len(x) + 1):

            A[i][j] = max(
            A[i][j-1] + s_gap,
            A[i-1][j] + s_gap,
            A[i-1][j-1] + (s_match if (y[i-1] == x[j-1] and y[i-1] != '-') else 0) +(s_mismatch if (y[i-1] != x[j-1] and y[i-1] != '-' and x[j - 1] != '-') else 0) +(s_gap if (y[i-1] == '-' or x[j - 1] == '-') else 0)
              )

    align_X = ""
    align_Y = ""
    i = len(x)
    j = len(y)

    while i > 0 or j > 0:

        current_score = A[j][i]

        if i > 0 and j > 0 and (
            ((x[i - 1] == y[j - 1] and y[j-1] != '-') and current_score == A[j - 1][i - 1] + s_match)  or
            ((y[j-1] != x[i-1] and y[j-1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][i - 1] +s_mismatch) or
            ((y[j-1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + s_gap)
            ):
            align_X = x[i - 1] + align_X
            align_Y = y[j - 1] + align_Y
            i = i - 1
            j = j - 1
        elif i > 0 and (current_score == A[j][i - 1] + s_gap):
            align_X = x[i - 1] + align_X
            align_Y = "-" + align_Y
            i = i - 1
        else:
            align_X = "-" + align_X
            align_Y = y[j - 1] + align_Y
            j = j - 1
    return (align_X, align_Y,A[len(y)][len(x)])
#-------------------------
def Distance(x, y):
    match = 0
    mismatch = 0
    for k in range(len(x)):
        if x[k]!= '-' and y[k]!='-':
            if x[k]==y[k]:
                match = match + 1
            else:
                mismatch = mismatch + 1
    return mismatch/(match+mismatch)
#---------------------------------------
def DistanceMat(sequence):
    N = len(sequence)
    distance = [['-' for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            xa , ya , p = global_align(sequence[j].value,sequence[i].value,1,-1,-2)
            distance[i][j] = p
    return distance
#--------------

def UpdateMat(mat):
    N = len(mat)
    #print(N)
    M = copy.deepcopy(mat)
    r = R(mat)
    for i in range(N):
        for j in range(N):
            M[i][j] = mat[i][j]-((r[i]+r[j])/(N-2))
    return M
#----------------------
def R(mat):
    N = len(mat)
    r = []
    for i in range(N):
        r.append(sum(mat[i]))
    return r
#---------------------

def FullGap(cl):
    counter = 0
    for item in cl:
        if item == '-':
            counter = counter + 1
    if counter == len(cl):
        return True
    else:
        return False
#---------------------
def MostRepeated(pose):
    poses = copy.deepcopy(pose)
    if FullGap(poses):
        return '-'
    else:
        while '-' in poses:
            poses.remove('-')
        dictp = {}
        poses.sort()
        count, itm = 0, ''
        for item in reversed(poses):
            dictp[item] = dictp.get(item, 0) + 1
            if dictp[item] >= count :
                count, itm = dictp[item], item
        return(itm)
#----------------------
def Consensus(seqi):
    seqx = copy.deepcopy(seqi)
    nseq = len(seqx)
    leng = max(len(j.value) for j in seqx)
    for k in range(nseq):
        seqx[k].value = seqx[k].value + (leng- len(seqx[k].value))*'-'
    gseq = ''
    for i in range(leng):
        gseq = gseq + MostRepeated([s.value[i] for s in seqx])
    return gseq
#----------------------
def MinInMat(mat):
    N = len(mat)
    m = mat[0][1]
    posm = 0 , 1
    for i in range(N):
        for j in range(N):
            if mat[i][j] < m:
                if i != j:
                    m = mat[i][j]
                    posm = i , j
    return posm
#----------------------
def GetSequences(N):
    sequence = []
    for i in range(N):
        seq = input()
        sequence.append(seq)
    return sequence
#---------------------
def UpdateChild(n):
    if n.leaves:
        state = True
        bchild = n.leaves
    else:
        state = False
        bchild = n.SubLeaves()
    if n.leaves:
        state = True
    bx = n.value
#    print(f'Updating child for {bx}')
    for child in bchild:
        x, y , p =global_align(child.value,bx,1 , -1 , -2)
#        print(child.value , bx , x , y)
        #child.value = x
        for k in range(len(n.value)):
            if bx[k] == '-':
                x = x[:k] + '-' + x[k+1:]
        child.value = x
        if not state:
            n.leaves.append(child)
    return n


def NewNeighbor(mat, sequence, mains):
    p = 0
    N = len(mat)
    i , j = MinInMat(mat)
    a = sequence[i]
    b = sequence[j]

    sequence.remove(a)
    sequence.remove(b)



    ax , bx , p = global_align(a.value,b.value,1,-1,-2)
    a.value = ax
    b.value = bx
    if not b.isleaf:
        b = UpdateChild(b)
    if not a.isleaf:
        a = UpdateChild(a)
    newN = Node(Consensus(a.SubLeaves() + b.SubLeaves()))
    newN.left = a
    newN.right = b
    a.parent = newN
    b.parent = newN
    sequence.insert(min([i , j]), newN)
    node = newN

    NewMat= [[0 for i1 in range(N-1)] for i2 in range(N-1)]
    #S(AU) =d(AB) / 2 + [r(A)-r(B)] / 2(N-2) = 1
    #S(BU) =d(AB) -S(AU) = 4
    for k in range(N-1):
        for t in range(N-1):
            NewMat[k][t] = mat[i][k] + mat[j][t] - mat[i][j]/2
    return NewMat, node , p
#----------------
class Node:
    def __init__(self , value ,order = 100000 , isleaf = False):
        self.value  = value
        self.parent = None
        self.right  = None
        self.left   = None
        self.order = order
        self.isleaf = isleaf
        if self.isleaf:
            self.leaves = [self]
        else:
            self.leaves = []
    def IsLeaf(self):
        return self.right == None and self.left == None
    def SubLeaves(self):
        if self.isleaf:
            return [copy.deepcopy(self)]
        if self.leaves:
            return copy.deepcopy(self.leaves)
        check = []
        c = copy.deepcopy(self)
        current = [c]
        while len(current)!=0:
            c = current.pop(0)
            #print('in loop   ',c.value , c.isleaf , depth(c) , c.order)
            check.append(c)
            if c.right:
               # if not (c.right in check):
                current.append(c.right)
            if c.left:
            #    if not(c.left in check):
                current.append(c.left)
        for item in check:
            #print(item.value , depth(item) , item.isleaf)
            if not item.isleaf:
            #    print('will remove',item.value , depth(item) ,item.order, item.isleaf )
                check.remove(item)
        self.leaves = check
        return copy.deepcopy(check)
###-----------------------------
def Finishing(sequence):
    #print('Finishing')
    a = sequence.pop(0)
    b = sequence.pop(0)
    newN = Node(Consensus(a.SubLeaves() + b.SubLeaves()))

   # print(a.value , b.value)
    ax , bx , p = global_align(a.value,b.value,1,-1,-2)
    a.value = ax
    b.value = bx
    if not b.isleaf:
        #print('B')
        b =UpdateChild(b)
    if not a.isleaf:
        #print('A')
        a = UpdateChild(a)

    #for ck in a.SubLeaves():
    #    print(f"{ck.value} at the end")
    a.parent = newN
    b.parent = newN
    newN.left = a
    newN.right = b

    #print(newN.value)
    sequence.append(newN)
    node = newN
    node.leaves= list(set(a.leaves + b.leaves))
    #UpdateChild(node)


  #  print(node.value , a.value , a.isleaf, a.order, b.value , b.isleaf , b.order)
    return newN , p
#------------------------
def TotalPoint(seq):
    colnum = len(seq[0].value)
    point = 0
    for i in range(colnum):
        s = ''
        for item in seq:
            s = s + item.value[i]
        point = point + ColPoint(s , 1 , -1 , -2)
    return point

#-----------------------
def ColPoint(col , match , mismatch , gap):
    p = 0
    for i in range(len(col)):
        for j in range(i+1 , len(col)):
            if col[i] == '-':
                if col[j] != '-':
                    p = p + gap
            if col[j] == '-':
                if col[i] != '-':
                    p = p + gap
            if col[i] != '-' and col[j] != '-':
                if col[i] == col[j]:
                    p = p  + match
                if col[i] != col[j]:
                    p = p + mismatch
    return p

#----------------------
def Score(seq,f):
    msa = f.value
    point = 0
    for s in seq:
        x, y , p =global_align(s.value,msa,1 , -1 , -2)
        point = point + p
    return point
def FinalScore(seq):
    point = 0
    for i in range(len(seq)):
        for j in range(i+1 , len(seq)):
            x, y , p =global_align(seq[i].value,seq[j].value,1 , -1 , -2)
            point = point + p
    return point
#----------------------
def Result(nf  ,mains):
    cy = nf.SubLeaves()


    cy = sorted(cy, key=lambda c: c.order)
    nottobe = []
    for item in cy:
        if not item.isleaf:
            nottobe.append(item)
    for i in range(len(nottobe)):
        cy.remove(nottobe[i])

    for i in range(len(cy)):
        print(cy[i].value)

    return cy
#---------------------------------




print('Please Enter the number of sequences')
N = int(input())
print('Please Enter the sequences')
seq5 = GetSequences(N)
s3main = copy.deepcopy(seq5)
seqin  = copy.deepcopy(seq5)
firsts = []
for i in range(len(seqin)):
    firsts.append(Node(seqin[i] , i , True))
mains =  copy.deepcopy(firsts)
initial = Node('Begin')
nloop = initial
point = 0
#print('-----------------------')
u = UpdateMat(DistanceMat(firsts))
while len(firsts)>3:
    m1 ,n1 , p = NewNeighbor(u , firsts , mains)
    u = UpdateMat(m1)
    nloop = n1

    point = point + p
m1 ,n1 , p = NewNeighbor(u , firsts , mains)
nfx  , p= Finishing(firsts)
point = point + p
print('--------Result--------')
f = Result(nfx , mains)
print(FinalScore(f))
