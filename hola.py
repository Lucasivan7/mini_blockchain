# Importamos las librerias necesarias para crear la blockchain
import hashlib
import json
from time import time
start_time = time()




# Datos del bloque, autor, contenido, tiempo.
autor = ""
contenido = ""
tiempo = ""

datos = {
    'autor': "Lucas Caballero",
    'contenido': "Pensamientos del autor",
    'tiempo': "20"
}

# Creacion de un objeto
class Block:
    def __init__(self, index, transaccion, hash_anterior):
        self.index = index
        self.transaccion = transaccion
        self.hash_anterior = hash_anterior
        '''
        Se crea la clase Block, que contiene los datos del bloque, el index, transaccion y el hash anterior.
        index: es el numero de bloque
        transaccion: son los datos del bloque
        hash_anterior: es el hash del bloque anterior
        '''


    def nueva_transaccion(autor, contenido):
        datos = {
            'autor': autor,
            'contenido': contenido,
                }
        return datos
        '''
        Creamos la funcion nueva_transaccion: que crea un diccionario con los datos del autor y el contenido.
        '''
    def hashear(self):
        bloque_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(bloque_string).hexdigest()
        '''
        Creamos la funcion hashear: que crea un hash del bloque.
        '''
class Blockchain():
    dificultad = 2
    def __init__(self):
        # La chain se define como una lista vacia, para poder almacenar los datos que va a contener.
        self.chain = []
        self.transaccion_pendiente = []
        self.create_genesis_block()

        '''
        Creamos la clase Blockchain, que contiene los datos de la blockchain, tambien definimos la dificultad de la blockchain.
        '''

    def create_genesis_block(self):
        genesis_block = Block(0, [], '0')
        genesis_block.hash = genesis_block.hashear
        self.chain.append(genesis_block)
        '''
        Creamos la funcion create_genesis_block: que crea el primer bloque de la blockchain.
        '''
    @property
    def last_block(self):
        return self.chain[-1]
        '''
        Definimos nuestra funcion last_block, como property, para que sea mas practico al ejecutar nuestro codigo.
        '''
    def proof_of_work(self, block):
        block.nonce = 0

        hash = block.hashear()
        while not hash.startswith('0' * Blockchain.dificultad):
            block.nonce += 1
            hash = block.hashear()

        return hash

        '''
        Creamos la funcion proof_of_work: que crea la prueba de trabajo, para minar el bloque.
        Pasamos como parametro el block, que es el bloque que queremos minar.
        '''

    def add_block(self, block, proof):

        hash_anterior = self.last_block.hashear()

        if hash_anterior != block.hash_anterior:
            return False
        
        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
        '''
        Creamos la funcion add_block: que agrega el bloque a la blockchain.
        Utilizando como parametro el block, y el proof
         Lo que realiza esta funcion es, agregar el bloque a la blockchain, y verificar que el hash del bloque anterior sea igual al hash del bloque actual.
        '''

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.dificultad) and block_hash == block.hashear())
        '''
        Creamos la funcion is_valid_proof: que verifica que el hash del bloque sea valido.
        Utilizando como parametro, la cantidad de 0 que deseamos que tenga el hash del bloque.
        '''

    def agregar_transacciones(self, transaccion):
        self.transaccion_pendiente.append(transaccion)
        '''
        Creamos la funcion agregar_transacciones, para poder agregar datos al bloque.
        '''

    def minar(self):
        if not self.transaccion_pendiente:
            return False

        last_block = self.last_block

        new_block = Block(index = last_block.index + 1, transaccion = self.transaccion_pendiente, hash_anterior = last_block.hash)

        proof = self.proof_of_work(new_block)

        self.add_block(new_block, proof)

        self.transaccion_pendiente = []

        return new_block.index
        '''
        Creamos la funcion minar: que mina el bloque.
        '''
