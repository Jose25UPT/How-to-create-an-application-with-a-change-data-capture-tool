from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuración del consumidor
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor Kafka
    'group.id': 'my-group',  # Grupo de consumidores
    'auto.offset.reset': 'earliest'  # Comienza desde el principio si es la primera vez
}

# Crear instancia del consumidor
consumer = Consumer(consumer_config)

# Suscribirse al tema
consumer.subscribe(['dbserver1.demo.products'])

# Leer mensajes del tema
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Polling con un timeout de 1 segundo
        if msg is None:  # No hay mensajes disponibles
            continue
        if msg.error():  # Error en el mensaje
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Fin de partición alcanzado {msg.partition} {msg.offset()}")
            else:
                raise KafkaException(msg.error())  # Excepciones si ocurre un error
        else:
            print(f"Recibido mensaje: {msg.value().decode('utf-8')}")  # Imprime el mensaje

except KeyboardInterrupt:
    print("Interrupción por el usuario")  # Permite interrumpir el consumo con Ctrl+C

finally:
    # Cerrar el consumidor
    consumer.close()
    print("Consumidor cerrado.")
