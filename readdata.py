# staffinfo
# skill
# deptcore
# T
# alpha beta gamma
# configvar
import os
from datetime import datetime
import config

# 辞書の値からキーを抽出
def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

def read_staff_info():
    d = []
    staff = {}
    # Windowsはstr型（UTF-8）をbyte型（cp932）に勝手に変換してしまうが変換できないためエラーが出る
    # エンコーディング方式を指定する
    path = os.path.join(config.DATA_DIR ,'data','staffinfo.dat')
    with open(path, encoding="utf-8_sig") as f:
    # with open('C:\\Users\\honda\\PyProjects\\scheduling\\data\\StaffInfo.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))
  
        # 0:uid, 1:id, 2:staffname
        for arr in d:
            id = int(arr[0])
            staff[id] = {'uid':id, 'id':arr[1], 'name':arr[2]}        
    return staff

def read_Nr_Gm_Core(Ndum):
    d = []
    Nr = []
    G = []; G1 = []; G2 = []; G3 = []; G4 = []; G5 = []; G6 = []; G7 = []; G8 = []; G9 = []; G10 = []
    Core = []; C1 = []; C2 = []; C3 = []; C4 = []; C5 = []; C6 = []; C7 = []; C8 = []; C9 = []
    # NrDeptCore -> 0:uid, 1:dept, 2:rt, 3:mr, 4:tv, 5:ks, 6:nm, 7:xp, 8:ct, 9:xo, 10:ag, 11:mg, 12:mt
    path = os.path.join(config.DATA_DIR ,'data','Nrdeptcore.dat')
    with open(path, encoding="utf-8_sig") as f:
    # with open('C:\\Users\\honda\\PyProjects\\scheduling\\data\\NrDeptCore.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))

        for arr in d:
            uid = int(arr[0])
            dept = arr[1].upper()
            if dept != 'AS' and arr[3] != 'ET':
                Nr.append(uid)

            if dept == 'MR':
                G1.append(uid)
                if arr[3] == '6':
                    C1.append(uid)      
            if dept == 'TV':
                G2.append(uid)
                if arr[4] == '6':
                    C2.append(uid)      
            if dept == 'KS':
                G3.append(uid)   
                if arr[5] == '6':
                    C3.append(uid)   
            if dept == 'NM':
                G4.append(uid)      
                if arr[6] == '6':
                    C4.append(uid)
            if dept == 'AG':
                G5.append(uid)    
                if arr[10] == '6':
                    C5.append(uid)  
            if dept == 'RT':
                G6.append(uid) 
                if arr[2] == '6':
                    C6.append(uid)
            if dept == 'XP':
                G7.append(uid)
                if arr[7] == '6':
                    C7.append(uid)                
            if dept == 'CT':
                G8.append(uid) 
                if arr[8] == '6':
                    C8.append(uid)
            if dept == 'XO':
                G9.append(uid)
                if arr[9] == '6':
                    C9.append(uid)
            if dept == 'FR' or dept == 'NF' or dept == 'MG' or dept == 'MT':
                G10.append(uid) 
    for n in Ndum:
        G1.append(n);G2.append(n);G3.append(n);G4.append(n);G5.append(n);G6.append(n);G7.append(n);G8.append(n);G9.append(n);G10.append(n)
        C1.append(n);C2.append(n);C3.append(n);C4.append(n);C5.append(n);C6.append(n);C7.append(n);C8.append(n);C9.append(n)

    G.append(G1); G.append(G2); G.append(G3); G.append(G4); G.append(G5); G.append(G6); G.append(G7); G.append(G8); G.append(G9); G.append(G10)
    Core.append(C1); Core.append(C2); Core.append(C3); Core.append(C4); Core.append(C5); Core.append(C6); Core.append(C7); Core.append(C8); Core.append(C9)

    return sorted(Nr), [sorted(m) for m in G], [sorted(m) for m in Core]

def read_skill(Ndum):
    d = []
    Nnight = []
    Ndaily = []
    Ns = []; N1 = []; N2 = []; N3 = []; N4 = []; N5 = []; N6 = []; N7 = []
    # Skill -> 0:uid, 1:nXA, 2:nMR, 3:nCT, 4:Fr, 5:夜勤, 6:休日勤
    path = os.path.join(config.DATA_DIR ,'data','skill.dat')
    with open(path, encoding="utf-8_sig") as f:
    # with open(settings.BASE_DIR + '\\data\\Skill.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))

        for arr in d:
            uid = int(arr[0])
            if arr[5] == '2':
                Nnight.append(uid)
            if arr[6] == '2':
                Ndaily.append(uid)
            if arr[1] == '2' and arr[6] == '2':
                N1.append(uid)
            if arr[2] == '2' and arr[6] == '2':
                N2.append(uid)
            if arr[3] == '2' and arr[6] == '2':
                N3.append(uid)
            if arr[4] == '2' and arr[6] == '2':
                N4.append(uid)
            if arr[1] == '2' and arr[5] == '2':
                N5.append(uid)
            if arr[2] == '2' and arr[5] == '2':
                N6.append(uid)
            if arr[3] == '2' and arr[5] == '2':
                N7.append(uid)

    for n in Ndum:
        N1.append(n); N2.append(n); N3.append(n); N4.append(n); N5.append(n); N6.append(n); N7.append(n)       
    Ns.append(N1); Ns.append(N2); Ns.append(N3); Ns.append(N4); Ns.append(N5); Ns.append(N6); Ns.append(N7)

    return sorted(Nnight), sorted(Ndaily), [sorted(l) for l in Ns]


def read_T():
    d = []
    Tdict = {}
    T = []; Tr = []; Tc = []
    path = os.path.join(config.DATA_DIR ,'data','T.dat')
    with open(path, encoding="utf-8_sig") as f:
    # with open(settings.BASE_DIR + '\\data\\T.dat', encoding="utf-8_sig") as f:
        d = f.readline()
        d = d.strip()
        d = d.split(',')
        d = sorted(d)

        i = 0
        for t in d:
            Tdict[i] = t
            T.append(i)
            i += 1
                  
        d = f.readline()
        d = d.strip()
        d = d.split(',')
        d = sorted(d)

        for t in d:
            Tr.append(get_key_from_value(Tdict, t))

        d = f.readline()
        d = d.strip()
        d = d.split(',')
        d = sorted(d)
        for t in d:
            Tc.append(get_key_from_value(Tdict, t))

    return Tdict, T, Tr, Tc


def read_alpha():
    d = []
    alpha = []
    dict = { 'da':0, 'dm':1, 'dc':2, 'df':3, 'na':4, 'nm':5, 'nc':6, 'nn':7, 'dw':8, 'ew':9, 'do':10, 'ho':11}
    path = os.path.join(config.DATA_DIR ,'data','alpha.dat')
    
    with open(path, encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))
    
    for arr in d:
        modality = []
        for i in arr[1:]:
            modality.append(int(i))
        alpha.insert(int(dict[arr[0].lower()]), modality)
    
    return alpha

# beta 0:MR, 1:TV, 2:HT, 3:MN, 4:XA, 5:RT, 6:XP, 7:CT, 8:XO, 9:MG, 10:MT, 11:FR/NF
def read_beta():
    d = []    
    beta = []
    dict = {'mr':0, 'tv':1, 'ks':2, 'nm':3, 'ag':4, 'rt':5, 'xp':6, 'ct':7, 'xo':8, 'mg':9, 'mt':10, 'fr':11}
    path = os.path.join(config.DATA_DIR ,'data','beta.dat')
    with open(path, encoding="utf-8_sig") as f:    
    # with open(settings.BASE_DIR + '\\data\\beta.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))
        
    for arr in d:
        lowLimit = []
        for i in arr[1:]:
            lowLimit.append(int(i))
        beta.insert(dict[arr[0].lower()], lowLimit)

    return beta

def read_gamma():
    d = []
    gamma = []
    dict = {'mr':0, 'tv':1, 'ks':2, 'nm':3, 'ag':4, 'rt':5, 'xp':6, 'ct':7, 'xo':8, 'mg':9, 'mt':10, 'fr':11}
    path = os.path.join(config.DATA_DIR ,'data','gamma.dat')
    with open(path, encoding="utf-8_sig") as f:    
    # with open(settings.BASE_DIR + '\\data\\gamma.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))
            
    for arr in d:
        core = []
        for i in arr[1:]:
            core.append(int(i))
        gamma.insert(dict[arr[0].lower()], core)    

    return gamma

def read_config_var():
    d = []
    path = os.path.join(config.DATA_DIR ,'data','configvar.dat')
    with open(path, encoding="utf-8_sig") as f:    
    # with open(settings.BASE_DIR + '\\data\\ConfigVar.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))

        for arr in d:
            if arr[0] == 'date':
                createDate = datetime.strptime(arr[1], '%Y/%m/%d')
            elif arr[0] == 'epsilon':
                epsilon = int(arr[1])
            elif arr[0] == 'iota':
                iota = int(arr[1])    
            elif arr[0] == 'kappa':
                kappa = int(arr[1])
            elif arr[0] == 'myu':
                myu = int(arr[1])
            elif arr[0] == 'nyu':
                nyu = []
                nyu.append(int(arr[1]) if arr[1] else 0)
                nyu.append(int(arr[2]) if arr[2] else 0)
                nyu.append(int(arr[3]) if arr[3] else 0)
            elif arr[0] == 'rho':
                rho = (int(arr[1]) if arr[1] else 0)
            elif arr[0] == 'lambda':
                lam = []
                lam.append(float(arr[1] if arr[1] else 0))
                lam.append(float(arr[2] if arr[2] else 0))
                lam.append(float(arr[3] if arr[3] else 0))
                lam.append(float(arr[4] if arr[4] else 0))
                lam.append(float(arr[5] if arr[5] else 0))

    return createDate, epsilon, iota, kappa, myu, nyu, rho, lam

def read_previous():
    d = []
    Fprev = []
    path = os.path.join(config.DATA_DIR ,'data','previous.dat')
    with open(path, encoding="utf-8_sig") as f:    
    # with open(settings.BASE_DIR + '\\data\\Previous.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))

        for arr in d:
            prev = []
            prev.append(int(arr[0]))
            prev.append(arr[1])
            prev.append(arr[2])
            Fprev.append(prev)

    return Fprev

def read_request():
    d = []
    Frequ = []
    path = os.path.join(config.DATA_DIR ,'data','request.dat')
    with open(path, encoding="utf-8_sig") as f:    
    # with open(settings.BASE_DIR + '\\data\\Request.dat', encoding="utf-8_sig") as f:
        for line in f:
            line = line.strip()
            d.append(list(line.split(',')))

        for arr in d:
            requ = []
            requ.append(int(arr[0]))
            requ.append(arr[1])
            requ.append(arr[2])
            Frequ.append(requ)

    return Frequ


