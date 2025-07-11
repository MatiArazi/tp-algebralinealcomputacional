# Matriz A de ejemplo
#A_ejemplo = np.array([
#    [0, 1, 1, 1, 0, 0, 0, 0],
#    [1, 0, 1, 1, 0, 0, 0, 0],
#    [1, 1, 0, 1, 0, 1, 0, 0],
#    [1, 1, 1, 0, 1, 0, 0, 0],
#    [0, 0, 0, 1, 0, 1, 1, 1],
#    [0, 0, 1, 0, 1, 0, 1, 1],
#    [0, 0, 0, 0, 1, 1, 0, 1],
#    [0, 0, 0, 0, 1, 1, 1, 0]
#])


import numpy as np

from template_funciones_1 import calculaLU


def calcula_L(A):
    grados = np.sum(A, axis=1)
    K = np.diag(grados)
    L = K - A
    return L

def calcula_R(A):
    
    k = A.sum(axis=1) # calculamos el grado de cada nodo: k[i] = suma de la fila i
    E2 = k.sum() # calculamos 2E = suma de todos los grados
    P = np.outer(k, k) / E2  # construimos P por producto externo y normalización
    R = A - P
    return R

def calcula_lambda(L,v):
    # Recibe L y v y retorna el corte asociado
    return  (1/4) * float(v.T @ L @ v)

def calcula_Q(R,v):
    return float(v.T @ R @ v)

def metpot1(A,tol=1e-8,maxrep=np.inf):
   # Recibe una matriz A y calcula su autovalor de mayor módulo, con un error relativo menor a tol y-o haciendo como mucho maxrep repeticiones
   N = A.shape[0]
   v =  np.random.uniform(-1.0, 1.0, size=N) # Generamos un vector de partida aleatorio, entre -1 y 1
   v /= np.linalg.norm(v) # Lo normalizamos 
   v1 = A @ v # Aplicamos la matriz una vez
   v1 /= np.linalg.norm(v1) # normalizamos
   l = float(v.T @ A @ v)# Calculamos el autovector estimado
   l1 = float(v1.T @ A @ v1) # Y el estimado en el siguiente paso
   nrep = 0 # Contador
   while np.abs(l1-l)/np.abs(l) > tol and nrep < maxrep: # Si estamos por debajo de la tolerancia buscada 
      v = v1 # actualizamos v y repetimos
      l = l1
      v1 = A @ v1 # Calculo nuevo v1
      v1 /= np.linalg.norm(v1) # Normalizo
      l1 = float(v1.T @ A @ v1) # Calculo autovector
      nrep += 1 # Un pasito mas
   if not nrep < maxrep:
      print('MaxRep alcanzado')
   if (np.all(v1 == 0)):
       l = 0
   else:
       l = (v1.T @ A @ v1) # Calculamos el autovalor
   return v1,l,nrep<maxrep

def deflaciona(A,tol=1e-8,maxrep=np.inf):
    # Recibe la matriz A, una tolerancia para el método de la potencia, y un número máximo de repeticiones
    v1,l1,_ = metpot1(A,tol,maxrep) # Buscamos primer autovector con método de la potencia
    deflA = A - l1 * np.outer(v1, v1) # Sugerencia, usar la funcion outer de numpy
    return deflA

def metpot2(A,v1,l1,tol=1e-8,maxrep=np.inf):
   # La funcion aplica el metodo de la potencia para buscar el segundo autovalor de A, suponiendo que sus autovectores son ortogonales
   # v1 y l1 son los primeors autovectores y autovalores de A}
   # Have fun!
   deflA = A - l1 * np.outer(v1, v1)
   return metpot1(deflA,tol,maxrep)


def calcula_B_inv(B):
    L, U = calculaLU(B)
    N = B.shape[0]
    B_inv = np.zeros((N, N))
    for i in range(N):
        # e_i
        e = np.zeros(N)
        e[i] = 1.0
        # L y = e
        y = np.zeros(N)
        for row in range(N):
            y[row] = e[row] - L[row, :row] @ y[:row]
        # U x = y
        x = np.zeros(N)
        for row in range(N-1, -1, -1):
            x[row] = (y[row] - U[row, row+1:] @ x[row+1:]) / U[row, row]
        B_inv[:, i] = x
    return B_inv

def metpotI(A,mu,tol=1e-8,maxrep=np.inf):
    # Retorna el primer autovalor de la inversa de A + mu * I, junto a su autovector y si el método convergió.
    N = A.shape[0]
    B = A + mu * np.eye(N)
    B_inv = calcula_B_inv(B)
    v1,l1,ok1 = metpot1(B_inv,tol=tol,maxrep=maxrep)
    l1 = 1/l1
    l1 -= mu
    return v1,l1,ok1

def metpotI2(A,mu,tol=1e-8,maxrep=np.inf):
   # Recibe la matriz A, y un valor mu y retorna el segundo autovalor y autovector de la matriz A, 
   # suponiendo que sus autovalores son positivos excepto por el menor que es igual a 0
   # Retorna el segundo autovector, su autovalor, y si el metodo llegó a converger.
   B = A + mu * np.eye( A.shape[0]) # Calculamos la matriz A shifteada en mu
   B_inv = calcula_B_inv(B)
   deflB = deflaciona(B_inv,tol,maxrep)
   v2, lam2, ok2 = metpot1(deflB, tol, maxrep)
   lam2 = 1/lam2
   lam2 -= mu
   return v2, lam2, ok2


def laplaciano_iterativo(A,niveles,nombres_s=None):
    # Recibe una matriz A, una cantidad de niveles sobre los que hacer cortes, y los nombres de los nodos
    # Retorna una lista con conjuntos de nodos representando las comunidades.
    # La función debe, recursivamente, ir realizando cortes y reduciendo en 1 el número de niveles hasta llegar a 0 y retornar.
    if nombres_s is None: # Si no se proveyeron nombres, los asignamos poniendo del 0 al N-1
        nombres_s = range(A.shape[0])
    if A.shape[0] == 1 or niveles == 0: # Si llegamos al último paso, retornamos los nombres en una lista
        return([nombres_s])
    else: # Sino:
        L = calcula_L(A) # Recalculamos el L
        v,l,_ = metpotI2(L,0.001) # Encontramos el segundo autovector de L
        # Recortamos A en dos partes, la que está asociada a el signo positivo de v y la que está asociada al negativo
        Ap = A[np.ix_(v > 0, v > 0)] # Asociado al signo positivo
        Am = A[np.ix_(v < 0, v < 0)] # Asociado al signo negativo
        
        return(
                laplaciano_iterativo(Ap,niveles-1,
                                     nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi>0]) +
                laplaciano_iterativo(Am,niveles-1,
                                     nombres_s=[ni for ni,vi in zip(nombres_s,v) if vi<0])
                )        


def modularidad_iterativo(A=None,R=None,nombres_s=None):
    # Recibe una matriz A, una matriz R de modularidad, y los nombres de los nodos
    # Retorna una lista con conjuntos de nodos representando las comunidades.

    if A is None and R is None:
        print('Dame una matriz')
        return(np.nan)
    if R is None:
        R = calcula_R(A)
    if nombres_s is None:
        nombres_s = range(R.shape[0])
    # Acá empieza lo bueno
    if R.shape[0] == 1: # Si llegamos al último nivel
        return [nombres_s]
    else:
        v,l,_ = metpot1(R) # Primer autovector y autovalor de R
        # Modularidad Actual:
        Q0 = np.sum(R[v>0,:][:,v>0]) + np.sum(R[v<0,:][:,v<0])
        if Q0<=0 or all(v>0) or all(v<0): # Si la modularidad actual es menor a cero, o no se propone una partición, terminamos
            return [nombres_s]
        else:
            ## Hacemos como con L, pero usando directamente R para poder mantener siempre la misma matriz de modularidad
            Rp = R[np.ix_(v > 0, v > 0)] # Parte de R asociada a los valores positivos de v
            Rm = R[np.ix_(v < 0, v < 0)] # Parte asociada a los valores negativos de v
            vp,lp,_ = metpot1(Rp)  # autovector principal de Rp
            vm,lm,_ = metpot1(Rm) # autovector principal de Rm
        
            # Calculamos el cambio en Q que se produciría al hacer esta partición
            Q1 = 0
            if not all(vp>0) or all(vp<0):
               Q1 = np.sum(Rp[vp>0,:][:,vp>0]) + np.sum(Rp[vp<0,:][:,vp<0])
            if not all(vm>0) or all(vm<0):
                Q1 += np.sum(Rm[vm>0,:][:,vm>0]) + np.sum(Rm[vm<0,:][:,vm<0])
            if Q0 >= Q1: # Si al partir obtuvimos un Q menor, devolvemos la última partición que hicimos
                return([[ni for ni,vi in zip(nombres_s,v) if vi>0],[ni for ni,vi in zip(nombres_s,v) if vi<0]])
            else:
                # Sino, repetimos para los subniveles
                return modularidad_iterativo(R=Rp, nombres_s=[nombres_s[i] for i in range(len(v)) if v[i] > 0]) + modularidad_iterativo(R=Rm, nombres_s=[nombres_s[i] for i in range(len(v)) if v[i] < 0])

